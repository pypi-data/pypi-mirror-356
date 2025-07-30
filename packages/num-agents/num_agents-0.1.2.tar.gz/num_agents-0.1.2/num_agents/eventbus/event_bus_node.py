"""
EventBus node implementation for the Nüm Agents SDK.

This module provides node classes for interacting with the EventBus
within a flow.
"""

from typing import Any, Dict, List, Optional, Pattern, Union

from num_agents.core import Node, SharedStore
from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus


class EventEmitterNode(Node):
    """
    Node for emitting events to the EventBus.
    
    This node allows flows to publish events to the EventBus, enabling
    communication with other components or nodes that are subscribed
    to those events.
    """
    
    def __init__(
        self, 
        event_bus: EventBus,
        event_type: str,
        name: Optional[str] = None,
        payload_key: Optional[str] = None,
        metadata_key: Optional[str] = None,
        source: Optional[str] = None
    ) -> None:
        """
        Initialize an event emitter node.
        
        Args:
            event_bus: The EventBus to emit events to
            event_type: The type of event to emit
            name: Optional name for the node
            payload_key: Optional key in the shared store to use as the event payload
            metadata_key: Optional key in the shared store to use as the event metadata
            source: Optional source identifier for the event
        """
        super().__init__(name or f"EventEmitter({event_type})")
        self.event_bus = event_bus
        self.event_type = event_type
        self.payload_key = payload_key
        self.metadata_key = metadata_key
        self.source = source
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node emits an event to the EventBus.
        
        Args:
            shared: The shared store for accessing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Get payload and metadata from shared store if keys are provided
        payload = shared.get(self.payload_key, {}) if self.payload_key else {}
        metadata = shared.get(self.metadata_key, {}) if self.metadata_key else {}
        
        # Create and publish the event
        event = Event(
            event_type=self.event_type,
            payload=payload,
            metadata=metadata,
            source=self.source or self.name
        )
        
        self.event_bus.publish(event)
        
        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp
        }


class EventListenerNode(Node):
    """
    Node for listening to events from the EventBus.
    
    This node allows flows to react to events published to the EventBus,
    enabling event-driven processing.
    """
    
    def __init__(
        self, 
        event_bus: EventBus,
        event_type: str,
        output_key: str,
        name: Optional[str] = None,
        is_pattern: bool = False,
        timeout: Optional[float] = None
    ) -> None:
        """
        Initialize an event listener node.
        
        Args:
            event_bus: The EventBus to listen to
            event_type: The type of event to listen for (can be a regex pattern if is_pattern is True)
            output_key: Key in the shared store to store the received event
            name: Optional name for the node
            is_pattern: If True, event_type is treated as a regex pattern
            timeout: Optional timeout in seconds to wait for an event
        """
        super().__init__(name or f"EventListener({event_type})")
        self.event_bus = event_bus
        self.event_type = event_type
        self.output_key = output_key
        self.is_pattern = is_pattern
        self.timeout = timeout
        self._received_event: Optional[Event] = None
    
    def _event_handler(self, event: Event) -> None:
        """
        Handle received events.
        
        Args:
            event: The received event
        """
        self._received_event = event
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node waits for and processes events from the EventBus.
        
        Args:
            shared: The shared store for storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        import threading
        import time
        
        # Reset the received event
        self._received_event = None
        
        # Subscribe to the event
        self.event_bus.subscribe(
            self.event_type, 
            self._event_handler,
            self.is_pattern
        )
        
        try:
            # Wait for the event or timeout
            start_time = time.time()
            while self._received_event is None:
                if self.timeout and time.time() - start_time > self.timeout:
                    return {"received": False, "timed_out": True}
                time.sleep(0.1)
            
            # Store the event in the shared store
            shared.set(self.output_key, self._received_event)
            
            return {
                "received": True,
                "event_id": self._received_event.event_id,
                "event_type": self._received_event.event_type,
                "timestamp": self._received_event.timestamp
            }
        finally:
            # Unsubscribe from the event
            self.event_bus.unsubscribe(
                self.event_type, 
                self._event_handler,
                self.is_pattern
            )


class EventDrivenBranchNode(Node):
    """
    Node for branching flow execution based on events.
    
    This node allows flows to take different paths based on which events
    are received from the EventBus.
    """
    
    def __init__(
        self, 
        event_bus: EventBus,
        event_branches: Dict[str, Node],
        default_branch: Optional[Node] = None,
        name: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> None:
        """
        Initialize an event-driven branch node.
        
        Args:
            event_bus: The EventBus to listen to
            event_branches: Mapping of event types to next nodes
            default_branch: Optional node to transition to if no matching event is received
            name: Optional name for the node
            timeout: Optional timeout in seconds to wait for events
        """
        super().__init__(name or "EventDrivenBranch")
        self.event_bus = event_bus
        self.event_branches = event_branches
        self.default_branch = default_branch
        self.timeout = timeout
        self._received_events: Dict[str, Event] = {}
    
    def _create_event_handler(self, event_type: str):
        """
        Create an event handler for a specific event type.
        
        Args:
            event_type: The event type to handle
            
        Returns:
            An event handler function
        """
        def handler(event: Event):
            self._received_events[event_type] = event
        return handler
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node waits for events and determines the next branch based on
        which event is received first.
        
        Args:
            shared: The shared store for accessing and storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        import threading
        import time
        
        # Reset received events
        self._received_events = {}
        
        # Subscribe to all event types
        handlers = {}
        for event_type in self.event_branches.keys():
            handler = self._create_event_handler(event_type)
            handlers[event_type] = handler
            self.event_bus.subscribe(event_type, handler)
        
        try:
            # Wait for any event or timeout
            start_time = time.time()
            while not self._received_events:
                if self.timeout and time.time() - start_time > self.timeout:
                    # Timeout occurred, use default branch if available
                    if self.default_branch:
                        self._next_nodes = [self.default_branch]
                    return {"branched": False, "timed_out": True}
                time.sleep(0.1)
            
            # Determine which event was received first
            first_event_type = next(iter(self._received_events.keys()))
            first_event = self._received_events[first_event_type]
            
            # Set the next node based on the received event
            next_node = self.event_branches[first_event_type]
            self._next_nodes = [next_node]
            
            # Store the event in the shared store
            shared.set(f"event_{first_event_type}", first_event)
            
            return {
                "branched": True,
                "branch_taken": first_event_type,
                "event_id": first_event.event_id,
                "timestamp": first_event.timestamp
            }
        finally:
            # Unsubscribe from all event types
            for event_type, handler in handlers.items():
                self.event_bus.unsubscribe(event_type, handler)
