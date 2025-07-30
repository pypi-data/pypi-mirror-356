"""
Plugin implementation for the example plugin.

This module provides the ExamplePlugin class, which implements the PluginBase interface
and serves as an example of how to create a plugin for the Nüm Agents SDK.
"""

from typing import Dict, Type

from num_agents.core import Node
from num_agents.plugins.plugin_base import PluginBase, PluginManifest
from num_agents.univers.univers_catalog_loader import UniversCatalogEntry

from example_plugin.nodes.example_node import ExampleNode
from example_plugin.nodes.data_processing_node import DataProcessingNode


class ExamplePlugin(PluginBase):
    """
    Example plugin implementation for Nüm Agents SDK.
    
    This class demonstrates how to implement the PluginBase interface
    to create a plugin for the Nüm Agents SDK.
    """
    
    def get_manifest(self) -> PluginManifest:
        """
        Get the plugin manifest.
        
        Returns:
            The plugin manifest with metadata about the plugin
        """
        return PluginManifest(
            name="example-plugin",
            version="0.1.0",
            description="Example plugin for Nüm Agents SDK",
            author="Nüm Agents Team",
            website="https://github.com/Creativityliberty/numagents"
        )
    
    def initialize(self) -> None:
        """
        Initialize the plugin.
        
        This method is called when the plugin is loaded.
        """
        print("Initializing Example Plugin...")
    
    def get_universes(self) -> Dict[str, UniversCatalogEntry]:
        """
        Get the universes provided by this plugin.
        
        Returns:
            A dictionary mapping universe names to UniversCatalogEntry objects
        """
        return {
            "ExampleUnivers": UniversCatalogEntry(
                name="ExampleUnivers",
                description="Example universe provided by the example plugin",
                modules=["ExampleNode", "DataProcessingNode"],
                version="0.1.0",
                author="Nüm Agents Team",
                tags=["example", "demo"]
            )
        }
    
    def get_node_types(self) -> Dict[str, Type[Node]]:
        """
        Get the node types provided by this plugin.
        
        Returns:
            A dictionary mapping node names to node classes
        """
        return {
            "ExampleNode": ExampleNode,
            "DataProcessingNode": DataProcessingNode
        }
