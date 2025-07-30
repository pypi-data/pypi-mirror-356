"""
Base classes for Nüm Agents plugins.

This module defines the base classes that all Nüm Agents plugins should inherit from,
as well as the manifest structure for plugin metadata.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Type, Union

from num_agents.core import Node
from num_agents.univers.univers_catalog_loader import UniversCatalogEntry


@dataclass
class PluginManifest:
    """
    Manifest for a Nüm Agents plugin.
    
    This class defines the metadata for a plugin, including its name, version,
    description, and the components it provides.
    """
    
    name: str
    """The name of the plugin."""
    
    version: str
    """The version of the plugin (semantic versioning recommended)."""
    
    description: str
    """A brief description of the plugin."""
    
    author: str
    """The author or organization that created the plugin."""
    
    website: Optional[str] = None
    """Optional URL to the plugin's website or repository."""
    
    license: str = "Proprietary"
    """The license under which the plugin is distributed."""
    
    requires: List[str] = field(default_factory=list)
    """List of dependencies (other plugins or Python packages) required by this plugin."""
    
    min_sdk_version: Optional[str] = None
    """Minimum version of the Nüm Agents SDK required by this plugin."""
    
    max_sdk_version: Optional[str] = None
    """Maximum version of the Nüm Agents SDK compatible with this plugin."""
    
    tags: List[str] = field(default_factory=list)
    """Tags for categorizing the plugin."""
    
    universes: List[str] = field(default_factory=list)
    """List of universes provided by this plugin."""
    
    modules: List[str] = field(default_factory=list)
    """List of modules provided by this plugin."""
    
    node_types: List[str] = field(default_factory=list)
    """List of node types provided by this plugin."""


class PluginBase(ABC):
    """
    Base class for all Nüm Agents plugins.
    
    This abstract class defines the interface that all plugins must implement
    to be compatible with the Nüm Agents SDK.
    """
    
    @property
    @abstractmethod
    def manifest(self) -> PluginManifest:
        """
        Get the plugin's manifest.
        
        Returns:
            The plugin's manifest
        """
        pass
    
    @abstractmethod
    def initialize(self) -> None:
        """
        Initialize the plugin.
        
        This method is called when the plugin is first loaded.
        It should perform any necessary setup, such as registering components.
        """
        pass
    
    @abstractmethod
    def get_universes(self) -> Dict[str, UniversCatalogEntry]:
        """
        Get the universes provided by this plugin.
        
        Returns:
            A dictionary mapping universe names to UniversCatalogEntry objects
        """
        pass
    
    @abstractmethod
    def get_node_types(self) -> Dict[str, Type[Node]]:
        """
        Get the node types provided by this plugin.
        
        Returns:
            A dictionary mapping node type names to Node classes
        """
        pass
    
    def shutdown(self) -> None:
        """
        Shut down the plugin.
        
        This method is called when the plugin is being unloaded.
        It should perform any necessary cleanup.
        
        By default, this method does nothing. Plugins should override it
        if they need to perform cleanup operations.
        """
        pass
