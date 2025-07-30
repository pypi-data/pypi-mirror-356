# CLI Commands

This document describes the command-line interface (CLI) commands available in the Nüm Agents SDK.

## Table of Contents

- [generate](#generate)
- [audit](#audit)
- [suggest-yaml](#suggest-yaml)
- [graph](#graph)
- [generate-manifest](#generate-manifest)

## generate

Generate an agent scaffold based on an agent specification.

```bash
num-agents generate <agent_spec> [OPTIONS]
```

### Arguments

- `agent_spec`: Path to the agent specification YAML file.

### Options

- `--univers-catalog`, `-u`: Path to the universe catalog YAML file.
- `--output-dir`, `-o`: Output directory for the generated scaffold.

### Example

```bash
num-agents generate agent.yaml --univers-catalog univers_catalog.yaml --output-dir my_agent
```

## audit

Generate an audit report for an agent.

```bash
num-agents audit <agent_dir> [OPTIONS]
```

### Arguments

- `agent_dir`: Path to the agent directory.

### Options

- `--agent-spec`, `-a`: Path to the agent specification YAML file.
- `--univers-catalog`, `-u`: Path to the universe catalog YAML file.
- `--output-path`, `-o`: Output path for the audit report.

### Example

```bash
num-agents audit my_agent --output-path audit_report.json
```

## suggest-yaml

Generate suggestions for improving the agent.yaml file.

```bash
num-agents suggest-yaml <agent_dir> [OPTIONS]
```

### Arguments

- `agent_dir`: Path to the agent directory.

### Options

- `--agent-spec`, `-a`: Path to the agent specification YAML file.
- `--univers-catalog`, `-u`: Path to the universe catalog YAML file.
- `--output-path`, `-o`: Output path for the YAML suggestions.
- `--rules-path`, `-r`: Path to the suggestion rules YAML file.
- `--summary`, `-s`: Show a summary of the agent analysis.

### Example

```bash
num-agents suggest-yaml my_agent --output-path suggestions.yaml --summary
```

## graph

Generate a logical graph for an agent.

```bash
num-agents graph <agent_dir> [OPTIONS]
```

### Arguments

- `agent_dir`: Path to the agent directory.

### Options

- `--output-mermaid`, `-m`: Output path for the Mermaid flowchart.
- `--output-markdown`, `-d`: Output path for the Markdown representation.

### Example

```bash
num-agents graph my_agent --output-mermaid logical_graph.mmd --output-markdown logical_graph.md
```

## generate-manifest

Generate a manifest of all files in an agent project.

```bash
num-agents generate-manifest <project_path> [OPTIONS]
```

### Arguments

- `project_path`: Path to the agent project directory.

### Options

- `--format`, `-f`: Output format (markdown or json). Default: markdown.
- `--output`, `-o`: Output file path. Default: manifest.md or manifest.json in the project directory.

### Example

```bash
num-agents generate-manifest my_agent --format markdown --output my_agent/manifest.md
```

The manifest includes:

- A table of contents with links to each category section
- Files grouped by category (root, nodes, docs, etc.)
- For each file:
  - Path relative to the project root
  - Type (core, node, python, documentation, configuration, etc.)
  - Description based on file content and purpose

### Sample Output (Markdown)

```markdown
# Project Files Manifest

This document provides an overview of all files in the project, their descriptions, and types.

## Table of Contents

- [Root](#root)
- [Nodes](#nodes)
- [Docs](#docs)

## Root

| File | Type | Description |
| ---- | ---- | ----------- |
| `agent.yaml` | configuration | Agent specification file defining the agent's configuration, universes, and modules |
| `flow.py` | core | Flow definition for the agent, connecting nodes in a processing pipeline |
| `main.py` | core | Entry point for the agent, initializing and running the flow |

## Nodes

| File | Type | Description |
| ---- | ---- | ----------- |
| `nodes/process_node.py` | node | Node implementation: process_node |
| `nodes/input_node.py` | node | Node implementation: input_node |

## Docs

| File | Type | Description |
| ---- | ---- | ----------- |
| `docs/README.md` | documentation | Documentation: Agent Overview |
```
