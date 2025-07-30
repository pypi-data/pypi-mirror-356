"""
EventBus implementation for the Nüm Agents SDK.

This module provides the EventBus class, which is responsible for
event publishing and subscription.
"""

import asyncio
import logging
import re
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable, Dict, List, Optional, Pattern, Set, Union

from num_agents.eventbus.event import Event


# Type definitions
EventHandler = Callable[[Event], None]
AsyncEventHandler = Callable[[Event], asyncio.coroutine]


class EventBus:
    """
    Event bus for publishing and subscribing to events.
    
    The EventBus provides a publish-subscribe pattern for communication
    between components in the Nüm Agents SDK.
    """
    
    def __init__(self) -> None:
        """Initialize a new event bus."""
        self._subscribers: Dict[str, List[EventHandler]] = defaultdict(list)
        self._pattern_subscribers: List[tuple[Pattern, EventHandler]] = []
        self._executor = ThreadPoolExecutor()
        self._logger = logging.getLogger(__name__)
    
    def subscribe(
        self, 
        event_type: str, 
        handler: EventHandler, 
        is_pattern: bool = False
    ) -> None:
        """
        Subscribe to events of a specific type.
        
        Args:
            event_type: The event type to subscribe to
            handler: The function to call when an event of this type is published
            is_pattern: If True, event_type is treated as a regex pattern
        """
        if is_pattern:
            pattern = re.compile(event_type)
            self._pattern_subscribers.append((pattern, handler))
        else:
            self._subscribers[event_type].append(handler)
        
        self._logger.debug(
            f"Subscribed to {'pattern' if is_pattern else 'event'}: {event_type}"
        )
    
    def unsubscribe(
        self, 
        event_type: str, 
        handler: Optional[EventHandler] = None, 
        is_pattern: bool = False
    ) -> None:
        """
        Unsubscribe from events of a specific type.
        
        Args:
            event_type: The event type to unsubscribe from
            handler: The handler to unsubscribe. If None, all handlers for this event type are removed.
            is_pattern: If True, event_type is treated as a regex pattern
        """
        if is_pattern:
            if handler is None:
                # Remove all handlers with matching pattern
                self._pattern_subscribers = [
                    (p, h) for p, h in self._pattern_subscribers 
                    if p.pattern != event_type
                ]
            else:
                # Remove specific handler with matching pattern
                self._pattern_subscribers = [
                    (p, h) for p, h in self._pattern_subscribers 
                    if not (p.pattern == event_type and h == handler)
                ]
        else:
            if handler is None:
                # Remove all handlers for this event type
                if event_type in self._subscribers:
                    del self._subscribers[event_type]
            else:
                # Remove specific handler for this event type
                if event_type in self._subscribers:
                    self._subscribers[event_type] = [
                        h for h in self._subscribers[event_type] if h != handler
                    ]
    
    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: The event to publish
        """
        event_type = event.event_type
        
        # Call handlers for exact event type match
        for handler in self._subscribers.get(event_type, []):
            try:
                self._executor.submit(handler, event)
            except Exception as e:
                self._logger.error(f"Error in event handler for {event_type}: {e}")
        
        # Call handlers for pattern matches
        for pattern, handler in self._pattern_subscribers:
            if pattern.match(event_type):
                try:
                    self._executor.submit(handler, event)
                except Exception as e:
                    self._logger.error(f"Error in pattern handler for {event_type}: {e}")
        
        self._logger.debug(f"Published event: {event_type}")
    
    def publish_sync(self, event: Event) -> None:
        """
        Publish an event synchronously to all subscribers.
        
        This method blocks until all handlers have processed the event.
        
        Args:
            event: The event to publish
        """
        event_type = event.event_type
        
        # Call handlers for exact event type match
        for handler in self._subscribers.get(event_type, []):
            try:
                handler(event)
            except Exception as e:
                self._logger.error(f"Error in event handler for {event_type}: {e}")
        
        # Call handlers for pattern matches
        for pattern, handler in self._pattern_subscribers:
            if pattern.match(event_type):
                try:
                    handler(event)
                except Exception as e:
                    self._logger.error(f"Error in pattern handler for {event_type}: {e}")
        
        self._logger.debug(f"Published event synchronously: {event_type}")
    
    async def publish_async(self, event: Event) -> None:
        """
        Publish an event asynchronously to all subscribers.
        
        This method is designed to be used in async contexts.
        
        Args:
            event: The event to publish
        """
        event_type = event.event_type
        tasks = []
        
        # Create tasks for exact event type match
        for handler in self._subscribers.get(event_type, []):
            if asyncio.iscoroutinefunction(handler):
                tasks.append(handler(event))
            else:
                tasks.append(
                    asyncio.get_event_loop().run_in_executor(
                        self._executor, handler, event
                    )
                )
        
        # Create tasks for pattern matches
        for pattern, handler in self._pattern_subscribers:
            if pattern.match(event_type):
                if asyncio.iscoroutinefunction(handler):
                    tasks.append(handler(event))
                else:
                    tasks.append(
                        asyncio.get_event_loop().run_in_executor(
                            self._executor, handler, event
                        )
                    )
        
        # Wait for all tasks to complete
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self._logger.debug(f"Published event asynchronously: {event_type}")
    
    def get_event_types(self) -> Set[str]:
        """
        Get all event types with subscribers.
        
        Returns:
            A set of all event types that have subscribers
        """
        return set(self._subscribers.keys())
    
    def get_pattern_subscriptions(self) -> List[str]:
        """
        Get all pattern subscriptions.
        
        Returns:
            A list of all pattern strings that have subscribers
        """
        return [pattern.pattern for pattern, _ in self._pattern_subscribers]
