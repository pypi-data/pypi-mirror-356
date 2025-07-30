"""
Tests for the Scheduler class in the Scheduler system.
"""

import unittest
from unittest.mock import Mock, patch
import threading
import time
from datetime import datetime, timedelta

from num_agents.eventbus.eventbus import EventBus
from num_agents.scheduler.scheduler import Scheduler
from num_agents.scheduler.task import Task, TaskSchedule, TaskStatus


class TestScheduler(unittest.TestCase):
    """Test cases for the Scheduler class."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.scheduler = Scheduler(event_bus=self.event_bus)
        self.mock_callback = Mock()
        self.mock_callback.return_value = "task_result"
    
    def tearDown(self):
        """Clean up after tests."""
        if self.scheduler.is_running:
            self.scheduler.stop()
    
    def test_scheduler_creation(self):
        """Test creating a scheduler with basic properties."""
        # Verify the scheduler properties
        self.assertFalse(self.scheduler.is_running)
        self.assertEqual(len(self.scheduler.tasks), 0)
        self.assertEqual(self.scheduler.event_bus, self.event_bus)
    
    def test_schedule_task(self):
        """Test scheduling a task."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Verify the task was added to the scheduler
        self.assertEqual(len(self.scheduler.tasks), 1)
        self.assertIn(task_id, self.scheduler.tasks)
        
        # Verify the task properties
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.name, "TestTask")
        self.assertEqual(task.callback, self.mock_callback)
        self.assertEqual(task.status, TaskStatus.PENDING)
    
    def test_schedule_task_with_args_kwargs(self):
        """Test scheduling a task with args and kwargs."""
        # Schedule a task with args and kwargs
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback,
            args=(1, 2),
            kwargs={"key": "value"}
        )
        
        # Verify the task properties
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.args, (1, 2))
        self.assertEqual(task.kwargs, {"key": "value"})
    
    def test_schedule_task_with_delay(self):
        """Test scheduling a task with a delay."""
        # Schedule a task with a delay
        delay = 60  # seconds
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback,
            delay=delay
        )
        
        # Verify the task schedule
        task = self.scheduler.tasks[task_id]
        self.assertIsNotNone(task.schedule.start_after)
        
        # The start_after time should be approximately now + delay
        now = datetime.now()
        expected_start = now + timedelta(seconds=delay)
        self.assertAlmostEqual(
            task.schedule.start_after.timestamp(),
            expected_start.timestamp(),
            delta=1  # Allow 1 second difference
        )
    
    def test_schedule_task_with_interval(self):
        """Test scheduling a task with an interval."""
        # Schedule a task with an interval
        interval = 60  # seconds
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback,
            interval=interval,
            max_runs=3
        )
        
        # Verify the task schedule
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.schedule.interval, timedelta(seconds=interval))
        self.assertEqual(task.schedule.max_runs, 3)
    
    def test_get_task(self):
        """Test getting a task by ID."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Get the task
        task = self.scheduler.get_task(task_id)
        
        # Verify the task
        self.assertEqual(task.name, "TestTask")
        self.assertEqual(task.callback, self.mock_callback)
    
    def test_get_nonexistent_task(self):
        """Test getting a nonexistent task."""
        # Try to get a nonexistent task
        task = self.scheduler.get_task("nonexistent-id")
        
        # Verify the result is None
        self.assertIsNone(task)
    
    def test_cancel_task(self):
        """Test canceling a task."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Cancel the task
        result = self.scheduler.cancel_task(task_id)
        
        # Verify the task was canceled
        self.assertTrue(result)
        self.assertEqual(len(self.scheduler.tasks), 0)
    
    def test_cancel_nonexistent_task(self):
        """Test canceling a nonexistent task."""
        # Try to cancel a nonexistent task
        result = self.scheduler.cancel_task("nonexistent-id")
        
        # Verify the result is False
        self.assertFalse(result)
    
    def test_get_all_tasks(self):
        """Test getting all tasks."""
        # Schedule multiple tasks
        task_id1 = self.scheduler.schedule(
            name="TestTask1",
            callback=self.mock_callback
        )
        task_id2 = self.scheduler.schedule(
            name="TestTask2",
            callback=self.mock_callback
        )
        
        # Get all tasks
        tasks = self.scheduler.get_all_tasks()
        
        # Verify the tasks
        self.assertEqual(len(tasks), 2)
        self.assertIn(task_id1, tasks)
        self.assertIn(task_id2, tasks)
        self.assertEqual(tasks[task_id1].name, "TestTask1")
        self.assertEqual(tasks[task_id2].name, "TestTask2")
    
    @patch('time.sleep')
    def test_start_stop(self, mock_sleep):
        """Test starting and stopping the scheduler."""
        # Mock time.sleep to avoid actual sleeping
        mock_sleep.return_value = None
        
        # Start the scheduler
        self.scheduler.start()
        
        # Verify the scheduler is running
        self.assertTrue(self.scheduler.is_running)
        self.assertIsNotNone(self.scheduler._thread)
        
        # Stop the scheduler
        self.scheduler.stop()
        
        # Verify the scheduler is stopped
        self.assertFalse(self.scheduler.is_running)
        self.assertIsNone(self.scheduler._thread)
    
    @patch('time.sleep')
    def test_run_due_tasks(self, mock_sleep):
        """Test running due tasks."""
        # Mock time.sleep to avoid actual sleeping
        mock_sleep.return_value = None
        
        # Schedule a task that is due immediately
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Run due tasks
        self.scheduler._run_due_tasks()
        
        # Verify the task was executed
        self.mock_callback.assert_called_once()
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.runs_completed, 1)
        self.assertEqual(task.last_result, "task_result")
    
    @patch('time.sleep')
    def test_run_recurring_task(self, mock_sleep):
        """Test running a recurring task."""
        # Mock time.sleep to avoid actual sleeping
        mock_sleep.return_value = None
        
        # Schedule a recurring task
        task_id = self.scheduler.schedule(
            name="RecurringTask",
            callback=self.mock_callback,
            interval=1,  # 1 second
            max_runs=2
        )
        
        # Start the scheduler
        self.scheduler.start()
        
        # Wait for the task to run twice
        # In a real test, we would use time.sleep, but we've mocked it
        # So we'll manually run the due tasks twice
        self.scheduler._run_due_tasks()
        
        # Simulate time passing
        task = self.scheduler.tasks[task_id]
        task.last_run = datetime.now() - timedelta(seconds=2)
        
        self.scheduler._run_due_tasks()
        
        # Stop the scheduler
        self.scheduler.stop()
        
        # Verify the task was executed twice
        self.assertEqual(self.mock_callback.call_count, 2)
        self.assertEqual(task.runs_completed, 2)
    
    def test_execute_task(self):
        """Test executing a task directly."""
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback,
            args=(1, 2),
            kwargs={"key": "value"}
        )
        
        # Execute the task directly
        result = self.scheduler.execute_task(task_id)
        
        # Verify the task was executed
        self.mock_callback.assert_called_once_with(1, 2, key="value")
        self.assertEqual(result, "task_result")
        
        # Verify the task state was updated
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.runs_completed, 1)
        self.assertEqual(task.last_result, "task_result")
    
    def test_execute_nonexistent_task(self):
        """Test executing a nonexistent task."""
        # Try to execute a nonexistent task
        with self.assertRaises(ValueError):
            self.scheduler.execute_task("nonexistent-id")
    
    def test_clear_tasks(self):
        """Test clearing all tasks."""
        # Schedule multiple tasks
        self.scheduler.schedule(
            name="TestTask1",
            callback=self.mock_callback
        )
        self.scheduler.schedule(
            name="TestTask2",
            callback=self.mock_callback
        )
        
        # Clear all tasks
        self.scheduler.clear_tasks()
        
        # Verify all tasks were removed
        self.assertEqual(len(self.scheduler.tasks), 0)
    
    @patch('time.sleep')
    def test_scheduler_with_event_bus(self, mock_sleep):
        """Test scheduler integration with EventBus."""
        # Mock time.sleep to avoid actual sleeping
        mock_sleep.return_value = None
        
        # Create a mock handler for task events
        mock_handler = Mock()
        self.event_bus.subscribe("task.*", mock_handler, is_pattern=True)
        
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Start the scheduler
        self.scheduler.start()
        
        # Run due tasks
        self.scheduler._run_due_tasks()
        
        # Stop the scheduler
        self.scheduler.stop()
        
        # Verify task events were published
        self.assertGreaterEqual(mock_handler.call_count, 2)  # At least started and completed events


if __name__ == "__main__":
    unittest.main()
