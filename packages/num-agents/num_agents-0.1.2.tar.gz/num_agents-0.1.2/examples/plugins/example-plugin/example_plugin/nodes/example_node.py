"""
Example node implementation.

This module provides the ExampleNode class, which is an example of a custom node
that can be provided by a plugin.
"""

from typing import Any, Dict

from num_agents.core import Node, SharedStore


class ExampleNode(Node):
    """
    Example node implementation.
    
    This node demonstrates how to create a custom node that can be provided by a plugin.
    It simply adds a message to the shared store.
    """
    
    def __init__(self) -> None:
        """Initialize the node."""
        super().__init__("ExampleNode")
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        Args:
            shared: The shared store for accessing and storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Add a message to the shared store
        shared.set("example_message", "Hello from ExampleNode!")
        
        # Log that the node was executed
        print(f"[{self.name}] Executed successfully")
        
        # Return success status
        return {
            "status": "success",
            "message": "Example node executed successfully"
        }
