# Dynamic Expertise Flow

## Overview

The `DynamicExpertiseFlow` is an advanced orchestration node that coordinates multi-expertise reasoning with automatic context detection. It represents a complete reasoning pipeline that handles everything from expertise application to decision making.

## Key Features

- **Automatic Context Detection**: Automatically detects if you're in a single-agent or multi-agent environment
- **Dynamic Strategy Selection**: Analyzes data characteristics to select the optimal aggregation strategy
- **Expertise-Based Confidence Weighting**: Applies domain expertise to weight proposition confidence
- **Threshold-Based Decision Making**: Makes decisions based on configurable confidence thresholds
- **Detailed Analysis**: Provides comprehensive agent-by-agent confidence reporting

## Architecture

The `DynamicExpertiseFlow` orchestrates a complete reasoning flow:

```
┌─────────────────────────────────────────────────────────────────┐
│                     DynamicExpertiseFlow                        │
│                                                                 │
│  ┌─────────────┐    ┌───────────────────────────┐    ┌────────┐ │
│  │ Context     │    │ For each expertise:       │    │Decision│ │
│  │ Detection   │───►│ ExpertiseWeightingNode    │───►│Making  │ │
│  └─────────────┘    └───────────────────────────┘    └────────┘ │
│         │                         │                      │      │
│         │                         ▼                      │      │
│         │           ┌───────────────────────────┐        │      │
│         └──────────►│MultiExpertiseAggregation  │◄───────┘      │
│                     └───────────────────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Usage

### Basic Usage

```python
from num_agents.reasoning.nodes.dynamic_expertise_flow import DynamicExpertiseFlow

# Create the flow
flow = DynamicExpertiseFlow(
    name="ReasoningFlow",
    confidence_threshold=0.7,
    auto_select_strategy=True
)

# Set up shared store
shared_store = {
    "logic_engine": logic_engine,
    "current_context_id": context_id,
    "expertises": [expertise1, expertise2, expertise3]  # For multi-agent mode
}

# Run the flow
result = flow._run(shared_store)
```

### Configuration Options

```python
flow = DynamicExpertiseFlow(
    name="CustomFlow",
    confidence_threshold=0.8,  # Higher threshold for stricter decisions
    auto_select_strategy=False,  # Use fixed strategy instead of auto-selection
    aggregation_strategy="softmax",  # Fixed strategy to use
    robust_params={  # Parameters for robust aggregation strategies
        "trim_percent": 0.2,  # Trim 20% from each end for trimmed_mean
        "winsor_percent": 0.1  # Cap 10% from each end for winsorized_mean
    }
)
```

## Input Requirements

The `shared_store` dictionary must contain:

- `logic_engine`: An instance of `LogicEngine`
- `current_context_id`: ID of the current reasoning context
- Either:
  - `expertises`: A list of `Expertise` objects (for multi-agent mode)
  - `expertise`: A single `Expertise` object (for single-agent mode)

## Output

The flow adds the following to the `shared_store`:

- `proposition_decisions`: Dictionary mapping proposition IDs to boolean decisions
- `proposition_scores_by_agent`: Dictionary mapping proposition IDs to lists of agent scores
- `is_multi_agent`: Boolean indicating if multi-agent mode was detected
- `selected_strategy`: The aggregation strategy that was selected (if in multi-agent mode)

## Flow Process

1. **Context Detection**:
   - Determines if we're in a single-agent or multi-agent context
   - In single-agent mode, converts the single expertise to a list for consistent processing

2. **Expertise Weighting**:
   - For each expertise, runs the `ExpertiseWeightingNode` to apply domain-specific weighting
   - Collects confidence scores for each proposition from each agent

3. **Strategy Selection** (if in multi-agent mode and `auto_select_strategy` is enabled):
   - Analyzes the distribution of confidence scores
   - Selects the optimal aggregation strategy based on:
     - Presence of outliers
     - Variance in scores
     - Skewness of the distribution

4. **Score Aggregation** (if in multi-agent mode):
   - Runs the `MultiExpertiseAggregationNode` with the selected strategy
   - Combines scores from all agents into a single confidence score for each proposition

5. **Decision Making**:
   - Compares aggregated confidence scores against the confidence threshold
   - Makes accept/reject decisions for each proposition
   - Updates proposition status to `VERIFIED` if confidence exceeds threshold

## Strategy Selection Logic

When `auto_select_strategy` is enabled, the flow uses the following logic:

| Data Characteristic | Selected Strategy | Rationale |
|---------------------|-------------------|-----------|
| Has outliers | `trimmed_mean` | Removes extreme values that could skew the result |
| High variance | `winsorized_mean` | Caps extreme values without removing them completely |
| Positive skew | `softmax` | Gives more weight to confident agents |
| Negative skew | `median` | Provides a robust middle estimate |
| Otherwise | `mean` | Simple average works well for consistent data |

## Advanced Usage

### Custom Strategy Selection

You can override the automatic strategy selection by subclassing:

```python
from num_agents.reasoning.nodes.dynamic_expertise_flow import DynamicExpertiseFlow

class CustomExpertiseFlow(DynamicExpertiseFlow):
    def _select_optimal_strategy(self, proposition_scores_by_agent):
        # Custom logic to select strategy based on your specific needs
        # For example, select based on proposition content or agent characteristics
        
        # Analyze scores
        # ...
        
        # Return selected strategy
        return "trimmed_mean"
```

### Integration with External Systems

To integrate with external AI systems:

```python
# Convert external agent outputs to Expertise objects
external_expertises = []
for agent_output in external_agent_outputs:
    expertise = Expertise(
        name=agent_output["name"],
        domains=[Domain(name=d) for d in agent_output["domains"]],
        relations=[],  # Optional relations
        confidence=agent_output["reliability_score"]
    )
    external_expertises.append(expertise)

# Add to shared store
shared_store["expertises"] = external_expertises

# Run the flow
flow._run(shared_store)
```

## Example: Medical Diagnosis

See `examples/dynamic_expertise_flow_demo.py` for a complete example showing how to:

1. Set up a medical diagnosis scenario with multiple expert opinions
2. Create different expertise profiles (general practitioner, pulmonologist, infectious disease specialist)
3. Run the flow to determine the most likely diagnosis based on symptoms
4. Analyze the confidence scores and decisions

## Best Practices

1. **Define Clear Domains**: Each expertise should have well-defined domains with clear relevance to the propositions.

2. **Tune the Confidence Threshold**: Adjust based on your application's risk tolerance:
   - Higher threshold (e.g., 0.8+): For critical decisions where false positives are costly
   - Medium threshold (0.6-0.8): For balanced decision making
   - Lower threshold (<0.6): For exploratory reasoning where recall is more important than precision

3. **Consider Agent Diversity**: Include experts with diverse knowledge domains for more robust reasoning.

4. **Analyze Agent Disagreements**: When agents disagree significantly, examine the underlying reasons before accepting the aggregated decision.

5. **Monitor Strategy Selection**: If using `auto_select_strategy`, monitor which strategies are being selected to ensure they align with your expectations.

## Troubleshooting

### Common Issues

1. **Low Confidence Scores**:
   - Check if expertises have relevant domains for the propositions
   - Verify that relations are properly defined with appropriate weights
   - Consider adjusting the base confidence of expertises

2. **Inconsistent Decisions**:
   - Check for contradictory relations in different expertises
   - Consider using more robust aggregation strategies
   - Analyze per-agent scores to identify outliers

3. **Performance Issues**:
   - For large numbers of propositions or agents, consider batching or parallel processing
   - Cache expertise weighting results if running multiple iterations
