"""
Tests for the EventBus class in the EventBus system.
"""

import unittest
from unittest.mock import Mock

from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus


class TestEventBus(unittest.TestCase):
    """Test cases for the EventBus class."""

    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = EventBus()
        self.test_event = Event(
            event_type="test.event",
            payload={"key": "value"},
            source="test_source"
        )
    
    def test_subscribe_and_publish(self):
        """Test subscribing to an event type and publishing an event."""
        # Create a mock handler
        mock_handler = Mock()
        
        # Subscribe to the event type
        self.event_bus.subscribe("test.event", mock_handler)
        
        # Publish an event
        self.event_bus.publish(self.test_event)
        
        # Verify the handler was called with the event
        mock_handler.assert_called_once_with(self.test_event)
    
    def test_unsubscribe(self):
        """Test unsubscribing from an event type."""
        # Create a mock handler
        mock_handler = Mock()
        
        # Subscribe to the event type
        self.event_bus.subscribe("test.event", mock_handler)
        
        # Unsubscribe from the event type
        self.event_bus.unsubscribe("test.event", mock_handler)
        
        # Publish an event
        self.event_bus.publish(self.test_event)
        
        # Verify the handler was not called
        mock_handler.assert_not_called()
    
    def test_pattern_subscription(self):
        """Test subscribing to an event pattern."""
        # Create mock handlers
        mock_handler1 = Mock()
        mock_handler2 = Mock()
        
        # Subscribe to specific event types and patterns
        self.event_bus.subscribe("test.event", mock_handler1)
        self.event_bus.subscribe("test.*", mock_handler2, is_pattern=True)
        
        # Publish an event
        self.event_bus.publish(self.test_event)
        
        # Verify both handlers were called
        mock_handler1.assert_called_once_with(self.test_event)
        mock_handler2.assert_called_once_with(self.test_event)
    
    def test_multiple_handlers(self):
        """Test multiple handlers for the same event type."""
        # Create mock handlers
        mock_handler1 = Mock()
        mock_handler2 = Mock()
        
        # Subscribe both handlers to the same event type
        self.event_bus.subscribe("test.event", mock_handler1)
        self.event_bus.subscribe("test.event", mock_handler2)
        
        # Publish an event
        self.event_bus.publish(self.test_event)
        
        # Verify both handlers were called
        mock_handler1.assert_called_once_with(self.test_event)
        mock_handler2.assert_called_once_with(self.test_event)
    
    def test_handler_exception(self):
        """Test that an exception in one handler doesn't affect others."""
        # Create handlers, one that raises an exception
        def raising_handler(event):
            raise Exception("Test exception")
        
        mock_handler = Mock()
        
        # Subscribe both handlers
        self.event_bus.subscribe("test.event", raising_handler)
        self.event_bus.subscribe("test.event", mock_handler)
        
        # Publish an event (should not raise an exception)
        self.event_bus.publish(self.test_event)
        
        # Verify the second handler was still called
        mock_handler.assert_called_once_with(self.test_event)
    
    def test_no_matching_subscribers(self):
        """Test publishing an event with no matching subscribers."""
        # Create a mock handler
        mock_handler = Mock()
        
        # Subscribe to a different event type
        self.event_bus.subscribe("other.event", mock_handler)
        
        # Publish an event
        self.event_bus.publish(self.test_event)
        
        # Verify the handler was not called
        mock_handler.assert_not_called()
    
    def test_get_subscribers(self):
        """Test getting subscribers for an event type."""
        # Create mock handlers
        mock_handler1 = Mock()
        mock_handler2 = Mock()
        
        # Subscribe handlers to different event types
        self.event_bus.subscribe("test.event", mock_handler1)
        self.event_bus.subscribe("other.event", mock_handler2)
        
        # Get subscribers for test.event
        subscribers = self.event_bus.get_subscribers("test.event")
        
        # Verify the correct handler is in the subscribers
        self.assertEqual(len(subscribers), 1)
        self.assertIn(mock_handler1, subscribers)
        self.assertNotIn(mock_handler2, subscribers)
    
    def test_clear_subscribers(self):
        """Test clearing all subscribers."""
        # Create mock handlers
        mock_handler1 = Mock()
        mock_handler2 = Mock()
        
        # Subscribe handlers to different event types
        self.event_bus.subscribe("test.event", mock_handler1)
        self.event_bus.subscribe("other.event", mock_handler2)
        
        # Clear all subscribers
        self.event_bus.clear_subscribers()
        
        # Publish events
        self.event_bus.publish(self.test_event)
        self.event_bus.publish(Event(
            event_type="other.event",
            payload={"key": "value"},
            source="test_source"
        ))
        
        # Verify no handlers were called
        mock_handler1.assert_not_called()
        mock_handler2.assert_not_called()


if __name__ == "__main__":
    unittest.main()
