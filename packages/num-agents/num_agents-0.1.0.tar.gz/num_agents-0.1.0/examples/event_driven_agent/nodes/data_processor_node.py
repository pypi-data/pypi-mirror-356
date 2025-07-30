"""
Data Processor Node for the Event-Driven Agent example.

This node handles data processing tasks and demonstrates
integration with the Scheduler.
"""

from typing import Any, Dict

from num_agents.core import Node, SharedStore


class DataProcessorNode(Node):
    """
    Node for processing data.
    
    This node simulates data processing operations and demonstrates
    how to prepare data for scheduled processing.
    """
    
    def __init__(self, name: str = None) -> None:
        """
        Initialize a data processor node.
        
        Args:
            name: Optional name for the node
        """
        super().__init__(name or "DataProcessorNode")
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This node prepares data for processing by a scheduled task.
        
        Args:
            shared: The shared store for accessing and storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        # Get the user input from the shared store
        user_input = shared.get("user_input", "")
        
        # Prepare the data for processing
        # In a real application, this might involve more complex preprocessing
        prepared_data = self._prepare_data(user_input)
        
        # Store the prepared data in the shared store
        shared.set("prepared_data", prepared_data)
        
        return {
            "prepared_data": prepared_data,
            "ready_for_processing": True
        }
    
    def _prepare_data(self, data: str) -> str:
        """
        Prepare data for processing.
        
        Args:
            data: The raw data to prepare
            
        Returns:
            The prepared data
        """
        # In a real application, this might involve data cleaning,
        # normalization, or other preprocessing steps
        return data.strip()
    
    @staticmethod
    def process_data(data: str) -> Dict[str, Any]:
        """
        Process data (to be called by the scheduler).
        
        This is a static method that can be used as a callback
        for scheduled tasks.
        
        Args:
            data: The data to process
            
        Returns:
            The processing results
        """
        # In a real application, this might involve complex data processing,
        # machine learning predictions, or API calls
        
        # Simple example: convert to uppercase and count words
        processed_data = data.upper()
        word_count = len(data.split())
        
        return {
            "processed_data": processed_data,
            "word_count": word_count,
            "timestamp": "2025-06-18T01:57:49+02:00"  # Would normally use datetime.now()
        }
