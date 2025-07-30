"""
Utility functions for working with the EventBus.

This module provides helper functions for common EventBus operations.
"""

from typing import Any, Callable, Dict, List, Optional, Pattern, Union

from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus


def create_event(
    event_type: str,
    payload: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None
) -> Event:
    """
    Create a new event with the specified parameters.
    
    Args:
        event_type: The type of event to create
        payload: Optional payload for the event
        metadata: Optional metadata for the event
        source: Optional source identifier for the event
        
    Returns:
        A new Event instance
    """
    return Event(
        event_type=event_type,
        payload=payload or {},
        metadata=metadata or {},
        source=source
    )


def publish_event(
    event_bus: EventBus,
    event_type: str,
    payload: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    source: Optional[str] = None
) -> Event:
    """
    Create and publish an event to the EventBus.
    
    Args:
        event_bus: The EventBus to publish to
        event_type: The type of event to publish
        payload: Optional payload for the event
        metadata: Optional metadata for the event
        source: Optional source identifier for the event
        
    Returns:
        The published Event instance
    """
    event = create_event(event_type, payload, metadata, source)
    event_bus.publish(event)
    return event


def publish_system_event(
    event_bus: EventBus,
    event_type: str,
    payload: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Event:
    """
    Create and publish a system event to the EventBus.
    
    Args:
        event_bus: The EventBus to publish to
        event_type: The type of system event to publish
        payload: Optional payload for the event
        metadata: Optional metadata for the event
        
    Returns:
        The published Event instance
    """
    return publish_event(
        event_bus=event_bus,
        event_type=event_type,
        payload=payload,
        metadata=metadata,
        source="System"
    )


def publish_flow_started_event(
    event_bus: EventBus,
    flow_name: str,
    flow_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Event:
    """
    Publish a flow started event to the EventBus.
    
    Args:
        event_bus: The EventBus to publish to
        flow_name: The name of the flow that started
        flow_id: Optional ID of the flow
        metadata: Optional metadata for the event
        
    Returns:
        The published Event instance
    """
    return publish_event(
        event_bus=event_bus,
        event_type=EventTypes.FLOW_STARTED,
        payload={"flow_name": flow_name, "flow_id": flow_id},
        metadata=metadata,
        source="Flow"
    )


def publish_flow_completed_event(
    event_bus: EventBus,
    flow_name: str,
    flow_id: Optional[str] = None,
    results: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Event:
    """
    Publish a flow completed event to the EventBus.
    
    Args:
        event_bus: The EventBus to publish to
        flow_name: The name of the flow that completed
        flow_id: Optional ID of the flow
        results: Optional results from the flow execution
        metadata: Optional metadata for the event
        
    Returns:
        The published Event instance
    """
    return publish_event(
        event_bus=event_bus,
        event_type=EventTypes.FLOW_COMPLETED,
        payload={"flow_name": flow_name, "flow_id": flow_id, "results": results or {}},
        metadata=metadata,
        source="Flow"
    )


def publish_node_started_event(
    event_bus: EventBus,
    node_name: str,
    node_id: str,
    flow_name: Optional[str] = None,
    flow_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Event:
    """
    Publish a node started event to the EventBus.
    
    Args:
        event_bus: The EventBus to publish to
        node_name: The name of the node that started
        node_id: The ID of the node
        flow_name: Optional name of the flow containing the node
        flow_id: Optional ID of the flow
        metadata: Optional metadata for the event
        
    Returns:
        The published Event instance
    """
    return publish_event(
        event_bus=event_bus,
        event_type=EventTypes.NODE_STARTED,
        payload={
            "node_name": node_name,
            "node_id": node_id,
            "flow_name": flow_name,
            "flow_id": flow_id
        },
        metadata=metadata,
        source="Node"
    )


def publish_node_completed_event(
    event_bus: EventBus,
    node_name: str,
    node_id: str,
    results: Dict[str, Any],
    flow_name: Optional[str] = None,
    flow_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Event:
    """
    Publish a node completed event to the EventBus.
    
    Args:
        event_bus: The EventBus to publish to
        node_name: The name of the node that completed
        node_id: The ID of the node
        results: Results from the node execution
        flow_name: Optional name of the flow containing the node
        flow_id: Optional ID of the flow
        metadata: Optional metadata for the event
        
    Returns:
        The published Event instance
    """
    return publish_event(
        event_bus=event_bus,
        event_type=EventTypes.NODE_COMPLETED,
        payload={
            "node_name": node_name,
            "node_id": node_id,
            "flow_name": flow_name,
            "flow_id": flow_id,
            "results": results
        },
        metadata=metadata,
        source="Node"
    )


def publish_data_event(
    event_bus: EventBus,
    data_type: str,
    data_key: str,
    data_value: Any,
    operation: str = "updated",
    source: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Event:
    """
    Publish a data event to the EventBus.
    
    Args:
        event_bus: The EventBus to publish to
        data_type: The type of data (e.g., "user", "system", "model")
        data_key: The key of the data that was modified
        data_value: The new value of the data
        operation: The operation performed on the data (created, updated, deleted)
        source: Optional source identifier for the event
        metadata: Optional metadata for the event
        
    Returns:
        The published Event instance
    """
    event_type_map = {
        "created": EventTypes.DATA_CREATED,
        "updated": EventTypes.DATA_UPDATED,
        "deleted": EventTypes.DATA_DELETED
    }
    
    event_type = event_type_map.get(operation.lower(), EventTypes.DATA_UPDATED)
    
    return publish_event(
        event_bus=event_bus,
        event_type=event_type,
        payload={
            "data_type": data_type,
            "data_key": data_key,
            "data_value": data_value,
            "operation": operation
        },
        metadata=metadata,
        source=source or "DataManager"
    )
