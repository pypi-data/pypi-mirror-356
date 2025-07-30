"""
Integration test for a complete agent lifecycle using the event_driven_agent example.
"""

import os
import sys
import unittest
from unittest.mock import patch
import importlib.util
import tempfile
import shutil
from pathlib import Path

from num_agents.eventbus.eventbus import EventBus
from num_agents.eventbus.event import Event
from num_agents.scheduler.scheduler import Scheduler


class TestEventDrivenAgentLifecycle(unittest.TestCase):
    """Integration test for a complete agent lifecycle using the event_driven_agent example."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for the test
        self.test_dir = tempfile.mkdtemp()
        
        # Path to the event_driven_agent example
        self.example_dir = Path(__file__).parent.parent.parent / "examples" / "event_driven_agent"
        
        # Copy the example files to the temporary directory
        if self.example_dir.exists():
            shutil.copytree(self.example_dir, os.path.join(self.test_dir, "event_driven_agent"))
            self.agent_dir = os.path.join(self.test_dir, "event_driven_agent")
        else:
            # If the example doesn't exist, create a minimal version for testing
            self.agent_dir = os.path.join(self.test_dir, "event_driven_agent")
            os.makedirs(self.agent_dir)
            
            # Create a minimal main.py
            with open(os.path.join(self.agent_dir, "main.py"), "w") as f:
                f.write("""
from flow import create_flow
from shared_store import create_shared_store

def main():
    shared_store = create_shared_store()
    flow = create_flow()
    flow.run(shared_store)

if __name__ == "__main__":
    main()
                """)
            
            # Create a minimal flow.py
            with open(os.path.join(self.agent_dir, "flow.py"), "w") as f:
                f.write("""
from num_agents.core import Flow
from num_agents.eventbus.eventbus import EventBus
from num_agents.scheduler.scheduler import Scheduler
from nodes.event_publisher_node import EventPublisherNode
from nodes.event_subscriber_node import EventSubscriberNode
from nodes.scheduled_task_node import ScheduledTaskNode

def create_flow():
    # Create EventBus and Scheduler
    event_bus = EventBus()
    scheduler = Scheduler(event_bus=event_bus)
    
    # Create nodes
    event_publisher = EventPublisherNode(event_bus=event_bus, name="EventPublisher")
    event_subscriber = EventSubscriberNode(event_bus=event_bus, name="EventSubscriber")
    scheduled_task = ScheduledTaskNode(scheduler=scheduler, name="ScheduledTask")
    
    # Create flow
    flow = Flow(
        nodes=[event_publisher, event_subscriber, scheduled_task],
        name="EventDrivenAgentFlow"
    )
    
    return flow
                """)
            
            # Create a minimal shared_store.py
            with open(os.path.join(self.agent_dir, "shared_store.py"), "w") as f:
                f.write("""
from num_agents.core import SharedStore

def create_shared_store():
    shared_store = SharedStore()
    return shared_store
                """)
            
            # Create nodes directory
            os.makedirs(os.path.join(self.agent_dir, "nodes"))
            
            # Create event_publisher_node.py
            with open(os.path.join(self.agent_dir, "nodes", "event_publisher_node.py"), "w") as f:
                f.write("""
from num_agents.core import Node
from num_agents.eventbus.eventbus import EventBus
from num_agents.eventbus.event import Event

class EventPublisherNode(Node):
    def __init__(self, event_bus, name="EventPublisherNode"):
        super().__init__(name=name)
        self.event_bus = event_bus
    
    def exec(self, shared):
        # Publish a test event
        event = Event(
            event_type="test.event",
            payload={"message": "Hello from EventPublisherNode!"},
            source=self.name
        )
        self.event_bus.publish(event)
        
        # Store the event in the shared store for testing
        shared.set("published_event", event)
        
        return {"status": "Event published"}
                """)
            
            # Create event_subscriber_node.py
            with open(os.path.join(self.agent_dir, "nodes", "event_subscriber_node.py"), "w") as f:
                f.write("""
from num_agents.core import Node
from num_agents.eventbus.eventbus import EventBus

class EventSubscriberNode(Node):
    def __init__(self, event_bus, name="EventSubscriberNode"):
        super().__init__(name=name)
        self.event_bus = event_bus
        self.received_events = []
        
        # Subscribe to the test event
        self.event_bus.subscribe("test.event", self.handle_test_event)
    
    def handle_test_event(self, event):
        self.received_events.append(event)
    
    def exec(self, shared):
        # Store the received events in the shared store for testing
        shared.set("received_events", self.received_events)
        
        return {"status": "Subscribed to events", "event_count": len(self.received_events)}
                """)
            
            # Create scheduled_task_node.py
            with open(os.path.join(self.agent_dir, "nodes", "scheduled_task_node.py"), "w") as f:
                f.write("""
from num_agents.core import Node
from num_agents.scheduler.scheduler import Scheduler

class ScheduledTaskNode(Node):
    def __init__(self, scheduler, name="ScheduledTaskNode"):
        super().__init__(name=name)
        self.scheduler = scheduler
    
    def test_task(self):
        return {"status": "Task executed"}
    
    def exec(self, shared):
        # Schedule a task
        task_id = self.scheduler.schedule(
            name="TestTask",
            callback=self.test_task,
            interval=5,  # 5 seconds
            max_runs=1
        )
        
        # Store the task ID in the shared store for testing
        shared.set("scheduled_task_id", task_id)
        
        return {"status": "Task scheduled", "task_id": task_id}
                """)
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_agent_lifecycle(self):
        """Test the complete lifecycle of the event-driven agent."""
        # Add the agent directory to the Python path
        sys.path.insert(0, self.agent_dir)
        
        try:
            # Import the modules from the agent
            flow_module = importlib.import_module("flow")
            shared_store_module = importlib.import_module("shared_store")
            
            # Create the shared store
            shared_store = shared_store_module.create_shared_store()
            
            # Create the flow
            flow = flow_module.create_flow()
            
            # Run the flow
            flow.run(shared_store)
            
            # Check that the event was published
            published_event = shared_store.get("published_event")
            self.assertIsNotNone(published_event)
            self.assertEqual(published_event.event_type, "test.event")
            self.assertEqual(published_event.payload["message"], "Hello from EventPublisherNode!")
            
            # Check that the event was received by the subscriber
            received_events = shared_store.get("received_events")
            self.assertIsNotNone(received_events)
            self.assertEqual(len(received_events), 1)
            self.assertEqual(received_events[0].event_type, "test.event")
            self.assertEqual(received_events[0].payload["message"], "Hello from EventPublisherNode!")
            
            # Check that the task was scheduled
            task_id = shared_store.get("scheduled_task_id")
            self.assertIsNotNone(task_id)
            
            # Get the scheduler from the flow
            scheduler = None
            for node in flow.nodes:
                if hasattr(node, "scheduler"):
                    scheduler = node.scheduler
                    break
            
            self.assertIsNotNone(scheduler)
            
            # Check that the task exists in the scheduler
            self.assertIn(task_id, scheduler.tasks)
            
            # Execute the task
            result = scheduler.execute_task(task_id)
            
            # Check the task result
            self.assertEqual(result, {"status": "Task executed"})
            
        finally:
            # Remove the agent directory from the Python path
            sys.path.remove(self.agent_dir)


if __name__ == "__main__":
    unittest.main()
