"""
Tests for the utility functions in the Scheduler system.
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from num_agents.eventbus.eventbus import EventBus
from num_agents.scheduler.scheduler import Scheduler
from num_agents.scheduler.task import Task, TaskSchedule, TaskStatus
from num_agents.scheduler.utils import (
    schedule_task,
    schedule_recurring_task,
    schedule_delayed_task,
    cancel_task,
    execute_task,
    get_task_status,
    get_task_result
)


class TestSchedulerUtils(unittest.TestCase):
    """Test cases for the Scheduler utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.scheduler = Scheduler(event_bus=self.event_bus)
        self.mock_callback = Mock()
        self.mock_callback.return_value = {"result": "success"}
    
    def test_schedule_task(self):
        """Test the schedule_task utility function."""
        # Use the utility function to schedule a task
        task_id = schedule_task(
            scheduler=self.scheduler,
            name="TestTask",
            callback=self.mock_callback,
            args=(1, 2),
            kwargs={"key": "value"}
        )
        
        # Verify the task was scheduled
        self.assertIsNotNone(task_id)
        self.assertIn(task_id, self.scheduler.tasks)
        
        # Verify the task properties
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.name, "TestTask")
        self.assertEqual(task.callback, self.mock_callback)
        self.assertEqual(task.args, (1, 2))
        self.assertEqual(task.kwargs, {"key": "value"})
        self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_schedule_recurring_task(self):
        """Test the schedule_recurring_task utility function."""
        # Use the utility function to schedule a recurring task
        task_id = schedule_recurring_task(
            scheduler=self.scheduler,
            name="RecurringTask",
            callback=self.mock_callback,
            interval=60,  # 60 seconds
            max_runs=3
        )
        
        # Verify the task was scheduled
        self.assertIsNotNone(task_id)
        self.assertIn(task_id, self.scheduler.tasks)
        
        # Verify the task properties
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.name, "RecurringTask")
        self.assertEqual(task.schedule.interval, timedelta(seconds=60))
        self.assertEqual(task.schedule.max_runs, 3)
    
    def test_schedule_delayed_task(self):
        """Test the schedule_delayed_task utility function."""
        # Use the utility function to schedule a delayed task
        task_id = schedule_delayed_task(
            scheduler=self.scheduler,
            name="DelayedTask",
            callback=self.mock_callback,
            delay=60  # 60 seconds
        )
        
        # Verify the task was scheduled
        self.assertIsNotNone(task_id)
        self.assertIn(task_id, self.scheduler.tasks)
        
        # Verify the task properties
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.name, "DelayedTask")
        self.assertIsNotNone(task.schedule.start_after)
        
        # The start_after time should be approximately now + delay
        now = datetime.now()
        expected_start = now + timedelta(seconds=60)
        self.assertAlmostEqual(
            task.schedule.start_after.timestamp(),
            expected_start.timestamp(),
            delta=1  # Allow 1 second difference
        )
    
    def test_cancel_task(self):
        """Test the cancel_task utility function."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Use the utility function to cancel the task
        result = cancel_task(
            scheduler=self.scheduler,
            task_id=task_id
        )
        
        # Verify the task was canceled
        self.assertTrue(result)
        self.assertEqual(len(self.scheduler.tasks), 0)
    
    def test_cancel_nonexistent_task(self):
        """Test canceling a nonexistent task."""
        # Use the utility function to cancel a nonexistent task
        result = cancel_task(
            scheduler=self.scheduler,
            task_id="nonexistent-id"
        )
        
        # Verify the result is False
        self.assertFalse(result)
    
    def test_execute_task(self):
        """Test the execute_task utility function."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback,
            args=(1, 2),
            kwargs={"key": "value"}
        )
        
        # Use the utility function to execute the task
        result = execute_task(
            scheduler=self.scheduler,
            task_id=task_id
        )
        
        # Verify the task was executed
        self.mock_callback.assert_called_once_with(1, 2, key="value")
        self.assertEqual(result, {"result": "success"})
        
        # Verify the task state was updated
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.runs_completed, 1)
        self.assertEqual(task.last_result, {"result": "success"})
    
    def test_execute_nonexistent_task(self):
        """Test executing a nonexistent task."""
        # Use the utility function to execute a nonexistent task
        with self.assertRaises(ValueError):
            execute_task(
                scheduler=self.scheduler,
                task_id="nonexistent-id"
            )
    
    def test_get_task_status(self):
        """Test the get_task_status utility function."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Use the utility function to get the task status
        status = get_task_status(
            scheduler=self.scheduler,
            task_id=task_id
        )
        
        # Verify the status is correct
        self.assertEqual(status, TaskStatus.PENDING)
        
        # Execute the task
        self.scheduler.execute_task(task_id)
        
        # Use the utility function to get the updated task status
        status = get_task_status(
            scheduler=self.scheduler,
            task_id=task_id
        )
        
        # Verify the status is updated
        self.assertEqual(status, TaskStatus.COMPLETED)
    
    def test_get_task_status_nonexistent_task(self):
        """Test getting the status of a nonexistent task."""
        # Use the utility function to get the status of a nonexistent task
        status = get_task_status(
            scheduler=self.scheduler,
            task_id="nonexistent-id"
        )
        
        # Verify the status is None
        self.assertIsNone(status)
    
    def test_get_task_result(self):
        """Test the get_task_result utility function."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Execute the task
        self.scheduler.execute_task(task_id)
        
        # Use the utility function to get the task result
        result = get_task_result(
            scheduler=self.scheduler,
            task_id=task_id
        )
        
        # Verify the result is correct
        self.assertEqual(result, {"result": "success"})
    
    def test_get_task_result_nonexistent_task(self):
        """Test getting the result of a nonexistent task."""
        # Use the utility function to get the result of a nonexistent task
        result = get_task_result(
            scheduler=self.scheduler,
            task_id="nonexistent-id"
        )
        
        # Verify the result is None
        self.assertIsNone(result)
    
    def test_get_task_result_pending_task(self):
        """Test getting the result of a pending task."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Use the utility function to get the result of a pending task
        result = get_task_result(
            scheduler=self.scheduler,
            task_id=task_id
        )
        
        # Verify the result is None
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
