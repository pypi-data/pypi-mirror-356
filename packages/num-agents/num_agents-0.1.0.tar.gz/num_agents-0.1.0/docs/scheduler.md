# Scheduler System

The Scheduler system in Nüm Agents SDK provides functionality for scheduling tasks to be executed at specific times, after delays, or at regular intervals. This enables time-based and recurring operations within your agents.

## Core Components

### Task and TaskSchedule

The `Task` class represents a unit of work that can be scheduled for execution, while `TaskSchedule` defines when and how often a task should be executed.

```python
from num_agents.scheduler.task import Task, TaskSchedule
from datetime import datetime, timedelta

# Create a schedule for a task
schedule = TaskSchedule(
    interval=timedelta(minutes=5),  # Run every 5 minutes
    max_runs=10,  # Run at most 10 times
    start_after=datetime.now() + timedelta(minutes=1)  # Start after 1 minute
)

# Create a task (normally you wouldn't create this directly)
def my_task_function(arg1, arg2):
    print(f"Task executed with {arg1} and {arg2}")

task = Task(
    name="MyPeriodicTask",
    callback=my_task_function,
    schedule=schedule,
    args=("value1", "value2")
)
```

### Scheduler

The `Scheduler` class is responsible for scheduling and executing tasks.

```python
from num_agents.scheduler.scheduler import Scheduler
from num_agents.eventbus.eventbus import EventBus

# Create an event bus (optional, for task events)
event_bus = EventBus()

# Create a scheduler
scheduler = Scheduler(event_bus=event_bus)

# Schedule a one-time task
task_id = scheduler.schedule(
    name="OneTimeTask",
    callback=lambda: print("One-time task executed"),
    delay=30  # Run after 30 seconds
)

# Schedule a recurring task
recurring_task_id = scheduler.schedule(
    name="RecurringTask",
    callback=lambda x: print(f"Recurring task executed with {x}"),
    interval=60,  # Run every 60 seconds
    max_runs=5,   # Run at most 5 times
    args=("parameter",)
)

# Start the scheduler
scheduler.start()

# Later, cancel a task
scheduler.cancel_task(task_id)

# Stop the scheduler when done
scheduler.stop()
```

## Scheduler Nodes

The SDK provides specialized nodes for working with the Scheduler in a flow:

### ScheduleTaskNode

Schedules a task from within a flow.

```python
from num_agents.scheduler.scheduler_node import ScheduleTaskNode

# Create a schedule task node
schedule_node = ScheduleTaskNode(
    scheduler=scheduler,
    task_name="DataProcessingTask",
    callback=process_data_function,
    delay=60,  # Run after 60 seconds
    task_id_output_key="task_id"  # Will store the task ID in shared.set("task_id", id)
)
```

### CancelTaskNode

Cancels a previously scheduled task.

```python
from num_agents.scheduler.scheduler_node import CancelTaskNode

# Create a cancel task node
cancel_node = CancelTaskNode(
    scheduler=scheduler,
    task_id_key="task_id"  # Will use shared.get("task_id") as the task ID to cancel
)
```

### WaitForTaskNode

Waits for a scheduled task to complete.

```python
from num_agents.scheduler.scheduler_node import WaitForTaskNode

# Create a wait for task node
wait_node = WaitForTaskNode(
    scheduler=scheduler,
    task_id_key="task_id",  # Will use shared.get("task_id") as the task ID to wait for
    result_key="task_result",  # Will store the task result in shared.set("task_result", result)
    timeout=300  # Wait up to 300 seconds for the task to complete
)
```

### ScheduledFlowNode

Schedules a sub-flow to be executed on a schedule.

```python
from num_agents.scheduler.scheduler_node import ScheduledFlowNode

# Create a scheduled flow node
scheduled_flow_node = ScheduledFlowNode(
    scheduler=scheduler,
    sub_flow_nodes=[node1, node2, node3],  # Nodes to execute as a sub-flow
    interval=timedelta(hours=1),  # Run every hour
    task_id_output_key="scheduled_flow_id"
)
```

## Utility Functions

The SDK provides utility functions for common Scheduler operations:

```python
from num_agents.scheduler.utils import (
    schedule_one_time_task,
    schedule_recurring_task,
    get_task_info,
    cancel_all_tasks
)

# Schedule a one-time task
task_id = schedule_one_time_task(
    scheduler=scheduler,
    name="DataCleanup",
    callback=cleanup_function,
    delay=300  # Run after 5 minutes
)

# Schedule a recurring task
recurring_id = schedule_recurring_task(
    scheduler=scheduler,
    name="DataSync",
    callback=sync_function,
    interval=timedelta(hours=1),  # Run every hour
    max_runs=24  # Run for 24 hours
)

# Get information about a task
task_info = get_task_info(scheduler, task_id)
print(f"Task status: {task_info['status']}")

# Cancel all tasks
num_cancelled = cancel_all_tasks(scheduler)
print(f"Cancelled {num_cancelled} tasks")
```

## Integration with Flow

To integrate the Scheduler with a flow:

```python
from num_agents.core import Flow, Node
from num_agents.scheduler.scheduler import Scheduler
from num_agents.scheduler.scheduler_node import ScheduleTaskNode, WaitForTaskNode

# Create a scheduler
scheduler = Scheduler()

# Start the scheduler
scheduler.start()

# Define a task function
def process_data(data):
    # Process the data
    return {"processed": True, "result": data * 2}

# Create nodes
start_node = Node("Start")
schedule_node = ScheduleTaskNode(
    scheduler=scheduler,
    task_name="ProcessData",
    callback=process_data,
    delay=10,
    args_key="input_data",
    task_id_output_key="processing_task_id"
)
wait_node = WaitForTaskNode(
    scheduler=scheduler,
    task_id_key="processing_task_id",
    result_key="processing_result"
)
end_node = Node("End")

# Create a flow
flow = Flow([start_node, schedule_node, wait_node, end_node])

# Set up input data
flow.shared.set("input_data", (42,))

# Execute the flow
flow.execute()

# Stop the scheduler when done
scheduler.stop()
```

## Best Practices

1. **Use descriptive task names**: Choose clear, descriptive names for your tasks.
2. **Handle task failures**: Implement proper error handling in your task callbacks.
3. **Set appropriate intervals**: Choose intervals that balance responsiveness with resource usage.
4. **Clean up tasks**: Cancel tasks that are no longer needed to free up resources.
5. **Use timeouts**: Set appropriate timeouts when waiting for tasks to complete.
6. **Consider persistence**: For critical tasks, implement a persistence mechanism to survive restarts.
