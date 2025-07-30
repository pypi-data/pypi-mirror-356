"""
Tests for the Scheduler nodes in the Scheduler system.
"""

import unittest
from unittest.mock import Mock, patch
import asyncio
from datetime import datetime, timedelta

from num_agents.core import SharedStore
from num_agents.eventbus.eventbus import EventBus
from num_agents.scheduler.scheduler import Scheduler
from num_agents.scheduler.task import Task, TaskSchedule, TaskStatus
from num_agents.scheduler.scheduler_node import (
    ScheduleTaskNode,
    CancelTaskNode,
    WaitForTaskNode,
    ScheduledFlowNode
)


class TestScheduleTaskNode(unittest.TestCase):
    """Test cases for the ScheduleTaskNode class."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.scheduler = Scheduler(event_bus=self.event_bus)
        self.shared = SharedStore()
        
        # Create a mock callback
        self.mock_callback = Mock()
        self.mock_callback.return_value = {"result": "success"}
        
        # Store callback arguments in shared store
        self.shared.set("callback_args", (1, 2))
        self.shared.set("callback_kwargs", {"key": "value"})
    
    def test_schedule_task(self):
        """Test scheduling a task from a node."""
        # Create a schedule task node
        schedule_node = ScheduleTaskNode(
            scheduler=self.scheduler,
            task_name="TestTask",
            callback=self.mock_callback,
            args_key="callback_args",
            kwargs_key="callback_kwargs",
            task_id_output_key="task_id",
            name="ScheduleTaskNode"
        )
        
        # Execute the node
        result = schedule_node.exec(self.shared)
        
        # Verify the task was scheduled
        self.assertEqual(len(self.scheduler.tasks), 1)
        
        # Verify the task ID was stored in the shared store
        task_id = self.shared.get("task_id")
        self.assertIsNotNone(task_id)
        
        # Verify the task properties
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.name, "TestTask")
        self.assertEqual(task.callback, self.mock_callback)
        self.assertEqual(task.args, (1, 2))
        self.assertEqual(task.kwargs, {"key": "value"})
        
        # Verify the node result
        self.assertTrue(result["task_scheduled"])
        self.assertEqual(result["task_id"], task_id)
    
    def test_schedule_task_with_delay(self):
        """Test scheduling a task with a delay."""
        # Create a schedule task node with a delay
        schedule_node = ScheduleTaskNode(
            scheduler=self.scheduler,
            task_name="TestTask",
            callback=self.mock_callback,
            delay=60,  # 60 seconds
            task_id_output_key="task_id",
            name="ScheduleTaskNode"
        )
        
        # Execute the node
        schedule_node.exec(self.shared)
        
        # Verify the task was scheduled with a delay
        task_id = self.shared.get("task_id")
        task = self.scheduler.tasks[task_id]
        self.assertIsNotNone(task.schedule.start_after)
        
        # The start_after time should be approximately now + delay
        now = datetime.now()
        expected_start = now + timedelta(seconds=60)
        self.assertAlmostEqual(
            task.schedule.start_after.timestamp(),
            expected_start.timestamp(),
            delta=1  # Allow 1 second difference
        )
    
    def test_schedule_task_with_interval(self):
        """Test scheduling a task with an interval."""
        # Create a schedule task node with an interval
        schedule_node = ScheduleTaskNode(
            scheduler=self.scheduler,
            task_name="TestTask",
            callback=self.mock_callback,
            interval=60,  # 60 seconds
            max_runs=3,
            task_id_output_key="task_id",
            name="ScheduleTaskNode"
        )
        
        # Execute the node
        schedule_node.exec(self.shared)
        
        # Verify the task was scheduled with an interval
        task_id = self.shared.get("task_id")
        task = self.scheduler.tasks[task_id]
        self.assertEqual(task.schedule.interval, timedelta(seconds=60))
        self.assertEqual(task.schedule.max_runs, 3)


class TestCancelTaskNode(unittest.TestCase):
    """Test cases for the CancelTaskNode class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scheduler = Scheduler()
        self.shared = SharedStore()
        
        # Schedule a task
        self.task_id = self.scheduler.schedule(
            name="TestTask",
            callback=lambda: "result"
        )
        
        # Store the task ID in the shared store
        self.shared.set("task_id", self.task_id)
    
    def test_cancel_task(self):
        """Test canceling a task from a node."""
        # Create a cancel task node
        cancel_node = CancelTaskNode(
            scheduler=self.scheduler,
            task_id_key="task_id",
            name="CancelTaskNode"
        )
        
        # Execute the node
        result = cancel_node.exec(self.shared)
        
        # Verify the task was canceled
        self.assertEqual(len(self.scheduler.tasks), 0)
        
        # Verify the node result
        self.assertTrue(result["task_cancelled"])
        self.assertEqual(result["task_id"], self.task_id)
    
    def test_cancel_nonexistent_task(self):
        """Test canceling a nonexistent task."""
        # Store a nonexistent task ID in the shared store
        self.shared.set("task_id", "nonexistent-id")
        
        # Create a cancel task node
        cancel_node = CancelTaskNode(
            scheduler=self.scheduler,
            task_id_key="task_id",
            name="CancelTaskNode"
        )
        
        # Execute the node
        result = cancel_node.exec(self.shared)
        
        # Verify the node result
        self.assertFalse(result["task_cancelled"])
        self.assertEqual(result["task_id"], "nonexistent-id")


class TestWaitForTaskNode(unittest.TestCase):
    """Test cases for the WaitForTaskNode class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scheduler = Scheduler()
        self.shared = SharedStore()
        
        # Create a mock callback
        self.mock_callback = Mock()
        self.mock_callback.return_value = {"result": "success"}
        
        # Schedule a task
        self.task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.mock_callback
        )
        
        # Store the task ID in the shared store
        self.shared.set("task_id", self.task_id)
    
    @patch('asyncio.get_event_loop')
    def test_wait_for_task(self, mock_get_event_loop):
        """Test waiting for a task to complete."""
        # Mock the event loop
        mock_loop = Mock()
        mock_get_event_loop.return_value = mock_loop
        
        # Set up the future that will be returned by create_future
        future = asyncio.Future()
        future.set_result({"result": "success"})
        mock_loop.create_future.return_value = future
        
        # Create a wait for task node
        wait_node = WaitForTaskNode(
            scheduler=self.scheduler,
            task_id_key="task_id",
            result_key="task_result",
            timeout=1.0,
            name="WaitForTaskNode"
        )
        
        # Execute the node
        result = wait_node.exec(self.shared)
        
        # Verify the task result was stored in the shared store
        self.assertEqual(self.shared.get("task_result"), {"result": "success"})
        
        # Verify the node result
        self.assertTrue(result["task_completed"])
        self.assertEqual(result["task_id"], self.task_id)
    
    @patch('asyncio.get_event_loop')
    def test_wait_timeout(self, mock_get_event_loop):
        """Test timeout when waiting for a task."""
        # Mock the event loop
        mock_loop = Mock()
        mock_get_event_loop.return_value = mock_loop
        
        # Set up the future that will be returned by create_future
        future = asyncio.Future()
        future.set_exception(asyncio.TimeoutError())
        mock_loop.create_future.return_value = future
        
        # Create a wait for task node
        wait_node = WaitForTaskNode(
            scheduler=self.scheduler,
            task_id_key="task_id",
            result_key="task_result",
            timeout=0.1,
            name="WaitForTaskNode"
        )
        
        # Execute the node
        result = wait_node.exec(self.shared)
        
        # Verify no result was stored in the shared store
        self.assertIsNone(self.shared.get("task_result"))
        
        # Verify the node result
        self.assertFalse(result["task_completed"])
        self.assertEqual(result["task_id"], self.task_id)


class TestScheduledFlowNode(unittest.TestCase):
    """Test cases for the ScheduledFlowNode class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scheduler = Scheduler()
        self.shared = SharedStore()
        
        # Create mock nodes for the sub-flow
        self.node1 = Mock()
        self.node1.exec.return_value = {"node": "1"}
        self.node1.name = "Node1"
        
        self.node2 = Mock()
        self.node2.exec.return_value = {"node": "2"}
        self.node2.name = "Node2"
    
    def test_schedule_flow(self):
        """Test scheduling a sub-flow."""
        # Create a scheduled flow node
        flow_node = ScheduledFlowNode(
            scheduler=self.scheduler,
            sub_flow_nodes=[self.node1, self.node2],
            interval=60,  # 60 seconds
            task_id_output_key="flow_task_id",
            name="ScheduledFlowNode"
        )
        
        # Execute the node
        result = flow_node.exec(self.shared)
        
        # Verify the flow was scheduled
        self.assertEqual(len(self.scheduler.tasks), 1)
        
        # Verify the task ID was stored in the shared store
        task_id = self.shared.get("flow_task_id")
        self.assertIsNotNone(task_id)
        
        # Verify the node result
        self.assertTrue(result["flow_scheduled"])
        self.assertEqual(result["task_id"], task_id)
    
    def test_execute_flow_callback(self):
        """Test executing the flow callback."""
        # Create a scheduled flow node
        flow_node = ScheduledFlowNode(
            scheduler=self.scheduler,
            sub_flow_nodes=[self.node1, self.node2],
            interval=60,  # 60 seconds
            name="ScheduledFlowNode"
        )
        
        # Execute the node to schedule the flow
        flow_node.exec(self.shared)
        
        # Get the scheduled task
        task = list(self.scheduler.tasks.values())[0]
        
        # Execute the task callback (which should execute the sub-flow)
        result = task.execute()
        
        # Verify the sub-flow nodes were executed
        self.node1.exec.assert_called_once()
        self.node2.exec.assert_called_once()
        
        # Verify the result contains the results of all nodes
        self.assertEqual(result, [{"node": "1"}, {"node": "2"}])


if __name__ == "__main__":
    unittest.main()
