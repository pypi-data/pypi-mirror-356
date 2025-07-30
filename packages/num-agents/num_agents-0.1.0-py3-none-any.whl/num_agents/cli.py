"""
Command-line interface for the Nüm Agents SDK.

This module provides a command-line interface for generating agent scaffolds
based on agent specifications.
"""

import os
import sys
from pathlib import Path
from typing import Optional

import typer

from num_agents.composer.composer import NumAgentsComposer
from num_agents.graph.logical_graph import generate_logical_graph
from num_agents.orchestrator.meta_orchestrator import MetaOrchestrator, analyze_agent

app = typer.Typer(
    name="num-agents",
    help="Command-line interface for the Nüm Agents SDK.",
    add_completion=False,
)


@app.command("generate")
def generate(
    agent_spec: str = typer.Argument(
        ...,
        help="Path to the agent specification YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    univers_catalog: Optional[str] = typer.Option(
        None,
        "--univers-catalog",
        "-u",
        help="Path to the universe catalog YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_dir: Optional[str] = typer.Option(
        None,
        "--output-dir",
        "-o",
        help="Output directory for the generated scaffold",
    ),
    skip_graph: bool = typer.Option(
        False,
        "--skip-graph",
        "-s",
        help="Skip generating the logical graph",
    ),
    skip_audit: bool = typer.Option(
        False,
        "--skip-audit",
        "-a",
        help="Skip generating the audit report",
    ),
) -> None:
    """
    Generate an agent scaffold based on an agent specification.
    
    This command generates an agent scaffold based on an agent specification,
    including a logical graph and an audit report.
    """
    # Generate the scaffold
    composer = NumAgentsComposer(agent_spec, univers_catalog, output_dir)
    output_dir = composer.generate_scaffold()
    
    typer.echo(f"Generated agent scaffold in {output_dir}")
    
    # Generate the logical graph
    if not skip_graph:
        mermaid_path, markdown_path = generate_logical_graph(output_dir)
        typer.echo(f"Generated logical graph in {mermaid_path}")
        typer.echo(f"Generated logical graph markdown in {markdown_path}")
    
    # Generate the audit report
    if not skip_audit:
        report_path = analyze_agent(output_dir, agent_spec, univers_catalog)
        typer.echo(f"Generated audit report in {report_path}")


@app.command("audit")
def audit(
    agent_dir: str = typer.Argument(
        ...,
        help="Path to the agent directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    agent_spec: Optional[str] = typer.Option(
        None,
        "--agent-spec",
        "-a",
        help="Path to the agent specification YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    univers_catalog: Optional[str] = typer.Option(
        None,
        "--univers-catalog",
        "-u",
        help="Path to the universe catalog YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_path: Optional[str] = typer.Option(
        None,
        "--output-path",
        "-o",
        help="Output path for the audit report",
    ),
) -> None:
    """
    Generate an audit report for an agent.
    
    This command analyzes an agent and generates an audit report,
    summarizing the results of consistency checks and suggestions.
    """
    # Generate the audit report
    report_path = analyze_agent(agent_dir, agent_spec, univers_catalog, output_path)
    typer.echo(f"Generated audit report in {report_path}")


@app.command("suggest-yaml")
def suggest_yaml(
    agent_dir: str = typer.Argument(
        ...,
        help="Path to the agent directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    agent_spec: Optional[str] = typer.Option(
        None,
        "--agent-spec",
        "-a",
        help="Path to the agent specification YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    univers_catalog: Optional[str] = typer.Option(
        None,
        "--univers-catalog",
        "-u",
        help="Path to the universe catalog YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    output_path: Optional[str] = typer.Option(
        None,
        "--output-path",
        "-o",
        help="Output path for the YAML suggestions",
    ),
    rules_path: Optional[str] = typer.Option(
        None,
        "--rules-path",
        "-r",
        help="Path to the suggestion rules YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    summary: bool = typer.Option(
        False,
        "--summary",
        "-s",
        help="Show a summary of the agent analysis",
    ),
) -> None:
    """
    Generate suggestions for improving the agent.yaml file.
    
    This command analyzes an agent and generates suggestions for improving
    the agent.yaml file, including adding missing modules, removing unused
    modules, and adding relevant tags.
    """
    # Create a MetaOrchestrator instance
    orchestrator = MetaOrchestrator(
        agent_dir=agent_dir,
        agent_spec_path=agent_spec,
        univers_catalog_path=univers_catalog,
        rules_path=rules_path
    )
    
    # Generate and export the YAML suggestions
    suggestions_path = orchestrator.export_yaml_suggestions(output_path)
    typer.echo(f"Generated agent.yaml suggestions in {suggestions_path}")
    
    # Show a summary if requested
    if summary:
        summary_data = orchestrator.get_summary()
        typer.echo("\nAgent Analysis Summary:")
        typer.echo(f"Agent Name: {summary_data['agent_name']}")
        typer.echo(f"Status: {summary_data['status']}")
        typer.echo(f"Health Score: {summary_data['health_score']}")
        typer.echo(f"Completeness: {summary_data['completeness']}")
        typer.echo(f"Issues: {summary_data['issue_count']}")
        typer.echo("Suggestion Counts:")
        for priority, count in summary_data['suggestion_counts'].items():
            typer.echo(f"  {priority.capitalize()}: {count}")
        
        # Show critical suggestions
        critical_suggestions = orchestrator.get_critical_suggestions()
        if critical_suggestions:
            typer.echo("\nCritical Suggestions:")
            for i, suggestion in enumerate(critical_suggestions, 1):
                typer.echo(f"  {i}. {suggestion}")


@app.command("graph")
def graph(
    agent_dir: str = typer.Argument(
        ...,
        help="Path to the agent directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    output_mermaid: Optional[str] = typer.Option(
        None,
        "--output-mermaid",
        "-m",
        help="Output path for the Mermaid flowchart",
    ),
    output_markdown: Optional[str] = typer.Option(
        None,
        "--output-markdown",
        "-d",
        help="Output path for the Markdown representation",
    ),
) -> None:
    """
    Generate a logical graph for an agent.
    
    This command analyzes an agent and generates a logical graph,
    visualizing the dependencies and relationships between nodes.
    """
    # Generate the logical graph
    mermaid_path, markdown_path = generate_logical_graph(
        agent_dir, output_mermaid, output_markdown
    )
    typer.echo(f"Generated logical graph in {mermaid_path}")
    typer.echo(f"Generated logical graph markdown in {markdown_path}")


def main() -> None:
    """Run the CLI application."""
    app()


@app.command("generate-manifest")
def generate_manifest(
    project_path: str = typer.Argument(
        ...,
        help="Path to the agent project directory",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
    ),
    output_format: str = typer.Option(
        "markdown",
        "--format",
        "-f",
        help="Output format (markdown or json)",
    ),
    output_file: Optional[str] = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (default: manifest.{md|json} in project directory)",
    ),
):
    """
    Generate a manifest of all files in an agent project.
    
    This command analyzes an agent project directory and generates a manifest
    of all files, including descriptions and categorizations.
    """
    from num_agents.utils.manifest_generator import ManifestGenerator
    
    project_path = os.path.abspath(project_path)
    
    console.print(f"Generating manifest for project at [bold cyan]{project_path}[/]...")
    
    try:
        generator = ManifestGenerator(project_path)
        manifest = generator.generate_manifest(output_format)
        
        if output_file is None:
            ext = "md" if output_format.lower() == "markdown" else "json"
            output_file = os.path.join(project_path, f"manifest.{ext}")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(manifest)
        
        console.print(f"[bold green]Success:[/] Manifest generated at [bold cyan]{output_file}[/]")
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise typer.Exit(1)


if __name__ == "__main__":
    main()
