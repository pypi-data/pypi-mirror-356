"""
Example universe implementation.

This module provides the ExampleUnivers class, which is an example of a custom universe
that can be provided by a plugin.
"""

from typing import List


class ExampleUnivers:
    """
    Example universe implementation.
    
    This class demonstrates how to create a custom universe that can be provided by a plugin.
    It defines the modules available in this universe.
    """
    
    @staticmethod
    def get_modules() -> List[str]:
        """
        Get the modules available in this universe.
        
        Returns:
            A list of module names
        """
        return ["ExampleNode", "DataProcessingNode"]
    
    @staticmethod
    def get_description() -> str:
        """
        Get a description of this universe.
        
        Returns:
            A description of the universe
        """
        return "Example universe provided by the example plugin"
