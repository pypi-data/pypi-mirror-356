"""
Notification Node for the Event-Driven Agent example.

This node handles sending notifications and demonstrates
integration with the EventBus.
"""

from typing import Any, Dict

from num_agents.core import Node, SharedStore
from num_agents.eventbus.event import Event, EventTypes
from num_agents.eventbus.eventbus import EventBus


class NotificationNode(Node):
    """
    Node for sending notifications.
    
    This node simulates sending notifications and demonstrates
    how to publish events to the EventBus.
    """
    
    def __init__(self, name: str = None, event_bus: EventBus = None) -> None:
        """
        Initialize a notification node.
        
        Args:
            name: Optional name for the node
            event_bus: Optional EventBus instance for publishing events
        """
        super().__init__(name or "NotificationNode")
        self.event_bus = event_bus
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node simulates sending a notification and publishes
        a notification event to the EventBus.
        
        Args:
            shared: The shared store for accessing and storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Get the user input from the shared store
        user_input = shared.get("user_input", "")
        
        # Create a notification message
        notification_message = self._create_notification_message(user_input)
        
        # Store the notification in the shared store
        shared.set("notification_message", notification_message)
        
        # Simulate sending the notification
        self._send_notification(notification_message)
        
        # If we have an event bus, publish a notification event
        if self.event_bus:
            self.event_bus.publish(
                Event(
                    event_type=EventTypes.custom("system.notification"),
                    payload={
                        "message": notification_message,
                        "type": "console",
                        "timestamp": "2025-06-18T01:57:49+02:00"  # Would normally use datetime.now()
                    },
                    source=self.name
                )
            )
        
        return {
            "notification_sent": True,
            "notification_message": notification_message
        }
    
    def _create_notification_message(self, user_input: str) -> str:
        """
        Create a notification message based on the user input.
        
        Args:
            user_input: The user's input string
            
        Returns:
            The notification message
        """
        # Extract keywords from the user input to personalize the notification
        if "remind" in user_input.lower():
            return f"REMINDER: {user_input}"
        elif "alert" in user_input.lower():
            return f"ALERT: {user_input}"
        else:
            return f"NOTIFICATION: {user_input}"
    
    def _send_notification(self, message: str) -> None:
        """
        Simulate sending a notification.
        
        In a real application, this might involve sending an email,
        a push notification, or another form of alert.
        
        Args:
            message: The notification message to send
        """
        # In a real application, this would use an external service
        # to send the notification
        print(f"\n[NOTIFICATION] {message}\n")
