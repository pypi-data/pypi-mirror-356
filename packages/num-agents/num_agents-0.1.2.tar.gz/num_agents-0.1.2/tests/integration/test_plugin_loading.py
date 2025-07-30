"""
Integration test for plugin loading and execution.
"""

import os
import sys
import unittest
from unittest.mock import patch
import tempfile
import shutil
from pathlib import Path

from num_agents.plugins.plugin_manager import PluginManager
from num_agents.eventbus.eventbus import EventBus
from num_agents.scheduler.scheduler import Scheduler


class TestPluginLoading(unittest.TestCase):
    """Integration test for plugin loading and execution."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for the test
        self.test_dir = tempfile.mkdtemp()
        
        # Create a plugins directory
        self.plugins_dir = os.path.join(self.test_dir, "plugins")
        os.makedirs(self.plugins_dir)
        
        # Create a test plugin
        self.plugin_dir = os.path.join(self.plugins_dir, "test_plugin")
        os.makedirs(self.plugin_dir)
        
        # Create plugin.yaml
        with open(os.path.join(self.plugin_dir, "plugin.yaml"), "w") as f:
            f.write("""
name: TestPlugin
version: 0.1.0
description: A test plugin for the Nüm Agents SDK
author: Test Author
entry_point: plugin.py
hooks:
  - name: initialize
    method: initialize
  - name: on_flow_start
    method: on_flow_start
  - name: on_flow_end
    method: on_flow_end
            """)
        
        # Create plugin.py
        with open(os.path.join(self.plugin_dir, "plugin.py"), "w") as f:
            f.write("""
from num_agents.plugins.plugin_base import PluginBase
from num_agents.eventbus.event import Event

class TestPlugin(PluginBase):
    def __init__(self):
        super().__init__()
        self.initialized = False
        self.flow_started = False
        self.flow_ended = False
        self.event_received = False
    
    def initialize(self, event_bus=None, scheduler=None):
        self.initialized = True
        self.event_bus = event_bus
        self.scheduler = scheduler
        
        # Subscribe to a test event
        if event_bus:
            event_bus.subscribe("test.plugin.event", self.handle_event)
        
        return {"status": "initialized"}
    
    def on_flow_start(self, flow_name, flow_id):
        self.flow_started = True
        return {"status": "flow_started", "flow_name": flow_name, "flow_id": flow_id}
    
    def on_flow_end(self, flow_name, flow_id, result):
        self.flow_ended = True
        return {"status": "flow_ended", "flow_name": flow_name, "flow_id": flow_id, "result": result}
    
    def handle_event(self, event):
        self.event_received = True
        
        # Publish a response event
        if self.event_bus:
            response_event = Event(
                event_type="test.plugin.response",
                payload={"message": "Response from plugin"},
                source="TestPlugin"
            )
            self.event_bus.publish(response_event)
        
        return True
            """)
        
        # Create an empty __init__.py
        with open(os.path.join(self.plugin_dir, "__init__.py"), "w") as f:
            f.write("")
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_plugin_loading(self):
        """Test loading a plugin."""
        # Create a plugin manager
        plugin_manager = PluginManager(plugins_dir=self.plugins_dir)
        
        # Load plugins
        plugins = plugin_manager.load_plugins()
        
        # Check that the plugin was loaded
        self.assertEqual(len(plugins), 1)
        self.assertIn("TestPlugin", plugins)
        
        # Check the plugin properties
        plugin_info = plugin_manager.get_plugin_info("TestPlugin")
        self.assertEqual(plugin_info["name"], "TestPlugin")
        self.assertEqual(plugin_info["version"], "0.1.0")
        self.assertEqual(plugin_info["description"], "A test plugin for the Nüm Agents SDK")
        self.assertEqual(plugin_info["author"], "Test Author")
    
    def test_plugin_initialization(self):
        """Test initializing a plugin."""
        # Create a plugin manager
        plugin_manager = PluginManager(plugins_dir=self.plugins_dir)
        
        # Load plugins
        plugin_manager.load_plugins()
        
        # Create EventBus and Scheduler
        event_bus = EventBus()
        scheduler = Scheduler(event_bus=event_bus)
        
        # Initialize plugins
        plugin_manager.initialize_plugins(event_bus=event_bus, scheduler=scheduler)
        
        # Get the plugin instance
        plugin = plugin_manager.get_plugin_instance("TestPlugin")
        
        # Check that the plugin was initialized
        self.assertTrue(plugin.initialized)
        self.assertEqual(plugin.event_bus, event_bus)
        self.assertEqual(plugin.scheduler, scheduler)
    
    def test_plugin_hooks(self):
        """Test plugin hooks."""
        # Create a plugin manager
        plugin_manager = PluginManager(plugins_dir=self.plugins_dir)
        
        # Load plugins
        plugin_manager.load_plugins()
        
        # Create EventBus and Scheduler
        event_bus = EventBus()
        scheduler = Scheduler(event_bus=event_bus)
        
        # Initialize plugins
        plugin_manager.initialize_plugins(event_bus=event_bus, scheduler=scheduler)
        
        # Call the on_flow_start hook
        plugin_manager.call_hook("on_flow_start", "TestFlow", "flow-123")
        
        # Call the on_flow_end hook
        plugin_manager.call_hook("on_flow_end", "TestFlow", "flow-123", {"status": "success"})
        
        # Get the plugin instance
        plugin = plugin_manager.get_plugin_instance("TestPlugin")
        
        # Check that the hooks were called
        self.assertTrue(plugin.flow_started)
        self.assertTrue(plugin.flow_ended)
    
    def test_plugin_event_handling(self):
        """Test plugin event handling."""
        # Create a plugin manager
        plugin_manager = PluginManager(plugins_dir=self.plugins_dir)
        
        # Load plugins
        plugin_manager.load_plugins()
        
        # Create EventBus and Scheduler
        event_bus = EventBus()
        scheduler = Scheduler(event_bus=event_bus)
        
        # Initialize plugins
        plugin_manager.initialize_plugins(event_bus=event_bus, scheduler=scheduler)
        
        # Create a mock handler for the response event
        response_received = [False]
        
        def handle_response(event):
            self.assertEqual(event.event_type, "test.plugin.response")
            self.assertEqual(event.payload["message"], "Response from plugin")
            self.assertEqual(event.source, "TestPlugin")
            response_received[0] = True
        
        # Subscribe to the response event
        event_bus.subscribe("test.plugin.response", handle_response)
        
        # Publish a test event
        event = Event(
            event_type="test.plugin.event",
            payload={"message": "Test message"},
            source="Test"
        )
        event_bus.publish(event)
        
        # Get the plugin instance
        plugin = plugin_manager.get_plugin_instance("TestPlugin")
        
        # Check that the event was received and the response was sent
        self.assertTrue(plugin.event_received)
        self.assertTrue(response_received[0])
    
    def test_plugin_with_scheduler(self):
        """Test plugin interaction with the scheduler."""
        # Create a plugin manager
        plugin_manager = PluginManager(plugins_dir=self.plugins_dir)
        
        # Load plugins
        plugin_manager.load_plugins()
        
        # Create EventBus and Scheduler
        event_bus = EventBus()
        scheduler = Scheduler(event_bus=event_bus)
        
        # Initialize plugins
        plugin_manager.initialize_plugins(event_bus=event_bus, scheduler=scheduler)
        
        # Get the plugin instance
        plugin = plugin_manager.get_plugin_instance("TestPlugin")
        
        # Schedule a task through the plugin
        task_id = scheduler.schedule(
            name="PluginTask",
            callback=lambda: {"status": "task_executed"}
        )
        
        # Execute the task
        result = scheduler.execute_task(task_id)
        
        # Check the task result
        self.assertEqual(result, {"status": "task_executed"})


if __name__ == "__main__":
    unittest.main()
