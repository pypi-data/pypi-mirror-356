"""
CLI commands for workflow management.

This module provides CLI commands for working with task chains
and the workflow engine.
"""

import os
import sys
import json
import yaml
import typer
from pathlib import Path
from typing import Optional

from num_agents.workflow.task_chain import WorkflowEngine, TaskChain
from num_agents.workflow.personas import registry as persona_registry
from num_agents.eventbus.eventbus import EventBus
from num_agents.core import SharedStore


app = typer.Typer(name="workflow", help="Commands for working with task chains")


@app.command("run")
def run_chain(
    chain_file: Path = typer.Argument(..., help="Path to the task chain YAML file"),
    output_dir: Optional[Path] = typer.Option(
        None, "--output-dir", "-o", help="Directory to store output files"
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
):
    """
    Run a task chain from a YAML file.
    
    This command loads a task chain from a YAML file and executes it
    using the workflow engine.
    """
    try:
        # Set up output directory
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
        else:
            output_dir = Path.cwd() / "workflow_output"
            output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set up event bus and shared store
        event_bus = EventBus()
        shared_store = SharedStore()
        
        # Set up workflow engine
        engine = WorkflowEngine(event_bus=event_bus, shared_store=shared_store)
        
        # Register personas from the registry
        for name in persona_registry.list_personas():
            handler = persona_registry.get(name)
            if handler:
                engine.register_persona(name, handler)
        
        # Load task chain
        typer.echo(f"Loading task chain from {chain_file}")
        chain = engine.load_chain(chain_file)
        
        # Print chain info
        typer.echo(f"Task chain loaded with {len(chain.steps)} steps")
        if verbose:
            for step in chain.steps:
                typer.echo(f"  Step {step.index}: {step.description} (Persona: {step.persona})")
        
        # Execute chain
        typer.echo("Executing task chain...")
        results = engine.execute_chain(chain)
        
        # Save results
        results_file = output_dir / "results.json"
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump({str(k): str(v) for k, v in results.items()}, f, indent=2)
        
        # Save output files
        for step_idx, result in results.items():
            if isinstance(result, dict):
                for file_path, content in result.items():
                    output_file = output_dir / file_path
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(content)
        
        typer.echo(f"Task chain execution completed. Results saved to {output_dir}")
        return 0
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        return 1


@app.command("create")
def create_chain(
    output_file: Path = typer.Argument(..., help="Path to the output task chain YAML file"),
    steps: int = typer.Option(3, "--steps", "-s", help="Number of steps to create"),
):
    """
    Create a sample task chain YAML file.
    
    This command creates a sample task chain YAML file with the specified
    number of steps.
    """
    try:
        # Create a sample task chain
        steps_list = []
        for i in range(steps):
            persona = "Architect" if i == 0 else "Planner" if i == 1 else "Coder"
            depends_on = [] if i == 0 else [i - 1]
            
            step = {
                "index": i,
                "persona": persona,
                "depends_on": depends_on,
                "description": f"Step {i}: {persona} task",
                "prompt": {
                    "text": f"This is the prompt for step {i}",
                    "requires": [],
                    "produces": [f"output_{i}.md"],
                    "internal_checks": []
                },
                "outputs": [f"output_{i}.md"]
            }
            steps_list.append(step)
        
        chain = {
            "steps": steps_list,
            "reflect": "Sample task chain",
            "err": [],
            "note": ["This is a sample task chain"],
            "warn": []
        }
        
        # Save the task chain
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(chain, f, default_flow_style=False)
        
        typer.echo(f"Sample task chain created at {output_file}")
        return 0
    except Exception as e:
        typer.echo(f"Error: {str(e)}", err=True)
        return 1


@app.command("validate")
def validate_chain(
    chain_file: Path = typer.Argument(..., help="Path to the task chain YAML file"),
):
    """
    Validate a task chain YAML file.
    
    This command loads a task chain from a YAML file and validates it
    against the task chain schema.
    """
    try:
        # Load the task chain
        with open(chain_file, "r", encoding="utf-8") as f:
            chain_data = yaml.safe_load(f)
        
        # Validate the task chain
        chain = TaskChain(**chain_data)
        
        # Print validation results
        typer.echo(f"Task chain validated successfully with {len(chain.steps)} steps")
        for step in chain.steps:
            typer.echo(f"  Step {step.index}: {step.description} (Persona: {step.persona})")
        
        return 0
    except Exception as e:
        typer.echo(f"Validation error: {str(e)}", err=True)
        return 1


if __name__ == "__main__":
    app()
