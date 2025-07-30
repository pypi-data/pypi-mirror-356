"""
Tests for the Task and TaskSchedule classes in the Scheduler system.
"""

import unittest
from unittest.mock import Mock
from datetime import datetime, timedelta

from num_agents.scheduler.task import Task, TaskSchedule, TaskStatus


class TestTaskSchedule(unittest.TestCase):
    """Test cases for the TaskSchedule class."""

    def test_one_time_schedule(self):
        """Test creating a one-time schedule."""
        # Create a one-time schedule
        schedule = TaskSchedule()
        
        # Verify the default values
        self.assertIsNone(schedule.interval)
        self.assertIsNone(schedule.cron)
        self.assertEqual(schedule.max_runs, 1)
        self.assertIsNone(schedule.start_after)
    
    def test_interval_schedule(self):
        """Test creating an interval-based schedule."""
        # Create an interval schedule
        interval = timedelta(minutes=5)
        schedule = TaskSchedule(interval=interval, max_runs=10)
        
        # Verify the values
        self.assertEqual(schedule.interval, interval)
        self.assertIsNone(schedule.cron)
        self.assertEqual(schedule.max_runs, 10)
        self.assertIsNone(schedule.start_after)
    
    def test_cron_schedule(self):
        """Test creating a cron-based schedule."""
        # Create a cron schedule
        cron = "0 * * * *"  # Every hour
        schedule = TaskSchedule(cron=cron)
        
        # Verify the values
        self.assertIsNone(schedule.interval)
        self.assertEqual(schedule.cron, cron)
        self.assertEqual(schedule.max_runs, 1)
        self.assertIsNone(schedule.start_after)
    
    def test_schedule_with_start_after(self):
        """Test creating a schedule with a start time."""
        # Create a schedule with a start time
        start_time = datetime.now() + timedelta(hours=1)
        schedule = TaskSchedule(start_after=start_time)
        
        # Verify the values
        self.assertIsNone(schedule.interval)
        self.assertIsNone(schedule.cron)
        self.assertEqual(schedule.max_runs, 1)
        self.assertEqual(schedule.start_after, start_time)
    
    def test_is_due_one_time(self):
        """Test if a one-time schedule is due."""
        # Create a one-time schedule
        schedule = TaskSchedule()
        
        # Verify it's due immediately
        self.assertTrue(schedule.is_due(datetime.now()))
        
        # Verify it's not due after being run once
        self.assertFalse(schedule.is_due(datetime.now(), runs_completed=1))
    
    def test_is_due_with_start_after(self):
        """Test if a schedule with start_after is due."""
        # Create a schedule with a future start time
        start_time = datetime.now() + timedelta(hours=1)
        schedule = TaskSchedule(start_after=start_time)
        
        # Verify it's not due before the start time
        self.assertFalse(schedule.is_due(datetime.now()))
        
        # Verify it's due after the start time
        future_time = datetime.now() + timedelta(hours=2)
        self.assertTrue(schedule.is_due(future_time))
    
    def test_is_due_interval(self):
        """Test if an interval-based schedule is due."""
        # Create an interval schedule
        interval = timedelta(minutes=5)
        schedule = TaskSchedule(interval=interval, max_runs=3)
        
        # Verify it's due immediately
        now = datetime.now()
        self.assertTrue(schedule.is_due(now))
        
        # Verify it's not due right after being run
        last_run = now
        self.assertFalse(schedule.is_due(now, last_run=last_run, runs_completed=1))
        
        # Verify it's due after the interval has passed
        future_time = now + timedelta(minutes=6)
        self.assertTrue(schedule.is_due(future_time, last_run=last_run, runs_completed=1))
        
        # Verify it's not due after max_runs
        self.assertFalse(schedule.is_due(future_time, last_run=last_run, runs_completed=3))
    
    def test_next_run_time_one_time(self):
        """Test getting the next run time for a one-time schedule."""
        # Create a one-time schedule
        schedule = TaskSchedule()
        
        # Verify the next run time is None if already run
        self.assertIsNone(schedule.next_run_time(datetime.now(), runs_completed=1))
        
        # Verify the next run time is now if not run yet
        now = datetime.now()
        self.assertEqual(schedule.next_run_time(now), now)
    
    def test_next_run_time_with_start_after(self):
        """Test getting the next run time for a schedule with start_after."""
        # Create a schedule with a future start time
        start_time = datetime.now() + timedelta(hours=1)
        schedule = TaskSchedule(start_after=start_time)
        
        # Verify the next run time is the start time
        self.assertEqual(schedule.next_run_time(datetime.now()), start_time)
    
    def test_next_run_time_interval(self):
        """Test getting the next run time for an interval-based schedule."""
        # Create an interval schedule
        interval = timedelta(minutes=5)
        schedule = TaskSchedule(interval=interval, max_runs=3)
        
        # Verify the next run time is now if not run yet
        now = datetime.now()
        self.assertEqual(schedule.next_run_time(now), now)
        
        # Verify the next run time is last_run + interval if already run
        last_run = now
        expected_next_run = last_run + interval
        self.assertEqual(
            schedule.next_run_time(now, last_run=last_run, runs_completed=1),
            expected_next_run
        )
        
        # Verify the next run time is None if max_runs reached
        self.assertIsNone(
            schedule.next_run_time(now, last_run=last_run, runs_completed=3)
        )


class TestTask(unittest.TestCase):
    """Test cases for the Task class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_callback = Mock()
        self.mock_callback.return_value = "task_result"
    
    def test_task_creation(self):
        """Test creating a task with basic properties."""
        # Create a task
        task = Task(
            name="TestTask",
            callback=self.mock_callback,
            schedule=TaskSchedule()
        )
        
        # Verify the task properties
        self.assertEqual(task.name, "TestTask")
        self.assertEqual(task.callback, self.mock_callback)
        self.assertIsInstance(task.schedule, TaskSchedule)
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.runs_completed, 0)
        self.assertIsNone(task.last_run)
        self.assertIsNone(task.last_result)
        self.assertIsNotNone(task.task_id)
    
    def test_task_with_args_kwargs(self):
        """Test creating a task with args and kwargs."""
        # Create a task with args and kwargs
        task = Task(
            name="TestTask",
            callback=self.mock_callback,
            schedule=TaskSchedule(),
            args=(1, 2),
            kwargs={"key": "value"}
        )
        
        # Verify the task properties
        self.assertEqual(task.args, (1, 2))
        self.assertEqual(task.kwargs, {"key": "value"})
    
    def test_execute_task(self):
        """Test executing a task."""
        # Create a task
        task = Task(
            name="TestTask",
            callback=self.mock_callback,
            schedule=TaskSchedule(),
            args=(1, 2),
            kwargs={"key": "value"}
        )
        
        # Execute the task
        result = task.execute()
        
        # Verify the callback was called with the correct arguments
        self.mock_callback.assert_called_once_with(1, 2, key="value")
        
        # Verify the task state was updated
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertEqual(task.runs_completed, 1)
        self.assertIsNotNone(task.last_run)
        self.assertEqual(task.last_result, "task_result")
        
        # Verify the result
        self.assertEqual(result, "task_result")
    
    def test_execute_task_with_exception(self):
        """Test executing a task that raises an exception."""
        # Create a callback that raises an exception
        def failing_callback():
            raise ValueError("Test exception")
        
        # Create a task
        task = Task(
            name="FailingTask",
            callback=failing_callback,
            schedule=TaskSchedule()
        )
        
        # Execute the task
        with self.assertRaises(ValueError):
            task.execute()
        
        # Verify the task state was updated
        self.assertEqual(task.status, TaskStatus.FAILED)
        self.assertEqual(task.runs_completed, 0)
        self.assertIsNotNone(task.last_run)
        self.assertIsNone(task.last_result)
    
    def test_is_due(self):
        """Test checking if a task is due."""
        # Create a task with a schedule
        schedule = TaskSchedule(interval=timedelta(minutes=5), max_runs=3)
        task = Task(
            name="TestTask",
            callback=self.mock_callback,
            schedule=schedule
        )
        
        # Verify the task is due initially
        now = datetime.now()
        self.assertTrue(task.is_due(now))
        
        # Execute the task
        task.execute()
        
        # Verify the task is not due right after execution
        self.assertFalse(task.is_due(now))
        
        # Verify the task is due after the interval
        future_time = now + timedelta(minutes=6)
        self.assertTrue(task.is_due(future_time))
        
        # Execute the task twice more
        task.execute()
        task.execute()
        
        # Verify the task is not due after max_runs
        self.assertFalse(task.is_due(future_time))
    
    def test_next_run_time(self):
        """Test getting the next run time for a task."""
        # Create a task with a schedule
        schedule = TaskSchedule(interval=timedelta(minutes=5), max_runs=3)
        task = Task(
            name="TestTask",
            callback=self.mock_callback,
            schedule=schedule
        )
        
        # Verify the next run time is now initially
        now = datetime.now()
        self.assertEqual(task.next_run_time(now), now)
        
        # Execute the task
        task.execute()
        
        # Verify the next run time is last_run + interval
        expected_next_run = task.last_run + timedelta(minutes=5)
        self.assertEqual(task.next_run_time(now), expected_next_run)
        
        # Execute the task twice more
        task.execute()
        task.execute()
        
        # Verify the next run time is None after max_runs
        self.assertIsNone(task.next_run_time(now))


if __name__ == "__main__":
    unittest.main()
