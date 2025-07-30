"""
Universe catalog loader for the Nüm Agents SDK.

This module provides functionality for loading and parsing the universe catalog,
which defines the available universes and their associated modules.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Any, Union

import yaml


@dataclass
class UniversCatalogEntry:
    """
    Entry in the universe catalog.
    
    This class represents an entry in the universe catalog, which defines
    a universe and its associated modules.
    """
    
    name: str
    """The name of the universe."""
    
    description: str
    """A brief description of the universe."""
    
    modules: List[str]
    """List of modules provided by this universe."""
    
    version: Optional[str] = None
    """Optional version of the universe."""
    
    author: Optional[str] = None
    """Optional author of the universe."""
    
    tags: List[str] = None
    """Optional tags for the universe."""


class UniversCatalogLoader:
    """
    Loader for the universe catalog.
    
    This class is responsible for loading and parsing the universe catalog YAML file,
    which defines the available universes and their associated modules.
    """
    
    def __init__(
        self,
        catalog_path: Optional[str] = None,
        plugin_manager: Optional[Any] = None
    ) -> None:
        """
        Initialize the universe catalog loader.
        
        Args:
            catalog_path: Optional path to the universe catalog YAML file.
                          If not provided, the default path will be used.
            plugin_manager: Optional plugin manager instance to use for loading
                           plugin-provided universes.
        """
        self.catalog_path = catalog_path or self._get_default_catalog_path()
        self._catalog: Dict[str, Any] = {}
        self._plugin_manager = plugin_manager
        self._plugin_universes: Dict[str, UniversCatalogEntry] = {}
    
    @staticmethod
    def _get_default_catalog_path() -> str:
        """
        Get the default path to the universe catalog YAML file.
        
        Returns:
            The default path to the universe catalog YAML file
        """
        # Try to find the catalog in the config directory relative to the package
        package_dir = Path(__file__).parent.parent.parent
        default_path = os.path.join(package_dir, "config", "univers_catalog.yaml")
        
        if os.path.exists(default_path):
            return default_path
        
        # If not found, check if it's in the current working directory
        cwd_path = os.path.join(os.getcwd(), "config", "univers_catalog.yaml")
        if os.path.exists(cwd_path):
            return cwd_path
        
        # If still not found, return the default path anyway (it will fail when loaded)
        return default_path
    
    def load(self) -> Dict[str, Any]:
        """
        Load the universe catalog from the YAML file.
        
        Returns:
            The parsed universe catalog as a dictionary
            
        Raises:
            FileNotFoundError: If the catalog file doesn't exist
            yaml.YAMLError: If the catalog file is not valid YAML
        """
        if not os.path.exists(self.catalog_path):
            raise FileNotFoundError(f"Universe catalog not found at {self.catalog_path}")
        
        with open(self.catalog_path, "r") as f:
            self._catalog = yaml.safe_load(f)
        
        # Load plugin universes if a plugin manager is available
        if self._plugin_manager is not None:
            self._load_plugin_universes()
        
        return self._catalog
        
    def _load_plugin_universes(self) -> None:
        """
        Load universes provided by plugins.
        
        This method loads universes from all registered plugins using the plugin manager.
        """
        if not hasattr(self._plugin_manager, 'universes'):
            return
            
        self._plugin_universes = self._plugin_manager.universes
    
    def get_universes(self) -> List[str]:
        """
        Get the list of available universes.
        
        Returns:
            A list of universe names
        """
        if not self._catalog:
            self.load()
        
        # Get universes from the catalog
        catalog_universes = list(self._catalog.get("univers_catalog", {}).keys())
        
        # Add universes from plugins
        plugin_universes = list(self._plugin_universes.keys())
        
        # Combine and return unique universes
        return list(set(catalog_universes + plugin_universes))
    
    def get_modules_for_universe(self, universe: str) -> List[str]:
        """
        Get the list of modules for a specific universe.
        
        Args:
            universe: The name of the universe
            
        Returns:
            A list of module names for the specified universe
            
        Raises:
            KeyError: If the universe doesn't exist in the catalog or plugins
        """
        if not self._catalog:
            self.load()
        
        # Check if the universe is provided by a plugin
        if universe in self._plugin_universes:
            return self._plugin_universes[universe].modules
        
        # Otherwise, check the catalog
        universe_data = self._catalog.get("univers_catalog", {}).get(universe)
        if not universe_data:
            raise KeyError(f"Universe '{universe}' not found in catalog or plugins")
        
        return universe_data.get("modules", [])
    
    def resolve_modules(self, universes: List[str]) -> Set[str]:
        """
        Resolve all modules for a list of universes.
        
        Args:
            universes: A list of universe names
            
        Returns:
            A set of all module names from the specified universes
        """
        if not self._catalog:
            self.load()
        
        modules = set()
        for universe in universes:
            try:
                universe_modules = self.get_modules_for_universe(universe)
                modules.update(universe_modules)
            except KeyError:
                # Skip universes that don't exist
                continue
        
        return modules
        
    def get_universe_entry(self, universe: str) -> Union[Dict[str, Any], UniversCatalogEntry]:
        """
        Get the full entry for a specific universe.
        
        Args:
            universe: The name of the universe
            
        Returns:
            The universe entry as a dictionary or UniversCatalogEntry
            
        Raises:
            KeyError: If the universe doesn't exist in the catalog or plugins
        """
        if not self._catalog:
            self.load()
        
        # Check if the universe is provided by a plugin
        if universe in self._plugin_universes:
            return self._plugin_universes[universe]
        
        # Otherwise, check the catalog
        universe_data = self._catalog.get("univers_catalog", {}).get(universe)
        if not universe_data:
            raise KeyError(f"Universe '{universe}' not found in catalog or plugins")
        
        return universe_data
