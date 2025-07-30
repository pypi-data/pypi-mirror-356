"""
Event definitions for the Nüm Agents EventBus.

This module provides the base Event class and related utilities for the event system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional
import uuid


@dataclass
class Event:
    """
    Base class for all events in the Nüm Agents SDK.
    
    An Event represents a message that can be published to the EventBus
    and consumed by subscribers.
    """
    
    event_type: str
    """The type of the event, used for filtering and routing."""
    
    payload: Dict[str, Any] = field(default_factory=dict)
    """The data payload of the event."""
    
    metadata: Dict[str, Any] = field(default_factory=dict)
    """Metadata associated with the event."""
    
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    """Unique identifier for the event."""
    
    timestamp: datetime = field(default_factory=datetime.now)
    """Timestamp when the event was created."""
    
    source: Optional[str] = None
    """Source of the event (e.g., node name, external system)."""
    
    def __post_init__(self) -> None:
        """Validate the event after initialization."""
        if not self.event_type:
            raise ValueError("Event type cannot be empty")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the event to a dictionary representation.
        
        Returns:
            Dictionary representation of the event
        """
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        """
        Create an event from a dictionary representation.
        
        Args:
            data: Dictionary representation of the event
            
        Returns:
            An Event instance
        """
        # Convert ISO timestamp string back to datetime
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        
        return cls(**data)


# Common event types
class EventTypes:
    """Common event types used in the Nüm Agents SDK."""
    
    # System events
    SYSTEM_STARTUP = "system.startup"
    SYSTEM_SHUTDOWN = "system.shutdown"
    
    # Flow events
    FLOW_STARTED = "flow.started"
    FLOW_COMPLETED = "flow.completed"
    FLOW_ERROR = "flow.error"
    
    # Node events
    NODE_STARTED = "node.started"
    NODE_COMPLETED = "node.completed"
    NODE_ERROR = "node.error"
    
    # Data events
    DATA_CREATED = "data.created"
    DATA_UPDATED = "data.updated"
    DATA_DELETED = "data.deleted"
    
    # User interaction events
    USER_INPUT = "user.input"
    USER_FEEDBACK = "user.feedback"
    
    # Custom events (prefix with 'custom.')
    @staticmethod
    def custom(name: str) -> str:
        """
        Create a custom event type name.
        
        Args:
            name: The custom event name
            
        Returns:
            A properly formatted custom event type
        """
        return f"custom.{name}"
