# Agent YAML Schema

This document describes the schema for the `agent.yaml` configuration file used in the Nüm Agents SDK.

## Basic Structure

The `agent.yaml` file defines the configuration for an agent, including its name, description, universes, protocol, LLM, and various features.

```yaml
agent:
  name: "ExampleAgent"
  description: "An example agent built with Nüm Agents SDK"
  univers:
    - PocketFlowCore
    - StructureAgentIA
  protocol: N2A
  llm: gpt-4o
  memory: true
  eventbus: true
  scheduler: true
  metrics: true
  tracing: true
```

## Enhanced Sections

The `agent.yaml` file can also include enhanced sections for working memory, expertise, and semantic entities.

### Working Memory

The `working_memory` section defines the agent's goals, context, constraints, and preferences. This information is loaded into the `SharedStore` during initialization and can be accessed by nodes during flow execution.

```yaml
agent:
  # ... basic configuration ...
  
  working_memory:
    goals:
      - "Assist users with data analysis tasks"
      - "Generate insightful visualizations"
    context:
      domain: "data science"
      project_type: "data analysis"
      user_expertise: "intermediate"
    constraints:
      - "Do not modify original data files"
      - "Respect user privacy"
    preferences:
      visualization_style: "minimalist"
      color_scheme: "blue"
```

### Expertise

The `expertise` section defines the agent's areas of expertise, including domains, skills, and knowledge bases. This information can be used to guide the agent's behavior and decision-making.

```yaml
agent:
  # ... basic configuration ...
  
  expertise:
    domains:
      - name: "data_analysis"
        proficiency: 0.9
        description: "Statistical analysis of datasets"
      - name: "machine_learning"
        proficiency: 0.8
        description: "Building and evaluating ML models"
    skills:
      - name: "python_programming"
        proficiency: 0.9
      - name: "sql_queries"
        proficiency: 0.8
    knowledge_bases:
      - name: "statistics_fundamentals"
        source: "internal"
      - name: "visualization_best_practices"
        source: "external"
        url: "https://example.com/viz-practices"
```

### Semantic Entities

The `semantic_entities` section defines the entities that the agent can manipulate, including their properties and relations. This information can be used for semantic reasoning and knowledge representation.

```yaml
agent:
  # ... basic configuration ...
  
  semantic_entities:
    - name: "Dataset"
      properties:
        - name: "source"
          type: "string"
        - name: "size"
          type: "integer"
        - name: "columns"
          type: "list"
      relations:
        - name: "contains"
          target: "DataPoint"
        - name: "derived_from"
          target: "Dataset"
    - name: "DataPoint"
      properties:
        - name: "values"
          type: "dict"
        - name: "timestamp"
          type: "datetime"
      relations:
        - name: "belongs_to"
          target: "Dataset"
```

## Accessing Agent Configuration

The agent configuration can be loaded using the `AgentSpecLoader` class:

```python
from num_agents.utils.file_io import AgentSpecLoader

# Load agent specification
loader = AgentSpecLoader("path/to/agent.yaml")
spec = loader.load()

# Access basic configuration
agent_name = loader.get_agent_name()
agent_description = loader.get_agent_description()
agent_universes = loader.get_agent_universes()

# Access working memory
working_memory = loader.get_working_memory()
goals = loader.get_goals()
context = loader.get_context()
constraints = loader.get_constraints()
preferences = loader.get_preferences()

# Access expertise
expertise = loader.get_expertise()
domains = loader.get_domains()
skills = loader.get_skills()
knowledge_bases = loader.get_knowledge_bases()

# Access semantic entities
semantic_entities = loader.get_semantic_entities()
```

## Integrating with SharedStore

The agent configuration can be used to initialize a `SharedStore` with working memory:

```python
from num_agents.utils.file_io import AgentSpecLoader
from num_agents.core import SharedStore

# Load agent specification
loader = AgentSpecLoader("path/to/agent.yaml")
spec = loader.load()

# Initialize SharedStore with agent specification
store = SharedStore(spec)

# Access working memory from SharedStore
goals = store.get_goals()
context = store.get_context()
constraints = store.get_constraints()
preferences = store.get_preferences()

# Update working memory
store.update_working_memory({
    "goals": ["New Goal 1", "New Goal 2"],
    "context": {
        "domain": "new domain",
        "additional_info": "new info"
    }
})
```

This integration allows nodes in a flow to access and update the agent's working memory during execution, providing a shared context for decision-making and reasoning.
