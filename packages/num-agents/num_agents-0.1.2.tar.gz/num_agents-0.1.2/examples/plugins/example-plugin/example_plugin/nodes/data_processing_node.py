"""
Data processing node implementation.

This module provides the DataProcessingNode class, which is an example of a custom node
that can be provided by a plugin and performs data processing operations.
"""

from typing import Any, Dict, List, Optional

from num_agents.core import Node, SharedStore


class DataProcessingNode(Node):
    """
    Data processing node implementation.
    
    This node demonstrates how to create a custom data processing node
    that can be provided by a plugin. It processes data from the shared store
    and adds the processed data back to the shared store.
    """
    
    def __init__(self) -> None:
        """Initialize the node."""
        super().__init__("DataProcessingNode")
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        Args:
            shared: The shared store for accessing and storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Get data from the shared store
        data = shared.get("input_data")
        
        # If no data is provided, use a default value
        if data is None:
            data = ["example", "data", "to", "process"]
            shared.set("input_data", data)
        
        # Process the data (in this example, convert strings to uppercase)
        processed_data = self._process_data(data)
        
        # Store the processed data in the shared store
        shared.set("processed_data", processed_data)
        
        # Log that the node was executed
        print(f"[{self.name}] Processed {len(data)} items")
        
        # Return success status and summary
        return {
            "status": "success",
            "items_processed": len(data),
            "message": "Data processing completed successfully"
        }
    
    def _process_data(self, data: List[str]) -> List[str]:
        """
        Process the input data.
        
        In this example, we simply convert strings to uppercase.
        In a real-world scenario, this could be any data processing operation.
        
        Args:
            data: The input data to process
            
        Returns:
            The processed data
        """
        if not data:
            return []
        
        # Convert strings to uppercase
        return [item.upper() if isinstance(item, str) else item for item in data]
