"""
Plugin Manager for the Nüm Agents SDK.

This module provides the PluginManager class, which is responsible for
discovering, loading, and managing plugins for the Nüm Agents SDK.
"""

import importlib
import logging
import os
import sys
from importlib.metadata import entry_points
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Type, Union

from num_agents.core import Node
from num_agents.plugins.plugin_base import PluginBase, PluginManifest
from num_agents.univers.univers_catalog_loader import UniversCatalogEntry


class PluginManager:
    """
    Manager for Nüm Agents plugins.
    
    This class is responsible for discovering, loading, and managing
    plugins for the Nüm Agents SDK.
    """
    
    def __init__(
        self,
        entry_point_group: str = "num_agents.plugins",
        plugin_dirs: Optional[List[str]] = None,
        auto_discover: bool = True
    ) -> None:
        """
        Initialize the plugin manager.
        
        Args:
            entry_point_group: The entry point group to use for discovering plugins
            plugin_dirs: Optional list of directories to search for plugins
            auto_discover: Whether to automatically discover plugins on initialization
        """
        self.entry_point_group = entry_point_group
        self.plugin_dirs = plugin_dirs or []
        
        # Add default plugin directories if they exist
        self._add_default_plugin_dirs()
        
        # Initialize plugin storage
        self.plugins: Dict[str, PluginBase] = {}
        self.universes: Dict[str, UniversCatalogEntry] = {}
        self.node_types: Dict[str, Type[Node]] = {}
        
        # Discover plugins if auto_discover is True
        if auto_discover:
            self.discover_plugins()
    
    def _add_default_plugin_dirs(self) -> None:
        """
        Add default plugin directories to the list of plugin directories.
        
        This method adds the following directories if they exist:
        - ~/.num_agents/plugins
        - <SDK_INSTALL_DIR>/plugins
        """
        # Add user plugin directory (~/.num_agents/plugins)
        user_plugin_dir = os.path.expanduser("~/.num_agents/plugins")
        if os.path.isdir(user_plugin_dir):
            self.plugin_dirs.append(user_plugin_dir)
        
        # Add SDK plugin directory (<SDK_INSTALL_DIR>/plugins)
        try:
            import num_agents
            sdk_dir = os.path.dirname(os.path.abspath(num_agents.__file__))
            sdk_plugin_dir = os.path.join(sdk_dir, "plugins")
            if os.path.isdir(sdk_plugin_dir) and sdk_plugin_dir not in self.plugin_dirs:
                self.plugin_dirs.append(sdk_plugin_dir)
        except ImportError:
            pass
    
    def discover_plugins(self) -> Dict[str, PluginBase]:
        """
        Discover available plugins.
        
        This method discovers plugins from both entry points and plugin directories.
        
        Returns:
            A dictionary mapping plugin names to plugin instances
        """
        # Discover plugins from entry points
        self._discover_from_entry_points()
        
        # Discover plugins from directories
        self._discover_from_dirs()
        
        return self.plugins
    
    def _discover_from_entry_points(self) -> None:
        """
        Discover plugins from entry points.
        
        This method uses importlib.metadata.entry_points to find plugins
        that have registered with the specified entry point group.
        """
        try:
            # For Python 3.10+
            try:
                eps = entry_points(group=self.entry_point_group)
            except TypeError:
                # For Python 3.8, 3.9 (entry_points() doesn't take kwargs)
                all_eps = entry_points()
                eps = all_eps.get(self.entry_point_group, [])
            
            for ep in eps:
                try:
                    plugin_class = ep.load()
                    plugin_instance = plugin_class()
                    
                    if not isinstance(plugin_instance, PluginBase):
                        logging.warning(
                            f"Plugin {ep.name} does not implement PluginBase, skipping."
                        )
                        continue
                    
                    self._register_plugin(plugin_instance)
                    logging.info(f"Loaded plugin {ep.name} from entry point.")
                
                except Exception as e:
                    logging.error(f"Error loading plugin {ep.name} from entry point: {e}")
        
        except Exception as e:
            logging.error(f"Error discovering plugins from entry points: {e}")
    
    def _discover_from_dirs(self) -> None:
        """
        Discover plugins from directories.
        
        This method searches the specified plugin directories for Python modules
        that contain plugin classes.
        """
        for plugin_dir in self.plugin_dirs:
            if not os.path.isdir(plugin_dir):
                continue
            
            # Add the plugin directory to sys.path temporarily
            sys.path.insert(0, plugin_dir)
            
            try:
                # Iterate over all Python files in the directory
                for item in os.listdir(plugin_dir):
                    if item.endswith(".py") and not item.startswith("__"):
                        module_name = item[:-3]  # Remove .py extension
                        
                        try:
                            # Import the module
                            module = importlib.import_module(module_name)
                            
                            # Look for plugin classes in the module
                            for attr_name in dir(module):
                                attr = getattr(module, attr_name)
                                
                                # Check if it's a class that inherits from PluginBase
                                if (
                                    isinstance(attr, type)
                                    and issubclass(attr, PluginBase)
                                    and attr is not PluginBase
                                ):
                                    try:
                                        plugin_instance = attr()
                                        self._register_plugin(plugin_instance)
                                        logging.info(
                                            f"Loaded plugin {plugin_instance.manifest.name} "
                                            f"from directory {plugin_dir}."
                                        )
                                    except Exception as e:
                                        logging.error(
                                            f"Error instantiating plugin class {attr_name} "
                                            f"from module {module_name}: {e}"
                                        )
                        
                        except Exception as e:
                            logging.error(
                                f"Error loading module {module_name} from {plugin_dir}: {e}"
                            )
            
            finally:
                # Remove the plugin directory from sys.path
                if plugin_dir in sys.path:
                    sys.path.remove(plugin_dir)
    
    def _register_plugin(self, plugin: PluginBase) -> None:
        """
        Register a plugin with the plugin manager.
        
        This method initializes the plugin and registers its components.
        
        Args:
            plugin: The plugin to register
        """
        manifest = plugin.manifest
        
        # Check if a plugin with the same name is already registered
        if manifest.name in self.plugins:
            logging.warning(
                f"Plugin {manifest.name} is already registered, skipping."
            )
            return
        
        # Initialize the plugin
        try:
            plugin.initialize()
        except Exception as e:
            logging.error(f"Error initializing plugin {manifest.name}: {e}")
            return
        
        # Register the plugin
        self.plugins[manifest.name] = plugin
        
        # Register the plugin's universes
        universes = plugin.get_universes()
        for name, universe in universes.items():
            if name in self.universes:
                logging.warning(
                    f"Universe {name} from plugin {manifest.name} "
                    f"conflicts with an existing universe, skipping."
                )
            else:
                self.universes[name] = universe
        
        # Register the plugin's node types
        node_types = plugin.get_node_types()
        for name, node_type in node_types.items():
            if name in self.node_types:
                logging.warning(
                    f"Node type {name} from plugin {manifest.name} "
                    f"conflicts with an existing node type, skipping."
                )
            else:
                self.node_types[name] = node_type
    
    def get_plugin(self, name: str) -> Optional[PluginBase]:
        """
        Get a plugin by name.
        
        Args:
            name: The name of the plugin to get
            
        Returns:
            The plugin instance, or None if not found
        """
        return self.plugins.get(name)
    
    def get_universe(self, name: str) -> Optional[UniversCatalogEntry]:
        """
        Get a universe by name.
        
        Args:
            name: The name of the universe to get
            
        Returns:
            The universe entry, or None if not found
        """
        return self.universes.get(name)
    
    def get_node_type(self, name: str) -> Optional[Type[Node]]:
        """
        Get a node type by name.
        
        Args:
            name: The name of the node type to get
            
        Returns:
            The node type class, or None if not found
        """
        return self.node_types.get(name)
    
    def shutdown(self) -> None:
        """
        Shut down all plugins.
        
        This method calls the shutdown method on all registered plugins
        and clears the plugin registry.
        """
        for name, plugin in list(self.plugins.items()):
            try:
                plugin.shutdown()
            except Exception as e:
                logging.error(f"Error shutting down plugin {name}: {e}")
        
        # Clear the plugin registry
        self.plugins.clear()
        self.universes.clear()
        self.node_types.clear()
