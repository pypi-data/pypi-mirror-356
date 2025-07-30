"""
Scheduler implementation for the Nüm Agents SDK.

This module provides the Scheduler class, which is responsible for
scheduling and executing tasks at specific times or intervals.
"""

import asyncio
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set, Union

from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus
from num_agents.scheduler.task import Task, TaskSchedule, TaskStatus


class Scheduler:
    """
    Scheduler for executing tasks at specific times or intervals.
    
    The Scheduler provides functionality for scheduling tasks to be executed
    at specific times, after delays, or at regular intervals.
    """
    
    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        """
        Initialize a new scheduler.
        
        Args:
            event_bus: Optional EventBus instance for publishing task events
        """
        self._tasks: Dict[str, Task] = {}
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._executor = ThreadPoolExecutor()
        self._lock = threading.RLock()
        self._event_bus = event_bus
        self._logger = logging.getLogger(__name__)
    
    def schedule_task(self, task: Task) -> str:
        """
        Schedule a task for execution.
        
        Args:
            task: The task to schedule
            
        Returns:
            The task ID
        """
        with self._lock:
            self._tasks[task.task_id] = task
            self._logger.debug(f"Scheduled task: {task.name} (ID: {task.task_id})")
            
            # Publish event if event bus is available
            if self._event_bus:
                event = Event(
                    event_type=EventTypes.custom("scheduler.task_scheduled"),
                    payload={"task_id": task.task_id, "task_name": task.name},
                    source="Scheduler"
                )
                self._event_bus.publish(event)
            
            return task.task_id
    
    def schedule(
        self,
        name: str,
        callback: Callable[..., Any],
        *,
        run_at: Optional[datetime] = None,
        delay: Optional[Union[int, float, timedelta]] = None,
        interval: Optional[Union[int, float, timedelta]] = None,
        cron_expression: Optional[str] = None,
        max_runs: Optional[int] = None,
        start_after: Optional[datetime] = None,
        end_after: Optional[datetime] = None,
        args: tuple = (),
        kwargs: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Schedule a function for execution.
        
        This is a convenience method that creates and schedules a Task.
        
        Args:
            name: Name of the task
            callback: Function to call when the task is executed
            run_at: Specific time to run the task once
            delay: Delay in seconds before running the task (alternative to run_at)
            interval: Time interval for recurring tasks (in seconds or as timedelta)
            cron_expression: Cron-like expression for more complex scheduling
            max_runs: Maximum number of times to run the task
            start_after: Don't start recurring task before this time
            end_after: Don't run recurring task after this time
            args: Positional arguments to pass to the callback
            kwargs: Keyword arguments to pass to the callback
            
        Returns:
            The task ID
            
        Raises:
            ValueError: If no scheduling method is specified
        """
        # Convert delay to run_at if specified
        if delay is not None:
            if isinstance(delay, (int, float)):
                delay = timedelta(seconds=delay)
            run_at = datetime.now() + delay
        
        # Convert interval to timedelta if it's a number
        if interval is not None and isinstance(interval, (int, float)):
            interval = timedelta(seconds=interval)
        
        # Create the task schedule
        schedule = TaskSchedule(
            run_at=run_at,
            interval=interval,
            cron_expression=cron_expression,
            max_runs=max_runs,
            start_after=start_after,
            end_after=end_after
        )
        
        # Create the task
        task = Task(
            name=name,
            callback=callback,
            schedule=schedule,
            args=args,
            kwargs=kwargs or {}
        )
        
        # Schedule the task
        return self.schedule_task(task)
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a scheduled task.
        
        Args:
            task_id: The ID of the task to cancel
            
        Returns:
            True if the task was cancelled, False if it wasn't found
        """
        with self._lock:
            if task_id in self._tasks:
                task = self._tasks[task_id]
                task.cancel()
                self._logger.debug(f"Cancelled task: {task.name} (ID: {task_id})")
                
                # Publish event if event bus is available
                if self._event_bus:
                    event = Event(
                        event_type=EventTypes.custom("scheduler.task_cancelled"),
                        payload={"task_id": task_id, "task_name": task.name},
                        source="Scheduler"
                    )
                    self._event_bus.publish(event)
                
                return True
            return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID.
        
        Args:
            task_id: The ID of the task to get
            
        Returns:
            The task, or None if not found
        """
        with self._lock:
            return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all scheduled tasks.
        
        Returns:
            A list of all tasks
        """
        with self._lock:
            return list(self._tasks.values())
    
    def get_pending_tasks(self) -> List[Task]:
        """
        Get all pending tasks.
        
        Returns:
            A list of pending tasks
        """
        with self._lock:
            return [task for task in self._tasks.values() 
                   if task.status == TaskStatus.PENDING]
    
    def get_due_tasks(self) -> List[Task]:
        """
        Get all tasks that are due to run.
        
        Returns:
            A list of due tasks
        """
        now = datetime.now()
        with self._lock:
            return [task for task in self._tasks.values() if task.is_due(now)]
    
    def start(self, interval: float = 1.0) -> None:
        """
        Start the scheduler.
        
        Args:
            interval: How often to check for due tasks (in seconds)
        """
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(
            target=self._run_scheduler,
            args=(interval,),
            daemon=True
        )
        self._thread.start()
        self._logger.debug("Scheduler started")
        
        # Publish event if event bus is available
        if self._event_bus:
            event = Event(
                event_type=EventTypes.custom("scheduler.started"),
                source="Scheduler"
            )
            self._event_bus.publish(event)
    
    def stop(self) -> None:
        """Stop the scheduler."""
        if not self._running:
            return
        
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)
            self._thread = None
        
        self._logger.debug("Scheduler stopped")
        
        # Publish event if event bus is available
        if self._event_bus:
            event = Event(
                event_type=EventTypes.custom("scheduler.stopped"),
                source="Scheduler"
            )
            self._event_bus.publish(event)
    
    def _run_scheduler(self, interval: float) -> None:
        """
        Run the scheduler loop.
        
        Args:
            interval: How often to check for due tasks (in seconds)
        """
        while self._running:
            try:
                self._check_and_execute_tasks()
            except Exception as e:
                self._logger.error(f"Error in scheduler loop: {e}")
            
            # Sleep for the specified interval
            time.sleep(interval)
    
    def _check_and_execute_tasks(self) -> None:
        """Check for due tasks and execute them."""
        due_tasks = self.get_due_tasks()
        
        for task in due_tasks:
            with self._lock:
                # Skip tasks that are no longer pending
                if task.status != TaskStatus.PENDING:
                    continue
                
                # Mark the task as running
                task.mark_running()
            
            # Execute the task in a separate thread
            self._executor.submit(self._execute_task, task)
    
    def _execute_task(self, task: Task) -> None:
        """
        Execute a task.
        
        Args:
            task: The task to execute
        """
        task_id = task.task_id
        task_name = task.name
        
        try:
            # Publish task started event
            if self._event_bus:
                event = Event(
                    event_type=EventTypes.custom("scheduler.task_started"),
                    payload={"task_id": task_id, "task_name": task_name},
                    source="Scheduler"
                )
                self._event_bus.publish(event)
            
            # Execute the task
            self._logger.debug(f"Executing task: {task_name} (ID: {task_id})")
            result = task.callback(*task.args, **task.kwargs)
            
            # Mark the task as completed
            with self._lock:
                task.mark_completed()
            
            # Publish task completed event
            if self._event_bus:
                event = Event(
                    event_type=EventTypes.custom("scheduler.task_completed"),
                    payload={
                        "task_id": task_id,
                        "task_name": task_name,
                        "result": result
                    },
                    source="Scheduler"
                )
                self._event_bus.publish(event)
            
            self._logger.debug(f"Task completed: {task_name} (ID: {task_id})")
            
        except Exception as e:
            # Mark the task as failed
            with self._lock:
                task.mark_failed()
            
            # Publish task failed event
            if self._event_bus:
                event = Event(
                    event_type=EventTypes.custom("scheduler.task_failed"),
                    payload={
                        "task_id": task_id,
                        "task_name": task_name,
                        "error": str(e)
                    },
                    source="Scheduler"
                )
                self._event_bus.publish(event)
            
            self._logger.error(f"Task failed: {task_name} (ID: {task_id}): {e}")
    
    async def _run_async_scheduler(self, interval: float) -> None:
        """
        Run the scheduler loop asynchronously.
        
        Args:
            interval: How often to check for due tasks (in seconds)
        """
        while self._running:
            try:
                self._check_and_execute_tasks()
            except Exception as e:
                self._logger.error(f"Error in async scheduler loop: {e}")
            
            # Sleep for the specified interval
            await asyncio.sleep(interval)
    
    async def start_async(self, interval: float = 1.0) -> None:
        """
        Start the scheduler asynchronously.
        
        Args:
            interval: How often to check for due tasks (in seconds)
        """
        if self._running:
            return
        
        self._running = True
        asyncio.create_task(self._run_async_scheduler(interval))
        self._logger.debug("Async scheduler started")
        
        # Publish event if event bus is available
        if self._event_bus:
            event = Event(
                event_type=EventTypes.custom("scheduler.started"),
                source="Scheduler"
            )
            self._event_bus.publish(event)
