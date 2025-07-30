"""
Plugin system for the Nüm Agents SDK.

This module provides the core functionality for discovering, loading,
and managing plugins for the Nüm Agents SDK.
"""

from num_agents.plugins.plugin_manager import PluginManager
from num_agents.plugins.plugin_base import PluginBase, PluginManifest

__all__ = ["PluginManager", "PluginBase", "PluginManifest"]
