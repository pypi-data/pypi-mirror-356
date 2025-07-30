"""
Tests for the utility functions in the EventBus system.
"""

import unittest
from unittest.mock import Mock, patch

from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus
from num_agents.eventbus.utils import (
    publish_event,
    publish_flow_started_event,
    publish_flow_completed_event,
    publish_node_started_event,
    publish_node_completed_event
)


class TestEventBusUtils(unittest.TestCase):
    """Test cases for the EventBus utility functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.mock_handler = Mock()
    
    def test_publish_event(self):
        """Test the publish_event utility function."""
        # Subscribe to the event type
        self.event_bus.subscribe("test.event", self.mock_handler)
        
        # Use the utility function to publish an event
        publish_event(
            event_bus=self.event_bus,
            event_type="test.event",
            payload={"key": "value"},
            metadata={"priority": "high"},
            source="test_source"
        )
        
        # Verify the handler was called with the correct event
        self.assertEqual(self.mock_handler.call_count, 1)
        event = self.mock_handler.call_args[0][0]
        self.assertEqual(event.event_type, "test.event")
        self.assertEqual(event.payload, {"key": "value"})
        self.assertEqual(event.metadata, {"priority": "high"})
        self.assertEqual(event.source, "test_source")
    
    def test_publish_flow_started_event(self):
        """Test the publish_flow_started_event utility function."""
        # Subscribe to the flow.started event type
        self.event_bus.subscribe(EventTypes.FLOW_STARTED, self.mock_handler)
        
        # Use the utility function to publish a flow started event
        publish_flow_started_event(
            event_bus=self.event_bus,
            flow_name="TestFlow",
            flow_id="flow-123"
        )
        
        # Verify the handler was called with the correct event
        self.assertEqual(self.mock_handler.call_count, 1)
        event = self.mock_handler.call_args[0][0]
        self.assertEqual(event.event_type, EventTypes.FLOW_STARTED)
        self.assertEqual(event.payload["flow_name"], "TestFlow")
        self.assertEqual(event.payload["flow_id"], "flow-123")
        self.assertEqual(event.source, "Flow")
    
    def test_publish_flow_completed_event(self):
        """Test the publish_flow_completed_event utility function."""
        # Subscribe to the flow.completed event type
        self.event_bus.subscribe(EventTypes.FLOW_COMPLETED, self.mock_handler)
        
        # Use the utility function to publish a flow completed event
        publish_flow_completed_event(
            event_bus=self.event_bus,
            flow_name="TestFlow",
            flow_id="flow-123",
            result={"status": "success"}
        )
        
        # Verify the handler was called with the correct event
        self.assertEqual(self.mock_handler.call_count, 1)
        event = self.mock_handler.call_args[0][0]
        self.assertEqual(event.event_type, EventTypes.FLOW_COMPLETED)
        self.assertEqual(event.payload["flow_name"], "TestFlow")
        self.assertEqual(event.payload["flow_id"], "flow-123")
        self.assertEqual(event.payload["result"], {"status": "success"})
        self.assertEqual(event.source, "Flow")
    
    def test_publish_node_started_event(self):
        """Test the publish_node_started_event utility function."""
        # Subscribe to the node.started event type
        self.event_bus.subscribe(EventTypes.NODE_STARTED, self.mock_handler)
        
        # Use the utility function to publish a node started event
        publish_node_started_event(
            event_bus=self.event_bus,
            node_name="TestNode",
            node_id="node-123",
            flow_id="flow-123"
        )
        
        # Verify the handler was called with the correct event
        self.assertEqual(self.mock_handler.call_count, 1)
        event = self.mock_handler.call_args[0][0]
        self.assertEqual(event.event_type, EventTypes.NODE_STARTED)
        self.assertEqual(event.payload["node_name"], "TestNode")
        self.assertEqual(event.payload["node_id"], "node-123")
        self.assertEqual(event.payload["flow_id"], "flow-123")
        self.assertEqual(event.source, "Node")
    
    def test_publish_node_completed_event(self):
        """Test the publish_node_completed_event utility function."""
        # Subscribe to the node.completed event type
        self.event_bus.subscribe(EventTypes.NODE_COMPLETED, self.mock_handler)
        
        # Use the utility function to publish a node completed event
        publish_node_completed_event(
            event_bus=self.event_bus,
            node_name="TestNode",
            node_id="node-123",
            flow_id="flow-123",
            result={"status": "success"}
        )
        
        # Verify the handler was called with the correct event
        self.assertEqual(self.mock_handler.call_count, 1)
        event = self.mock_handler.call_args[0][0]
        self.assertEqual(event.event_type, EventTypes.NODE_COMPLETED)
        self.assertEqual(event.payload["node_name"], "TestNode")
        self.assertEqual(event.payload["node_id"], "node-123")
        self.assertEqual(event.payload["flow_id"], "flow-123")
        self.assertEqual(event.payload["result"], {"status": "success"})
        self.assertEqual(event.source, "Node")


if __name__ == "__main__":
    unittest.main()
