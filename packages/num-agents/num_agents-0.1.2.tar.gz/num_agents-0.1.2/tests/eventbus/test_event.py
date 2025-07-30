"""
Tests for the Event class in the EventBus system.
"""

import unittest
from datetime import datetime

from num_agents.eventbus.event import Event, EventTypes


class TestEvent(unittest.TestCase):
    """Test cases for the Event class."""

    def test_event_creation(self):
        """Test creating an event with basic properties."""
        event = Event(
            event_type="test.event",
            payload={"key": "value"},
            source="test_source"
        )
        
        self.assertEqual(event.event_type, "test.event")
        self.assertEqual(event.payload, {"key": "value"})
        self.assertEqual(event.source, "test_source")
        self.assertIsNotNone(event.event_id)
        self.assertIsNotNone(event.timestamp)
    
    def test_event_with_metadata(self):
        """Test creating an event with metadata."""
        metadata = {"priority": "high", "category": "test"}
        event = Event(
            event_type="test.event",
            payload={"key": "value"},
            metadata=metadata,
            source="test_source"
        )
        
        self.assertEqual(event.metadata, metadata)
    
    def test_event_with_custom_id_and_timestamp(self):
        """Test creating an event with custom ID and timestamp."""
        event_id = "custom-id-123"
        timestamp = datetime.now()
        
        event = Event(
            event_type="test.event",
            payload={"key": "value"},
            source="test_source",
            event_id=event_id,
            timestamp=timestamp
        )
        
        self.assertEqual(event.event_id, event_id)
        self.assertEqual(event.timestamp, timestamp)
    
    def test_event_types_constants(self):
        """Test the predefined event type constants."""
        self.assertEqual(EventTypes.FLOW_STARTED, "flow.started")
        self.assertEqual(EventTypes.FLOW_COMPLETED, "flow.completed")
        self.assertEqual(EventTypes.NODE_STARTED, "node.started")
        self.assertEqual(EventTypes.NODE_COMPLETED, "node.completed")
        self.assertEqual(EventTypes.SYSTEM_STARTUP, "system.startup")
        self.assertEqual(EventTypes.SYSTEM_SHUTDOWN, "system.shutdown")
        self.assertEqual(EventTypes.USER_INPUT, "user.input")
    
    def test_event_types_custom(self):
        """Test creating custom event types."""
        custom_type = EventTypes.custom("test.custom")
        self.assertEqual(custom_type, "test.custom")
    
    def test_event_to_dict(self):
        """Test converting an event to a dictionary."""
        event = Event(
            event_type="test.event",
            payload={"key": "value"},
            metadata={"priority": "high"},
            source="test_source",
            event_id="test-id-123"
        )
        
        event_dict = event.to_dict()
        
        self.assertEqual(event_dict["event_type"], "test.event")
        self.assertEqual(event_dict["payload"], {"key": "value"})
        self.assertEqual(event_dict["metadata"], {"priority": "high"})
        self.assertEqual(event_dict["source"], "test_source")
        self.assertEqual(event_dict["event_id"], "test-id-123")
        self.assertIn("timestamp", event_dict)
    
    def test_event_from_dict(self):
        """Test creating an event from a dictionary."""
        timestamp = datetime.now().isoformat()
        event_dict = {
            "event_type": "test.event",
            "payload": {"key": "value"},
            "metadata": {"priority": "high"},
            "source": "test_source",
            "event_id": "test-id-123",
            "timestamp": timestamp
        }
        
        event = Event.from_dict(event_dict)
        
        self.assertEqual(event.event_type, "test.event")
        self.assertEqual(event.payload, {"key": "value"})
        self.assertEqual(event.metadata, {"priority": "high"})
        self.assertEqual(event.source, "test_source")
        self.assertEqual(event.event_id, "test-id-123")
        self.assertEqual(event.timestamp, timestamp)


if __name__ == "__main__":
    unittest.main()
