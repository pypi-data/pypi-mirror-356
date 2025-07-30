# Multi-Expertise Aggregation

## Overview

The Multi-Expertise Aggregation framework provides a powerful way to combine insights from multiple expert agents or knowledge domains. This system allows you to:

1. Weight propositions based on domain expertise
2. Aggregate confidence scores from multiple agents using various strategies
3. Dynamically select the optimal aggregation method based on data characteristics
4. Make decisions based on confidence thresholds

## Components

The framework consists of two main components:

1. **MultiExpertiseAggregationNode**: Combines confidence scores from multiple agents
2. **DynamicExpertiseFlow**: Orchestrates the entire reasoning process with automatic context detection

## MultiExpertiseAggregationNode

### Purpose

The `MultiExpertiseAggregationNode` takes confidence scores from multiple expert agents and combines them using a specified aggregation strategy.

### Features

- Multiple aggregation strategies (mean, max, min, median, softmax, etc.)
- Support for agent weighting (giving some agents more influence than others)
- Detailed per-agent confidence reporting
- Robust aggregation methods that handle outliers

### Usage

```python
from num_agents.reasoning.nodes.multi_expertise_aggregation_node import MultiExpertiseAggregationNode

# Create the node
aggregation_node = MultiExpertiseAggregationNode()

# Set up shared store with required components
shared_store = {
    "logic_engine": logic_engine,
    "current_context_id": context_id,
    "expertises": [expertise1, expertise2, expertise3],  # List of Expertise objects
    "aggregation_strategy": "mean",  # Optional, defaults to "mean"
    "agent_weights": [0.8, 1.0, 0.9],  # Optional, weights for each expertise
    "return_agent_details": True,  # Optional, return per-agent confidence details
    "robust_aggregation_params": {  # Optional, parameters for robust strategies
        "trim_percent": 0.1,  # For trimmed_mean
        "winsor_percent": 0.1  # For winsorized_mean
    }
}

# Run the node
updated_store = aggregation_node._run(shared_store)

# Access results
agent_confidence_details = updated_store.get("agent_confidence_details", {})
```

### Aggregation Strategies

| Strategy | Description | Best Used When |
|----------|-------------|----------------|
| `mean` | Simple average of all scores | Scores are consistent across agents |
| `max` | Maximum score among all agents | You need an optimistic estimate |
| `min` | Minimum score among all agents | You need a conservative estimate |
| `median` | Middle value of sorted scores | There are potential outliers |
| `softmax` | Weighted average based on exponential scaling | Some agents are much more confident |
| `trimmed_mean` | Mean after removing extreme values | There are definite outliers |
| `winsorized_mean` | Mean after capping extreme values | There are extreme values but you don't want to discard them |

### Custom Aggregation Functions

You can also provide a custom aggregation function:

```python
def custom_aggregation(scores, weights=None):
    # Your custom aggregation logic here
    return calculated_score

shared_store["aggregation_strategy"] = custom_aggregation
```

## DynamicExpertiseFlow

### Purpose

The `DynamicExpertiseFlow` orchestrates the entire multi-expertise reasoning process, from context detection to decision making.

### Features

- Auto-detects single vs multi-agent contexts
- Dynamically selects the optimal aggregation strategy based on data characteristics
- Applies expertise weighting to propositions
- Makes decisions based on confidence thresholds
- Provides detailed agent-by-agent analysis

### Usage

```python
from num_agents.reasoning.nodes.dynamic_expertise_flow import DynamicExpertiseFlow

# Create the flow
flow = DynamicExpertiseFlow(
    name="ReasoningFlow",
    confidence_threshold=0.7,  # Threshold for accepting propositions
    auto_select_strategy=True,  # Automatically select best aggregation strategy
    aggregation_strategy="mean",  # Default strategy if auto_select is False
    robust_params={  # Parameters for robust aggregation strategies
        "trim_percent": 0.1,
        "winsor_percent": 0.1
    }
)

# Set up shared store with required components
shared_store = {
    "logic_engine": logic_engine,
    "current_context_id": context_id,
    "expertises": [expertise1, expertise2, expertise3]  # For multi-agent mode
    # OR
    # "expertise": expertise  # For single-agent mode
}

# Run the flow
updated_store = flow._run(shared_store)

# Access results
is_multi_agent = updated_store.get("is_multi_agent", False)
selected_strategy = updated_store.get("selected_strategy")
proposition_decisions = updated_store.get("proposition_decisions", {})
proposition_scores_by_agent = updated_store.get("proposition_scores_by_agent", {})
```

### Strategy Selection Logic

When `auto_select_strategy` is enabled, the flow analyzes the distribution of confidence scores and selects the optimal aggregation strategy:

- If scores have outliers: uses `trimmed_mean`
- If scores have high variance: uses `winsorized_mean`
- If scores have positive skew (some high values): uses `softmax`
- If scores have negative skew (some low values): uses `median`
- Otherwise: uses `mean`

## Complete Example

See `examples/dynamic_expertise_flow_demo.py` for a complete working example that demonstrates:

1. Setting up a reasoning context with propositions
2. Creating multiple expertises with different domain knowledge
3. Running the DynamicExpertiseFlow
4. Analyzing the results

## Best Practices

1. **Define Expertises Carefully**: Ensure each expertise has well-defined domains and relations with appropriate weights.

2. **Use Agent Weighting**: If some agents are more reliable than others, use agent weights to give them more influence.

3. **Consider Robust Strategies**: When combining opinions from diverse experts, robust aggregation strategies like `trimmed_mean` can help handle outliers.

4. **Analyze Per-Agent Scores**: Look at the individual agent scores to understand where there is agreement or disagreement.

5. **Adjust Confidence Threshold**: Set the confidence threshold based on your application's needs - higher for critical decisions, lower for exploratory reasoning.

## Advanced Configuration

### Custom Strategy Selection

You can override the automatic strategy selection by implementing your own selection logic:

```python
class CustomExpertiseFlow(DynamicExpertiseFlow):
    def _select_optimal_strategy(self, proposition_scores_by_agent):
        # Your custom selection logic here
        return selected_strategy
```

### Integrating with External Systems

The framework can be integrated with external AI systems by:

1. Converting external agent outputs to `Expertise` objects
2. Adding these to the `expertises` list in the shared store
3. Running the flow to get aggregated decisions
