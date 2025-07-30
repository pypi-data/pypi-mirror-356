"""
Tests for the EventBus nodes in the EventBus system.
"""

import unittest
from unittest.mock import Mock, patch
import asyncio

from num_agents.core import SharedStore
from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus
from num_agents.eventbus.event_bus_node import (
    EventEmitterNode,
    EventListenerNode,
    EventDrivenBranchNode
)


class TestEventEmitterNode(unittest.TestCase):
    """Test cases for the EventEmitterNode class."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.shared = SharedStore()
        self.shared.set("test_payload", {"data": "test_value"})
    
    def test_emit_event(self):
        """Test emitting an event from a node."""
        # Create a mock handler to verify the event
        mock_handler = Mock()
        self.event_bus.subscribe("test.event", mock_handler)
        
        # Create an emitter node
        emitter_node = EventEmitterNode(
            event_bus=self.event_bus,
            event_type="test.event",
            payload_key="test_payload",
            name="TestEmitter"
        )
        
        # Execute the node
        result = emitter_node.exec(self.shared)
        
        # Verify the event was published
        self.assertEqual(mock_handler.call_count, 1)
        event = mock_handler.call_args[0][0]
        self.assertEqual(event.event_type, "test.event")
        self.assertEqual(event.payload, {"data": "test_value"})
        self.assertEqual(event.source, "TestEmitter")
        
        # Verify the node result
        self.assertTrue(result["event_emitted"])
        self.assertEqual(result["event_type"], "test.event")
    
    def test_emit_event_with_static_payload(self):
        """Test emitting an event with a static payload."""
        # Create a mock handler to verify the event
        mock_handler = Mock()
        self.event_bus.subscribe("test.event", mock_handler)
        
        # Create an emitter node with a static payload
        static_payload = {"static": "payload"}
        emitter_node = EventEmitterNode(
            event_bus=self.event_bus,
            event_type="test.event",
            payload=static_payload,
            name="TestEmitter"
        )
        
        # Execute the node
        result = emitter_node.exec(self.shared)
        
        # Verify the event was published with the static payload
        self.assertEqual(mock_handler.call_count, 1)
        event = mock_handler.call_args[0][0]
        self.assertEqual(event.payload, static_payload)
    
    def test_emit_event_with_metadata(self):
        """Test emitting an event with metadata."""
        # Create a mock handler to verify the event
        mock_handler = Mock()
        self.event_bus.subscribe("test.event", mock_handler)
        
        # Create an emitter node with metadata
        metadata = {"priority": "high"}
        emitter_node = EventEmitterNode(
            event_bus=self.event_bus,
            event_type="test.event",
            payload_key="test_payload",
            metadata=metadata,
            name="TestEmitter"
        )
        
        # Execute the node
        emitter_node.exec(self.shared)
        
        # Verify the event was published with metadata
        event = mock_handler.call_args[0][0]
        self.assertEqual(event.metadata, metadata)


class TestEventListenerNode(unittest.TestCase):
    """Test cases for the EventListenerNode class."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.shared = SharedStore()
        self.test_event = Event(
            event_type="test.event",
            payload={"data": "test_value"},
            source="test_source"
        )
    
    @patch('asyncio.get_event_loop')
    def test_listen_for_event(self, mock_get_event_loop):
        """Test listening for an event."""
        # Mock the event loop
        mock_loop = Mock()
        mock_get_event_loop.return_value = mock_loop
        
        # Set up the future that will be returned by create_future
        future = asyncio.Future()
        future.set_result(self.test_event)
        mock_loop.create_future.return_value = future
        
        # Create a listener node
        listener_node = EventListenerNode(
            event_bus=self.event_bus,
            event_type="test.event",
            output_key="received_event",
            timeout=1.0,
            name="TestListener"
        )
        
        # Execute the node
        result = listener_node.exec(self.shared)
        
        # Verify the event was stored in the shared store
        self.assertEqual(self.shared.get("received_event"), self.test_event)
        
        # Verify the node result
        self.assertTrue(result["event_received"])
        self.assertEqual(result["event_type"], "test.event")
    
    @patch('asyncio.get_event_loop')
    def test_listen_timeout(self, mock_get_event_loop):
        """Test listener timeout when no event is received."""
        # Mock the event loop
        mock_loop = Mock()
        mock_get_event_loop.return_value = mock_loop
        
        # Set up the future that will be returned by create_future
        future = asyncio.Future()
        future.set_exception(asyncio.TimeoutError())
        mock_loop.create_future.return_value = future
        
        # Create a listener node
        listener_node = EventListenerNode(
            event_bus=self.event_bus,
            event_type="test.event",
            output_key="received_event",
            timeout=0.1,
            name="TestListener"
        )
        
        # Execute the node
        result = listener_node.exec(self.shared)
        
        # Verify no event was stored in the shared store
        self.assertIsNone(self.shared.get("received_event"))
        
        # Verify the node result
        self.assertFalse(result["event_received"])


class TestEventDrivenBranchNode(unittest.TestCase):
    """Test cases for the EventDrivenBranchNode class."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.shared = SharedStore()
        
        # Create mock nodes for branching
        self.branch1_node = Mock()
        self.branch1_node.exec.return_value = {"branch": "1"}
        
        self.branch2_node = Mock()
        self.branch2_node.exec.return_value = {"branch": "2"}
        
        self.default_node = Mock()
        self.default_node.exec.return_value = {"branch": "default"}
    
    @patch('asyncio.get_event_loop')
    def test_branch_on_event(self, mock_get_event_loop):
        """Test branching based on received event."""
        # Mock the event loop
        mock_loop = Mock()
        mock_get_event_loop.return_value = mock_loop
        
        # Set up the future that will be returned by create_future
        event = Event(
            event_type="branch1.event",
            payload={"data": "test_value"},
            source="test_source"
        )
        future = asyncio.Future()
        future.set_result(event)
        mock_loop.create_future.return_value = future
        
        # Create a branch node
        branch_node = EventDrivenBranchNode(
            event_bus=self.event_bus,
            event_branches={
                "branch1.event": self.branch1_node,
                "branch2.event": self.branch2_node
            },
            default_branch=self.default_node,
            timeout=1.0,
            name="TestBranch"
        )
        
        # Execute the node
        result = branch_node.exec(self.shared)
        
        # Verify the correct branch was taken
        self.branch1_node.exec.assert_called_once_with(self.shared)
        self.branch2_node.exec.assert_not_called()
        self.default_node.exec.assert_not_called()
        
        # Verify the node result
        self.assertEqual(result, {"branch": "1"})
    
    @patch('asyncio.get_event_loop')
    def test_default_branch_on_timeout(self, mock_get_event_loop):
        """Test taking the default branch on timeout."""
        # Mock the event loop
        mock_loop = Mock()
        mock_get_event_loop.return_value = mock_loop
        
        # Set up the future that will be returned by create_future
        future = asyncio.Future()
        future.set_exception(asyncio.TimeoutError())
        mock_loop.create_future.return_value = future
        
        # Create a branch node
        branch_node = EventDrivenBranchNode(
            event_bus=self.event_bus,
            event_branches={
                "branch1.event": self.branch1_node,
                "branch2.event": self.branch2_node
            },
            default_branch=self.default_node,
            timeout=0.1,
            name="TestBranch"
        )
        
        # Execute the node
        result = branch_node.exec(self.shared)
        
        # Verify the default branch was taken
        self.branch1_node.exec.assert_not_called()
        self.branch2_node.exec.assert_not_called()
        self.default_node.exec.assert_called_once_with(self.shared)
        
        # Verify the node result
        self.assertEqual(result, {"branch": "default"})


if __name__ == "__main__":
    unittest.main()
