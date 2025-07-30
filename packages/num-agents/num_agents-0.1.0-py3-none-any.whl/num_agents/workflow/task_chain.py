"""
Task Chain module for Nüm Agents SDK.

This module provides functionality for defining and executing task chains
with dependencies, personas, and internal checks.
"""

import os
import yaml
import json
import logging
from typing import Dict, List, Optional, Any, Callable, Union, Set
from pathlib import Path
from datetime import datetime

from pydantic import BaseModel, Field, validator

from num_agents.eventbus.event import Event
from num_agents.eventbus.eventbus import EventBus


class TaskPrompt(BaseModel):
    """
    Model for a task prompt in a chain.
    
    A task prompt defines what a step requires, what it produces,
    and what internal checks should be performed.
    """
    text: str = Field(..., description="The prompt text for the task")
    requires: List[str] = Field(default_factory=list, description="Resources required by the task")
    produces: List[str] = Field(default_factory=list, description="Resources produced by the task")
    internal_checks: List[str] = Field(default_factory=list, description="Internal checks to perform")


class TaskStep(BaseModel):
    """
    Model for a step in a task chain.
    
    A task step represents a single unit of work in a task chain,
    with a specific persona, dependencies, and outputs.
    """
    index: int = Field(..., description="The index of the step in the chain")
    persona: str = Field(..., description="The persona responsible for executing the step")
    depends_on: List[int] = Field(default_factory=list, description="Indices of steps this step depends on")
    description: str = Field(..., description="A description of the step")
    prompt: TaskPrompt = Field(..., description="The prompt for the step")
    outputs: List[str] = Field(default_factory=list, description="Expected outputs of the step")
    
    @validator("depends_on")
    def validate_dependencies(cls, v: List[int], values: Dict[str, Any]) -> List[int]:
        """Validate that dependencies have lower indices than the current step."""
        if "index" in values and any(dep >= values["index"] for dep in v):
            raise ValueError(f"Step {values['index']} cannot depend on steps with equal or higher indices")
        return v


class TaskChain(BaseModel):
    """
    Model for a chain of tasks.
    
    A task chain represents a sequence of steps with dependencies,
    reflections, errors, notes, and warnings.
    """
    steps: List[TaskStep] = Field(..., description="The steps in the chain")
    reflect: Optional[str] = Field(None, description="Reflection on the chain")
    err: List[str] = Field(default_factory=list, description="Errors in the chain")
    note: List[str] = Field(default_factory=list, description="Notes about the chain")
    warn: List[str] = Field(default_factory=list, description="Warnings about the chain")
    
    @validator("steps")
    def validate_steps(cls, v: List[TaskStep]) -> List[TaskStep]:
        """Validate that all steps have unique indices."""
        indices = set()
        for step in v:
            if step.index in indices:
                raise ValueError(f"Duplicate step index: {step.index}")
            indices.add(step.index)
        return v


class PersonaContext(BaseModel):
    """
    Context provided to a persona handler.
    
    This includes information about the step being executed,
    results from dependencies, and access to shared storage.
    """
    step: Dict[str, Any] = Field(..., description="The step being executed")
    dependencies: Dict[int, Any] = Field(..., description="Results from dependencies")
    shared_store: Any = Field(None, description="Shared storage for the workflow")
    event_bus: Optional[EventBus] = Field(None, description="Event bus for publishing events")


class WorkflowEngine:
    """
    Engine for executing task chains.
    
    The workflow engine is responsible for loading task chains,
    registering personas, and executing task chains in the correct order.
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None, shared_store: Any = None):
        """
        Initialize the workflow engine.
        
        Args:
            event_bus: Optional event bus for publishing events
            shared_store: Optional shared storage for the workflow
        """
        self.event_bus = event_bus
        self.shared_store = shared_store
        self.personas: Dict[str, Callable[[PersonaContext], Any]] = {}
        self.task_results: Dict[int, Any] = {}
        self.logger = logging.getLogger(__name__)
    
    def register_persona(self, name: str, handler: Callable[[PersonaContext], Any]) -> None:
        """
        Register a persona handler.
        
        Args:
            name: The name of the persona
            handler: The handler function for the persona
        """
        self.personas[name] = handler
        self.logger.info(f"Registered persona: {name}")
    
    def load_chain(self, chain_file: Union[str, Path]) -> TaskChain:
        """
        Load a task chain from a YAML file.
        
        Args:
            chain_file: Path to the YAML file containing the task chain
            
        Returns:
            The loaded task chain
            
        Raises:
            FileNotFoundError: If the chain file does not exist
            ValueError: If the chain file is not valid YAML or does not contain a valid task chain
        """
        chain_path = Path(chain_file)
        if not chain_path.exists():
            raise FileNotFoundError(f"Chain file not found: {chain_file}")
        
        try:
            with open(chain_path, "r", encoding="utf-8") as f:
                chain_data = yaml.safe_load(f)
            
            return TaskChain(**chain_data)
        except Exception as e:
            raise ValueError(f"Failed to load chain from {chain_file}: {str(e)}")
    
    def save_chain(self, chain: TaskChain, output_file: Union[str, Path]) -> None:
        """
        Save a task chain to a YAML file.
        
        Args:
            chain: The task chain to save
            output_file: Path to the output YAML file
            
        Raises:
            ValueError: If the chain cannot be saved
        """
        try:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(json.loads(chain.json()), f, default_flow_style=False)
        except Exception as e:
            raise ValueError(f"Failed to save chain to {output_file}: {str(e)}")
    
    def execute_chain(self, chain: TaskChain) -> Dict[int, Any]:
        """
        Execute a task chain.
        
        Args:
            chain: The task chain to execute
            
        Returns:
            A dictionary mapping step indices to their results
            
        Raises:
            ValueError: If a dependency is missing or a persona is not registered
        """
        # Reset results
        self.task_results = {}
        
        # Sort steps by dependencies
        steps = self._sort_steps_by_dependencies(chain.steps)
        
        for step in steps:
            self.logger.info(f"Executing step {step.index}: {step.description}")
            
            # Check dependencies
            for dep_idx in step.depends_on:
                if dep_idx not in self.task_results:
                    raise ValueError(f"Step {step.index} depends on step {dep_idx}, but it has not been executed")
            
            # Check persona
            if step.persona not in self.personas:
                raise ValueError(f"Persona '{step.persona}' not registered")
            
            # Prepare context for the step
            context = PersonaContext(
                step=step.dict(),
                dependencies={idx: self.task_results[idx] for idx in step.depends_on},
                shared_store=self.shared_store,
                event_bus=self.event_bus
            )
            
            # Execute persona handler
            try:
                start_time = datetime.now()
                result = self.personas[step.persona](context)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                
                self.task_results[step.index] = result
                self.logger.info(f"Step {step.index} completed in {duration:.2f}s")
                
                # Publish event if event_bus is available
                if self.event_bus:
                    event = Event(
                        event_type="workflow.step.completed",
                        payload={
                            "step_index": step.index,
                            "persona": step.persona,
                            "description": step.description,
                            "duration": duration,
                            "result": result
                        },
                        source="WorkflowEngine"
                    )
                    self.event_bus.publish(event)
            except Exception as e:
                self.logger.error(f"Step {step.index} failed: {str(e)}")
                
                # Publish error event if event_bus is available
                if self.event_bus:
                    event = Event(
                        event_type="workflow.step.failed",
                        payload={
                            "step_index": step.index,
                            "persona": step.persona,
                            "description": step.description,
                            "error": str(e)
                        },
                        source="WorkflowEngine"
                    )
                    self.event_bus.publish(event)
                
                raise ValueError(f"Step {step.index} failed: {str(e)}")
        
        return self.task_results
    
    def _sort_steps_by_dependencies(self, steps: List[TaskStep]) -> List[TaskStep]:
        """
        Sort steps by dependencies using topological sort.
        
        Args:
            steps: The steps to sort
            
        Returns:
            The sorted steps
            
        Raises:
            ValueError: If there is a circular dependency
        """
        # Create a graph representation
        graph: Dict[int, Set[int]] = {step.index: set(step.depends_on) for step in steps}
        
        # Find nodes with no dependencies
        no_deps = [idx for idx, deps in graph.items() if not deps]
        
        # Topological sort
        sorted_indices = []
        while no_deps:
            # Remove a node with no dependencies
            idx = no_deps.pop(0)
            sorted_indices.append(idx)
            
            # Remove edges from the graph
            for node, deps in graph.items():
                if idx in deps:
                    deps.remove(idx)
                    if not deps and node not in sorted_indices and node not in no_deps:
                        no_deps.append(node)
        
        # Check for circular dependencies
        if len(sorted_indices) != len(steps):
            raise ValueError("Circular dependency detected in task chain")
        
        # Map indices back to steps
        index_to_step = {step.index: step for step in steps}
        return [index_to_step[idx] for idx in sorted_indices]
