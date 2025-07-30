"""
User Input Node for the Event-Driven Agent example.

This node handles user input and determines the type of request.
"""

from typing import Any, Dict

from num_agents.core import Node, SharedStore
from num_agents.eventbus.event import EventTypes
from num_agents.eventbus.eventbus import EventBus


class UserInputNode(Node):
    """
    Node for handling user input and determining the request type.
    
    This node prompts the user for input, stores it in the shared store,
    and determines the type of request based on keywords.
    """
    
    def __init__(self, name: str = None, event_bus: EventBus = None) -> None:
        """
        Initialize a user input node.
        
        Args:
            name: Optional name for the node
            event_bus: Optional EventBus instance for publishing events
        """
        super().__init__(name or "UserInputNode")
        self.event_bus = event_bus
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node prompts the user for input and determines the request type.
        
        Args:
            shared: The shared store for storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Prompt the user for input
        user_input = input("\nWhat would you like to do? ")
        
        # Store the user input in the shared store
        shared.set("user_input", user_input)
        
        # Determine the request type based on keywords
        request_type = self._determine_request_type(user_input)
        shared.set("request_type", request_type)
        
        # If we have an event bus, publish an event for the request type
        if self.event_bus and request_type != "unknown":
            from num_agents.eventbus.event import Event
            
            self.event_bus.publish(
                Event(
                    event_type=f"request.{request_type}",
                    payload={"user_input": user_input},
                    source=self.name
                )
            )
        
        return {
            "user_input": user_input,
            "request_type": request_type
        }
    
    def _determine_request_type(self, user_input: str) -> str:
        """
        Determine the type of request based on keywords in the user input.
        
        Args:
            user_input: The user's input string
            
        Returns:
            The determined request type (process, notify, or unknown)
        """
        user_input = user_input.lower()
        
        if any(keyword in user_input for keyword in ["process", "analyze", "compute", "calculate"]):
            return "process"
        elif any(keyword in user_input for keyword in ["notify", "alert", "remind", "send"]):
            return "notify"
        else:
            return "unknown"
