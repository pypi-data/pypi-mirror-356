"""
Personas module for Nüm Agents SDK.

This module provides predefined personas for use in task chains.
Personas are specialized roles that can be assigned to steps in a task chain.
"""

import logging
from typing import Any, Dict, List, Optional, Callable

from num_agents.workflow.task_chain import PersonaContext


class PersonaRegistry:
    """
    Registry for personas.
    
    The persona registry maintains a collection of persona handlers
    that can be used in task chains.
    """
    
    def __init__(self):
        """Initialize the persona registry."""
        self.personas: Dict[str, Callable[[PersonaContext], Any]] = {}
        self.logger = logging.getLogger(__name__)
    
    def register(self, name: str, handler: Callable[[PersonaContext], Any]) -> None:
        """
        Register a persona handler.
        
        Args:
            name: The name of the persona
            handler: The handler function for the persona
        """
        self.personas[name] = handler
        self.logger.info(f"Registered persona: {name}")
    
    def get(self, name: str) -> Optional[Callable[[PersonaContext], Any]]:
        """
        Get a persona handler by name.
        
        Args:
            name: The name of the persona
            
        Returns:
            The persona handler, or None if not found
        """
        return self.personas.get(name)
    
    def list_personas(self) -> List[str]:
        """
        List all registered personas.
        
        Returns:
            A list of persona names
        """
        return list(self.personas.keys())


# Global persona registry
registry = PersonaRegistry()


def architect_persona(context: PersonaContext) -> Dict[str, Any]:
    """
    Architect persona for task chains.
    
    The architect persona is responsible for high-level design decisions,
    system architecture, and technical direction.
    
    Args:
        context: The context for the persona handler
        
    Returns:
        The result of the architect's work
    """
    step = context.step
    description = step.get("description", "")
    prompt = step.get("prompt", {})
    prompt_text = prompt.get("text", "")
    
    # Log the architect's task
    logging.info(f"Architect persona executing: {description}")
    logging.info(f"Prompt: {prompt_text}")
    
    # Check what the architect needs to produce
    outputs = step.get("outputs", [])
    results = {}
    
    # Simulate the architect's work
    for output in outputs:
        if output.endswith(".md"):
            results[output] = f"# {description}\n\n{prompt_text}\n\nArchitect's analysis and design..."
        elif output.endswith(".yaml") or output.endswith(".yml"):
            results[output] = f"# {description}\nversion: 1.0\ndesign:\n  key: value"
    
    # Store results in shared store if available
    if context.shared_store is not None:
        for key, value in results.items():
            context.shared_store.set(f"architect.{key}", value)
    
    # Publish event if event bus is available
    if context.event_bus is not None:
        context.event_bus.publish({
            "type": "persona.architect.completed",
            "description": description,
            "results": list(results.keys())
        })
    
    return results


def planner_persona(context: PersonaContext) -> Dict[str, Any]:
    """
    Planner persona for task chains.
    
    The planner persona is responsible for breaking down tasks,
    defining modules, and creating implementation plans.
    
    Args:
        context: The context for the persona handler
        
    Returns:
        The result of the planner's work
    """
    step = context.step
    description = step.get("description", "")
    prompt = step.get("prompt", {})
    prompt_text = prompt.get("text", "")
    
    # Log the planner's task
    logging.info(f"Planner persona executing: {description}")
    logging.info(f"Prompt: {prompt_text}")
    
    # Check dependencies
    dependencies = context.dependencies
    dependency_results = []
    for dep_idx, dep_result in dependencies.items():
        dependency_results.append(f"Dependency {dep_idx}: {list(dep_result.keys())}")
    
    # Check what the planner needs to produce
    outputs = step.get("outputs", [])
    results = {}
    
    # Simulate the planner's work
    for output in outputs:
        if output.endswith(".yaml") or output.endswith(".yml"):
            results[output] = f"# {description}\nversion: 1.0\nplan:\n  modules:\n    - name: module1\n    - name: module2"
        elif output.endswith(".md"):
            results[output] = f"# {description}\n\n{prompt_text}\n\nPlanner's analysis and plan...\n\nBased on: {', '.join(dependency_results)}"
    
    # Store results in shared store if available
    if context.shared_store is not None:
        for key, value in results.items():
            context.shared_store.set(f"planner.{key}", value)
    
    # Publish event if event bus is available
    if context.event_bus is not None:
        context.event_bus.publish({
            "type": "persona.planner.completed",
            "description": description,
            "results": list(results.keys())
        })
    
    return results


def designer_persona(context: PersonaContext) -> Dict[str, Any]:
    """
    Designer persona for task chains.
    
    The designer persona is responsible for UI/UX design,
    user flows, and visual elements.
    
    Args:
        context: The context for the persona handler
        
    Returns:
        The result of the designer's work
    """
    step = context.step
    description = step.get("description", "")
    prompt = step.get("prompt", {})
    prompt_text = prompt.get("text", "")
    
    # Log the designer's task
    logging.info(f"Designer persona executing: {description}")
    logging.info(f"Prompt: {prompt_text}")
    
    # Check dependencies
    dependencies = context.dependencies
    dependency_results = []
    for dep_idx, dep_result in dependencies.items():
        dependency_results.append(f"Dependency {dep_idx}: {list(dep_result.keys())}")
    
    # Check what the designer needs to produce
    outputs = step.get("outputs", [])
    results = {}
    
    # Simulate the designer's work
    for output in outputs:
        if output.endswith(".tsx") or output.endswith(".jsx"):
            results[output] = f"// {description}\nimport React from 'react';\n\nexport default function Component() {{\n  return <div>Designer's UI component</div>;\n}}"
        elif output.endswith(".md"):
            results[output] = f"# {description}\n\n{prompt_text}\n\nDesigner's UI/UX design...\n\nBased on: {', '.join(dependency_results)}"
    
    # Store results in shared store if available
    if context.shared_store is not None:
        for key, value in results.items():
            context.shared_store.set(f"designer.{key}", value)
    
    # Publish event if event bus is available
    if context.event_bus is not None:
        context.event_bus.publish({
            "type": "persona.designer.completed",
            "description": description,
            "results": list(results.keys())
        })
    
    return results


def coder_persona(context: PersonaContext) -> Dict[str, Any]:
    """
    Coder persona for task chains.
    
    The coder persona is responsible for implementing code,
    writing tests, and fixing bugs.
    
    Args:
        context: The context for the persona handler
        
    Returns:
        The result of the coder's work
    """
    step = context.step
    description = step.get("description", "")
    prompt = step.get("prompt", {})
    prompt_text = prompt.get("text", "")
    
    # Log the coder's task
    logging.info(f"Coder persona executing: {description}")
    logging.info(f"Prompt: {prompt_text}")
    
    # Check dependencies
    dependencies = context.dependencies
    dependency_results = []
    for dep_idx, dep_result in dependencies.items():
        dependency_results.append(f"Dependency {dep_idx}: {list(dep_result.keys())}")
    
    # Check what the coder needs to produce
    outputs = step.get("outputs", [])
    results = {}
    
    # Simulate the coder's work
    for output in outputs:
        if output.endswith(".py"):
            results[output] = f"# {description}\n\ndef main():\n    print('Coder's implementation')\n\nif __name__ == '__main__':\n    main()"
        elif output.endswith(".js") or output.endswith(".ts"):
            results[output] = f"// {description}\n\nfunction main() {{\n  console.log('Coder's implementation');\n}}\n\nmain();"
        elif output.endswith(".md"):
            results[output] = f"# {description}\n\n{prompt_text}\n\nCoder's implementation notes...\n\nBased on: {', '.join(dependency_results)}"
    
    # Store results in shared store if available
    if context.shared_store is not None:
        for key, value in results.items():
            context.shared_store.set(f"coder.{key}", value)
    
    # Publish event if event bus is available
    if context.event_bus is not None:
        context.event_bus.publish({
            "type": "persona.coder.completed",
            "description": description,
            "results": list(results.keys())
        })
    
    return results


# Register default personas
registry.register("Architect", architect_persona)
registry.register("Planner", planner_persona)
registry.register("Designer", designer_persona)
registry.register("Coder", coder_persona)
