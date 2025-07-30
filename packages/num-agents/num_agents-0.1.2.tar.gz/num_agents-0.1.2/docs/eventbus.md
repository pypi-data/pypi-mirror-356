# EventBus System

The EventBus system in Nüm Agents SDK provides a publish-subscribe pattern for communication between components. This enables event-driven architecture and decoupled communication between nodes in a flow.

## Core Components

### Event

The `Event` class represents a message that can be published to the EventBus and consumed by subscribers.

```python
from num_agents.eventbus.event import Event

# Create a simple event
event = Event(
    event_type="custom.data_processed",
    payload={"result": "success", "items_processed": 42},
    metadata={"priority": "high"},
    source="DataProcessor"
)
```

### EventBus

The `EventBus` class is responsible for event publishing and subscription.

```python
from num_agents.eventbus.eventbus import EventBus
from num_agents.eventbus.event import Event

# Create an event bus
event_bus = EventBus()

# Define a handler function
def log_event(event):
    print(f"Event received: {event.event_type} from {event.source}")
    print(f"Payload: {event.payload}")

# Subscribe to events
event_bus.subscribe("custom.data_processed", log_event)
event_bus.subscribe("data.*", log_event, is_pattern=True)  # Pattern subscription

# Publish an event
event = Event(
    event_type="custom.data_processed",
    payload={"result": "success"},
    source="DataProcessor"
)
event_bus.publish(event)
```

## EventBus Nodes

The SDK provides specialized nodes for working with the EventBus in a flow:

### EventEmitterNode

Emits events to the EventBus from within a flow.

```python
from num_agents.eventbus.event_bus_node import EventEmitterNode

# Create an emitter node
emitter_node = EventEmitterNode(
    event_bus=event_bus,
    event_type="custom.data_processed",
    payload_key="processing_result",  # Will use shared.get("processing_result") as payload
    source="ProcessingFlow"
)
```

### EventListenerNode

Listens for events from the EventBus and stores them in the shared store.

```python
from num_agents.eventbus.event_bus_node import EventListenerNode

# Create a listener node
listener_node = EventListenerNode(
    event_bus=event_bus,
    event_type="custom.data_processed",
    output_key="received_event",  # Will store the event in shared.set("received_event", event)
    timeout=5.0  # Wait up to 5 seconds for an event
)
```

### EventDrivenBranchNode

Branches flow execution based on which events are received.

```python
from num_agents.eventbus.event_bus_node import EventDrivenBranchNode

# Create a branch node
branch_node = EventDrivenBranchNode(
    event_bus=event_bus,
    event_branches={
        "custom.success": success_node,
        "custom.error": error_node
    },
    default_branch=default_node,
    timeout=10.0
)
```

## Utility Functions

The SDK provides utility functions for common EventBus operations:

```python
from num_agents.eventbus.utils import publish_event, publish_flow_started_event

# Publish an event
publish_event(
    event_bus=event_bus,
    event_type="custom.notification",
    payload={"message": "Processing complete"},
    source="DataProcessor"
)

# Publish a flow started event
publish_flow_started_event(
    event_bus=event_bus,
    flow_name="DataProcessingFlow",
    flow_id="12345"
)
```

## Integration with Flow

To integrate the EventBus with a flow:

```python
from num_agents.core import Flow, Node
from num_agents.eventbus.eventbus import EventBus
from num_agents.eventbus.event_bus_node import EventEmitterNode, EventListenerNode

# Create an event bus
event_bus = EventBus()

# Create nodes
start_node = Node("Start")
process_node = Node("Process")
notify_node = EventEmitterNode(
    event_bus=event_bus,
    event_type="custom.processing_complete",
    payload_key="result"
)
end_node = Node("End")

# Create a flow
flow = Flow([start_node, process_node, notify_node, end_node])

# Execute the flow
flow.execute()
```

## Best Practices

1. **Use meaningful event types**: Create a consistent naming scheme for event types (e.g., `domain.action`).
2. **Keep payloads serializable**: Ensure event payloads can be easily serialized/deserialized.
3. **Handle exceptions in event handlers**: Prevent exceptions in one handler from affecting others.
4. **Consider event patterns**: Use pattern subscriptions for grouping related events.
5. **Document events**: Maintain documentation of all events used in your system.
