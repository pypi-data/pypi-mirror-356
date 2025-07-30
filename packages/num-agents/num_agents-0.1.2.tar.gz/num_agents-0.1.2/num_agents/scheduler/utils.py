"""
Utility functions for working with the Scheduler.

This module provides helper functions for common Scheduler operations.
"""

from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Union

from num_agents.scheduler.scheduler import Scheduler
from num_agents.scheduler.task import Task, TaskSchedule, TaskStatus


def schedule_one_time_task(
    scheduler: Scheduler,
    name: str,
    callback: Callable[..., Any],
    run_at: Optional[datetime] = None,
    delay: Optional[Union[int, float, timedelta]] = None,
    args: tuple = (),
    kwargs: Optional[Dict[str, Any]] = None
) -> str:
    """
    Schedule a one-time task.
    
    Args:
        scheduler: The Scheduler to schedule the task with
        name: Name of the task
        callback: Function to call when the task is executed
        run_at: Specific time to run the task
        delay: Delay in seconds before running the task (alternative to run_at)
        args: Positional arguments to pass to the callback
        kwargs: Keyword arguments to pass to the callback
        
    Returns:
        The task ID
        
    Raises:
        ValueError: If neither run_at nor delay is specified
    """
    if run_at is None and delay is None:
        raise ValueError("Either run_at or delay must be specified")
    
    return scheduler.schedule(
        name=name,
        callback=callback,
        run_at=run_at,
        delay=delay,
        args=args,
        kwargs=kwargs
    )


def schedule_recurring_task(
    scheduler: Scheduler,
    name: str,
    callback: Callable[..., Any],
    interval: Union[int, float, timedelta],
    max_runs: Optional[int] = None,
    start_after: Optional[datetime] = None,
    end_after: Optional[datetime] = None,
    args: tuple = (),
    kwargs: Optional[Dict[str, Any]] = None
) -> str:
    """
    Schedule a recurring task.
    
    Args:
        scheduler: The Scheduler to schedule the task with
        name: Name of the task
        callback: Function to call when the task is executed
        interval: Time interval for recurring tasks (in seconds or as timedelta)
        max_runs: Maximum number of times to run the task
        start_after: Don't start recurring task before this time
        end_after: Don't run recurring task after this time
        args: Positional arguments to pass to the callback
        kwargs: Keyword arguments to pass to the callback
        
    Returns:
        The task ID
    """
    return scheduler.schedule(
        name=name,
        callback=callback,
        interval=interval,
        max_runs=max_runs,
        start_after=start_after,
        end_after=end_after,
        args=args,
        kwargs=kwargs
    )


def schedule_cron_task(
    scheduler: Scheduler,
    name: str,
    callback: Callable[..., Any],
    cron_expression: str,
    max_runs: Optional[int] = None,
    start_after: Optional[datetime] = None,
    end_after: Optional[datetime] = None,
    args: tuple = (),
    kwargs: Optional[Dict[str, Any]] = None
) -> str:
    """
    Schedule a task using a cron expression.
    
    Args:
        scheduler: The Scheduler to schedule the task with
        name: Name of the task
        callback: Function to call when the task is executed
        cron_expression: Cron-like expression for scheduling
        max_runs: Maximum number of times to run the task
        start_after: Don't start recurring task before this time
        end_after: Don't run recurring task after this time
        args: Positional arguments to pass to the callback
        kwargs: Keyword arguments to pass to the callback
        
    Returns:
        The task ID
    """
    return scheduler.schedule(
        name=name,
        callback=callback,
        cron_expression=cron_expression,
        max_runs=max_runs,
        start_after=start_after,
        end_after=end_after,
        args=args,
        kwargs=kwargs
    )


def get_task_info(scheduler: Scheduler, task_id: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a task.
    
    Args:
        scheduler: The Scheduler to get the task from
        task_id: The ID of the task
        
    Returns:
        A dictionary with task information, or None if the task wasn't found
    """
    task = scheduler.get_task(task_id)
    if task:
        return task.to_dict()
    return None


def get_all_tasks_info(scheduler: Scheduler) -> List[Dict[str, Any]]:
    """
    Get information about all tasks.
    
    Args:
        scheduler: The Scheduler to get tasks from
        
    Returns:
        A list of dictionaries with task information
    """
    return [task.to_dict() for task in scheduler.get_all_tasks()]


def get_pending_tasks_info(scheduler: Scheduler) -> List[Dict[str, Any]]:
    """
    Get information about pending tasks.
    
    Args:
        scheduler: The Scheduler to get tasks from
        
    Returns:
        A list of dictionaries with task information
    """
    return [task.to_dict() for task in scheduler.get_pending_tasks()]


def get_due_tasks_info(scheduler: Scheduler) -> List[Dict[str, Any]]:
    """
    Get information about due tasks.
    
    Args:
        scheduler: The Scheduler to get tasks from
        
    Returns:
        A list of dictionaries with task information
    """
    return [task.to_dict() for task in scheduler.get_due_tasks()]


def cancel_all_tasks(scheduler: Scheduler) -> int:
    """
    Cancel all scheduled tasks.
    
    Args:
        scheduler: The Scheduler to cancel tasks from
        
    Returns:
        The number of tasks cancelled
    """
    tasks = scheduler.get_all_tasks()
    count = 0
    
    for task in tasks:
        if scheduler.cancel_task(task.task_id):
            count += 1
    
    return count
