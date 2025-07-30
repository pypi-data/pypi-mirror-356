"""
Task definitions for the Nüm Agents Scheduler.

This module provides the base Task class and related utilities for the scheduler system.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable, Dict, Optional, Union
import uuid


class TaskStatus(Enum):
    """Status of a scheduled task."""
    
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class TaskSchedule:
    """
    Schedule configuration for a task.
    
    This class defines when and how often a task should be executed.
    """
    
    # One-time execution
    run_at: Optional[datetime] = None
    """Specific time to run the task once."""
    
    # Recurring execution
    interval: Optional[timedelta] = None
    """Time interval for recurring tasks."""
    
    cron_expression: Optional[str] = None
    """Cron-like expression for more complex scheduling."""
    
    max_runs: Optional[int] = None
    """Maximum number of times to run the task (None for unlimited)."""
    
    start_after: Optional[datetime] = None
    """Don't start recurring task before this time."""
    
    end_after: Optional[datetime] = None
    """Don't run recurring task after this time."""
    
    def __post_init__(self) -> None:
        """Validate the schedule configuration."""
        # Ensure at least one scheduling method is specified
        if not any([self.run_at, self.interval, self.cron_expression]):
            raise ValueError(
                "At least one scheduling method must be specified: "
                "run_at, interval, or cron_expression"
            )
        
        # Validate that interval is positive
        if self.interval is not None and self.interval.total_seconds() <= 0:
            raise ValueError("Interval must be positive")
        
        # Validate max_runs is positive if specified
        if self.max_runs is not None and self.max_runs <= 0:
            raise ValueError("max_runs must be positive")


@dataclass
class Task:
    """
    Base class for all scheduled tasks in the Nüm Agents SDK.
    
    A Task represents a unit of work that can be scheduled for execution
    at specific times or intervals.
    """
    
    name: str
    """Name of the task."""
    
    callback: Callable[..., Any]
    """Function to call when the task is executed."""
    
    schedule: TaskSchedule
    """When to execute the task."""
    
    args: tuple = field(default_factory=tuple)
    """Positional arguments to pass to the callback."""
    
    kwargs: Dict[str, Any] = field(default_factory=dict)
    """Keyword arguments to pass to the callback."""
    
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    """Unique identifier for the task."""
    
    status: TaskStatus = field(default=TaskStatus.PENDING)
    """Current status of the task."""
    
    created_at: datetime = field(default_factory=datetime.now)
    """When the task was created."""
    
    last_run: Optional[datetime] = None
    """When the task was last executed."""
    
    next_run: Optional[datetime] = None
    """When the task is scheduled to run next."""
    
    run_count: int = 0
    """Number of times the task has been executed."""
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    """Additional metadata for the task."""
    
    def __post_init__(self) -> None:
        """Initialize the task after creation."""
        # Calculate the next run time
        self._calculate_next_run()
    
    def _calculate_next_run(self) -> None:
        """Calculate when the task should run next."""
        now = datetime.now()
        
        if self.schedule.run_at:
            # One-time task
            self.next_run = self.schedule.run_at
        elif self.schedule.interval:
            # Recurring task with interval
            if self.last_run:
                # Calculate from last run
                self.next_run = self.last_run + self.schedule.interval
            else:
                # First run: either now or after start_after
                if self.schedule.start_after and self.schedule.start_after > now:
                    self.next_run = self.schedule.start_after
                else:
                    self.next_run = now
        elif self.schedule.cron_expression:
            # Cron-based scheduling would be implemented here
            # This requires a cron parser library
            self.next_run = now  # Placeholder
        
        # Check if we've reached max_runs
        if (self.schedule.max_runs is not None and 
                self.run_count >= self.schedule.max_runs):
            self.next_run = None
            self.status = TaskStatus.COMPLETED
        
        # Check if we've passed end_after
        if (self.schedule.end_after is not None and 
                now > self.schedule.end_after):
            self.next_run = None
            self.status = TaskStatus.COMPLETED
    
    def mark_running(self) -> None:
        """Mark the task as running."""
        self.status = TaskStatus.RUNNING
    
    def mark_completed(self) -> None:
        """Mark the task as completed for this run."""
        self.last_run = datetime.now()
        self.run_count += 1
        
        # Check if this was the last run
        if (self.schedule.max_runs is not None and 
                self.run_count >= self.schedule.max_runs):
            self.status = TaskStatus.COMPLETED
            self.next_run = None
        else:
            self.status = TaskStatus.PENDING
            self._calculate_next_run()
    
    def mark_failed(self) -> None:
        """Mark the task as failed for this run."""
        self.last_run = datetime.now()
        self.status = TaskStatus.FAILED
        
        # Still calculate next run for recurring tasks
        if self.schedule.interval or self.schedule.cron_expression:
            self.status = TaskStatus.PENDING
            self._calculate_next_run()
    
    def cancel(self) -> None:
        """Cancel the task."""
        self.status = TaskStatus.CANCELLED
        self.next_run = None
    
    def is_due(self, current_time: Optional[datetime] = None) -> bool:
        """
        Check if the task is due to run.
        
        Args:
            current_time: The current time to check against (defaults to now)
            
        Returns:
            True if the task is due to run, False otherwise
        """
        if self.status != TaskStatus.PENDING or self.next_run is None:
            return False
        
        current_time = current_time or datetime.now()
        return current_time >= self.next_run
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the task to a dictionary representation.
        
        Returns:
            Dictionary representation of the task
        """
        return {
            "task_id": self.task_id,
            "name": self.name,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "last_run": self.last_run.isoformat() if self.last_run else None,
            "next_run": self.next_run.isoformat() if self.next_run else None,
            "run_count": self.run_count,
            "metadata": self.metadata,
            # Schedule info
            "schedule": {
                "run_at": self.schedule.run_at.isoformat() if self.schedule.run_at else None,
                "interval": self.schedule.interval.total_seconds() if self.schedule.interval else None,
                "cron_expression": self.schedule.cron_expression,
                "max_runs": self.schedule.max_runs,
                "start_after": self.schedule.start_after.isoformat() if self.schedule.start_after else None,
                "end_after": self.schedule.end_after.isoformat() if self.schedule.end_after else None,
            }
        }
