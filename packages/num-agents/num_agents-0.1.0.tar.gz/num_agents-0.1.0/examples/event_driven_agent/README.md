# Event-Driven Agent Example

This example demonstrates how to use the EventBus and Scheduler components of the Nüm Agents SDK to create an event-driven agent with scheduled task capabilities.

## Overview

The Event-Driven Agent showcases:

1. **Event-Based Communication**: Using the EventBus to enable decoupled communication between nodes
2. **Task Scheduling**: Using the Scheduler to execute tasks at specific times or intervals
3. **Flow Control**: Using events to dynamically control the flow of execution
4. **Integration Patterns**: Demonstrating how to integrate EventBus and Scheduler with other components

## Architecture

The agent consists of the following components:

- **EventBus**: Central event dispatcher for publishing and subscribing to events
- **Scheduler**: Task scheduler for executing tasks at specific times or intervals
- **Flow**: Main flow definition that orchestrates the nodes
- **Nodes**:
  - `UserInputNode`: Handles user input and determines request type
  - `DataProcessorNode`: Processes data using scheduled tasks
  - `NotificationNode`: Sends notifications and publishes events
  - `LLMNode`: Simulates LLM interactions for generating responses
  - Event-related nodes (`EventEmitterNode`, `EventListenerNode`, `EventDrivenBranchNode`)
  - Scheduler-related nodes (`ScheduleTaskNode`, `WaitForTaskNode`)

## Flow Diagram

```
UserInputNode → UserInputEventNode → BranchNode
                                      │
                                      ├─── DataProcessorNode → ScheduleProcessingNode → WaitForProcessingNode → DataProcessedEventNode → LLMNode
                                      │                                                                                                    │
                                      └─── NotificationNode ──────────────────────────────────────────────────────────────────────────────┘
                                                                                                                                          │
                                                                                                                                          v
                                                                                                                          NotificationListenerNode
                                                                                                                                          │
                                                                                                                                          v
                                                                                                                                    UserInputNode
```

## Event Types

The agent uses the following event types:

- `user.input`: Published when user input is received
- `request.process`: Published when the user requests data processing
- `request.notify`: Published when the user requests a notification
- `data.processed`: Published when data processing is complete
- `system.notification`: Published when a notification is sent

## How to Run

1. Make sure you have installed the Nüm Agents SDK
2. Navigate to the example directory:
   ```
   cd examples/event_driven_agent
   ```
3. Run the agent:
   ```
   python main.py
   ```

## Example Interactions

Here are some example interactions to try:

1. **Data Processing**:
   ```
   What would you like to do? process this text and analyze it
   ```

2. **Notification**:
   ```
   What would you like to do? remind me to check my emails
   ```

3. **General Assistance**:
   ```
   What would you like to do? help
   ```

## Extending the Example

You can extend this example in several ways:

1. **Add Persistence**: Implement persistence for the EventBus and Scheduler to survive restarts
2. **Add More Event Types**: Define additional event types for more complex interactions
3. **Integrate with External Services**: Connect the agent to external APIs or services
4. **Implement Real LLM Integration**: Replace the simulated LLM with a real language model API
5. **Add Web Interface**: Create a web interface for interacting with the agent

## Key Concepts

### Event-Driven Architecture

Event-driven architecture allows components to communicate through events, reducing coupling and enabling more flexible and scalable systems. In this example:

- The `EventBus` serves as the central event dispatcher
- Nodes can publish events and subscribe to events
- Events can trigger different execution paths in the flow

### Task Scheduling

Task scheduling allows the agent to perform actions at specific times or intervals. In this example:

- The `Scheduler` manages scheduled tasks
- Tasks can be one-time or recurring
- Scheduled tasks can trigger node execution or specific actions

### Flow Control

The combination of events and scheduled tasks enables sophisticated flow control:

- Events can trigger different branches in the flow
- Scheduled tasks can pause and resume flow execution
- Events can be used to synchronize parallel flows

## Related Documentation

For more information, see:

- [EventBus Documentation](/docs/eventbus.md)
- [Scheduler Documentation](/docs/scheduler.md)
- [Nüm Agents SDK Documentation](/docs/README.md)
