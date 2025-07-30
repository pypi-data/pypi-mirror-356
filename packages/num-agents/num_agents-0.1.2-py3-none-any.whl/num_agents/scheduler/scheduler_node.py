"""
Scheduler node implementation for the Nüm Agents SDK.

This module provides node classes for interacting with the Scheduler
within a flow.
"""

from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union

from num_agents.core import Node, SharedStore
from num_agents.scheduler.scheduler import Scheduler
from num_agents.scheduler.task import Task, TaskSchedule, TaskStatus


class ScheduleTaskNode(Node):
    """
    Node for scheduling tasks with the Scheduler.
    
    This node allows flows to schedule tasks to be executed at specific
    times or intervals.
    """
    
    def __init__(
        self, 
        scheduler: Scheduler,
        task_name: str,
        callback: Callable[..., Any],
        name: Optional[str] = None,
        run_at: Optional[Union[datetime, str]] = None,
        delay: Optional[Union[int, float, timedelta]] = None,
        interval: Optional[Union[int, float, timedelta]] = None,
        cron_expression: Optional[str] = None,
        max_runs: Optional[int] = None,
        start_after: Optional[Union[datetime, str]] = None,
        end_after: Optional[Union[datetime, str]] = None,
        args_key: Optional[str] = None,
        kwargs_key: Optional[str] = None,
        task_id_output_key: Optional[str] = None
    ) -> None:
        """
        Initialize a schedule task node.
        
        Args:
            scheduler: The Scheduler to schedule tasks with
            task_name: Name of the task to schedule
            callback: Function to call when the task is executed
            name: Optional name for the node
            run_at: Specific time to run the task once
            delay: Delay in seconds before running the task (alternative to run_at)
            interval: Time interval for recurring tasks (in seconds or as timedelta)
            cron_expression: Cron-like expression for more complex scheduling
            max_runs: Maximum number of times to run the task
            start_after: Don't start recurring task before this time
            end_after: Don't run recurring task after this time
            args_key: Optional key in the shared store for task arguments
            kwargs_key: Optional key in the shared store for task keyword arguments
            task_id_output_key: Optional key in the shared store to store the task ID
        """
        super().__init__(name or f"ScheduleTask({task_name})")
        self.scheduler = scheduler
        self.task_name = task_name
        self.callback = callback
        self.run_at = run_at
        self.delay = delay
        self.interval = interval
        self.cron_expression = cron_expression
        self.max_runs = max_runs
        self.start_after = start_after
        self.end_after = end_after
        self.args_key = args_key
        self.kwargs_key = kwargs_key
        self.task_id_output_key = task_id_output_key
        
        # Convert string datetime to datetime objects if needed
        if isinstance(self.run_at, str):
            self.run_at = datetime.fromisoformat(self.run_at)
        if isinstance(self.start_after, str):
            self.start_after = datetime.fromisoformat(self.start_after)
        if isinstance(self.end_after, str):
            self.end_after = datetime.fromisoformat(self.end_after)
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node schedules a task with the Scheduler.
        
        Args:
            shared: The shared store for accessing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Get task arguments from shared store if keys are provided
        args = shared.get(self.args_key, ()) if self.args_key else ()
        kwargs = shared.get(self.kwargs_key, {}) if self.kwargs_key else {}
        
        # Schedule the task
        task_id = self.scheduler.schedule(
            name=self.task_name,
            callback=self.callback,
            run_at=self.run_at,
            delay=self.delay,
            interval=self.interval,
            cron_expression=self.cron_expression,
            max_runs=self.max_runs,
            start_after=self.start_after,
            end_after=self.end_after,
            args=args,
            kwargs=kwargs
        )
        
        # Store the task ID in the shared store if output key is provided
        if self.task_id_output_key:
            shared.set(self.task_id_output_key, task_id)
        
        return {
            "task_id": task_id,
            "task_name": self.task_name,
            "scheduled": True
        }


class CancelTaskNode(Node):
    """
    Node for cancelling scheduled tasks.
    
    This node allows flows to cancel tasks that were previously scheduled
    with the Scheduler.
    """
    
    def __init__(
        self, 
        scheduler: Scheduler,
        task_id_key: str,
        name: Optional[str] = None
    ) -> None:
        """
        Initialize a cancel task node.
        
        Args:
            scheduler: The Scheduler to cancel tasks with
            task_id_key: Key in the shared store containing the task ID to cancel
            name: Optional name for the node
        """
        super().__init__(name or "CancelTask")
        self.scheduler = scheduler
        self.task_id_key = task_id_key
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node cancels a scheduled task.
        
        Args:
            shared: The shared store for accessing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Get the task ID from the shared store
        task_id = shared.get(self.task_id_key)
        
        if not task_id:
            return {
                "cancelled": False,
                "error": f"Task ID not found in shared store at key: {self.task_id_key}"
            }
        
        # Cancel the task
        cancelled = self.scheduler.cancel_task(task_id)
        
        return {
            "task_id": task_id,
            "cancelled": cancelled
        }


class WaitForTaskNode(Node):
    """
    Node for waiting for a scheduled task to complete.
    
    This node allows flows to pause execution until a scheduled task
    has completed.
    """
    
    def __init__(
        self, 
        scheduler: Scheduler,
        task_id_key: str,
        result_key: Optional[str] = None,
        name: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> None:
        """
        Initialize a wait for task node.
        
        Args:
            scheduler: The Scheduler to check task status with
            task_id_key: Key in the shared store containing the task ID to wait for
            result_key: Optional key in the shared store to store the task result
            name: Optional name for the node
            timeout: Optional timeout in seconds to wait for the task
        """
        super().__init__(name or "WaitForTask")
        self.scheduler = scheduler
        self.task_id_key = task_id_key
        self.result_key = result_key
        self.timeout = timeout
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node waits for a scheduled task to complete.
        
        Args:
            shared: The shared store for accessing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        import time
        
        # Get the task ID from the shared store
        task_id = shared.get(self.task_id_key)
        
        if not task_id:
            return {
                "completed": False,
                "error": f"Task ID not found in shared store at key: {self.task_id_key}"
            }
        
        # Wait for the task to complete
        start_time = time.time()
        while True:
            # Check if we've timed out
            if self.timeout and time.time() - start_time > self.timeout:
                return {"completed": False, "timed_out": True}
            
            # Get the task
            task = self.scheduler.get_task(task_id)
            
            if not task:
                return {
                    "completed": False,
                    "error": f"Task not found with ID: {task_id}"
                }
            
            # Check if the task has completed
            if task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
                # Store the task result in the shared store if output key is provided
                if self.result_key and hasattr(task, "result"):
                    shared.set(self.result_key, task.result)
                
                return {
                    "task_id": task_id,
                    "completed": task.status == TaskStatus.COMPLETED,
                    "status": task.status.value,
                    "run_count": task.run_count
                }
            
            # Sleep for a short time before checking again
            time.sleep(0.1)


class ScheduledFlowNode(Node):
    """
    Node for executing a sub-flow on a schedule.
    
    This node allows flows to schedule the execution of a sub-flow
    at specific times or intervals.
    """
    
    def __init__(
        self, 
        scheduler: Scheduler,
        sub_flow_nodes: List[Node],
        name: Optional[str] = None,
        run_at: Optional[Union[datetime, str]] = None,
        delay: Optional[Union[int, float, timedelta]] = None,
        interval: Optional[Union[int, float, timedelta]] = None,
        cron_expression: Optional[str] = None,
        max_runs: Optional[int] = None,
        start_after: Optional[Union[datetime, str]] = None,
        end_after: Optional[Union[datetime, str]] = None,
        task_id_output_key: Optional[str] = None
    ) -> None:
        """
        Initialize a scheduled flow node.
        
        Args:
            scheduler: The Scheduler to schedule tasks with
            sub_flow_nodes: List of nodes to execute as a sub-flow
            name: Optional name for the node
            run_at: Specific time to run the sub-flow once
            delay: Delay in seconds before running the sub-flow (alternative to run_at)
            interval: Time interval for recurring sub-flow execution (in seconds or as timedelta)
            cron_expression: Cron-like expression for more complex scheduling
            max_runs: Maximum number of times to run the sub-flow
            start_after: Don't start recurring sub-flow before this time
            end_after: Don't run recurring sub-flow after this time
            task_id_output_key: Optional key in the shared store to store the task ID
        """
        super().__init__(name or "ScheduledFlow")
        self.scheduler = scheduler
        self.sub_flow_nodes = sub_flow_nodes
        self.run_at = run_at
        self.delay = delay
        self.interval = interval
        self.cron_expression = cron_expression
        self.max_runs = max_runs
        self.start_after = start_after
        self.end_after = end_after
        self.task_id_output_key = task_id_output_key
        
        # Convert string datetime to datetime objects if needed
        if isinstance(self.run_at, str):
            self.run_at = datetime.fromisoformat(self.run_at)
        if isinstance(self.start_after, str):
            self.start_after = datetime.fromisoformat(self.start_after)
        if isinstance(self.end_after, str):
            self.end_after = datetime.fromisoformat(self.end_after)
    
    def _execute_sub_flow(self, shared_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the sub-flow.
        
        Args:
            shared_data: Data to initialize the sub-flow's shared store with
            
        Returns:
            Results of the sub-flow execution
        """
        from num_agents.core import Flow, SharedStore
        
        # Create a new flow with the sub-flow nodes
        sub_flow = Flow(self.sub_flow_nodes)
        
        # Initialize the sub-flow's shared store with the provided data
        for key, value in shared_data.items():
            sub_flow.shared.set(key, value)
        
        # Execute the sub-flow
        return sub_flow.execute()
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node schedules a sub-flow to be executed on a schedule.
        
        Args:
            shared: The shared store for accessing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Create a copy of the shared store data to pass to the sub-flow
        shared_data = {key: shared.get(key) for key in shared.keys()}
        
        # Schedule the sub-flow execution
        task_id = self.scheduler.schedule(
            name=f"SubFlow({self.name})",
            callback=self._execute_sub_flow,
            run_at=self.run_at,
            delay=self.delay,
            interval=self.interval,
            cron_expression=self.cron_expression,
            max_runs=self.max_runs,
            start_after=self.start_after,
            end_after=self.end_after,
            args=(shared_data,)
        )
        
        # Store the task ID in the shared store if output key is provided
        if self.task_id_output_key:
            shared.set(self.task_id_output_key, task_id)
        
        return {
            "task_id": task_id,
            "scheduled": True,
            "sub_flow_node_count": len(self.sub_flow_nodes)
        }
