"""
Integration test for the exportAll CLI command with event-driven agent configurations.
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from num_agents.cli import app
from typer.testing import CliRunner


class TestExportAllWithEvents(unittest.TestCase):
    """Integration test for the exportAll CLI command with event-driven agent configurations."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary directory for the test
        self.test_dir = tempfile.mkdtemp()
        
        # Create a temporary agent.yaml file
        self.agent_yaml_path = os.path.join(self.test_dir, "agent.yaml")
        with open(self.agent_yaml_path, "w") as f:
            f.write("""
name: EventDrivenTestAgent
description: A test agent that uses the EventBus and Scheduler
version: 0.1.0
universes:
  - core
  - eventbus
  - scheduler
protocol:
  llm:
    provider: openai
    model: gpt-4
    temperature: 0.7
  memory:
    type: simple
nodes:
  - name: EventPublisherNode
    type: EventBusNode
    config:
      events_to_publish:
        - event_type: test.event
          payload:
            message: "Hello from the test agent!"
  - name: EventSubscriberNode
    type: EventBusNode
    config:
      events_to_subscribe:
        - event_type: test.event
          handler: handle_test_event
  - name: SchedulerNode
    type: ScheduleTaskNode
    config:
      task_name: TestTask
      callback: test_callback
      interval: 60
      max_runs: 3
            """)
        
        # Create a temporary univers_catalog.yaml file
        self.univers_catalog_path = os.path.join(self.test_dir, "univers_catalog.yaml")
        with open(self.univers_catalog_path, "w") as f:
            f.write("""
universes:
  core:
    description: Core modules for the Nüm Agents SDK
    modules:
      - name: flow
        description: Flow module for orchestrating nodes
      - name: node
        description: Base node module for processing data
      - name: shared_store
        description: Shared store module for data sharing between nodes
  eventbus:
    description: EventBus modules for event-driven communication
    modules:
      - name: event
        description: Event module for defining events
      - name: eventbus
        description: EventBus module for publishing and subscribing to events
      - name: event_bus_node
        description: EventBusNode for integrating with flows
  scheduler:
    description: Scheduler modules for task scheduling
    modules:
      - name: task
        description: Task module for defining scheduled tasks
      - name: scheduler
        description: Scheduler module for managing tasks
      - name: scheduler_node
        description: SchedulerNode for integrating with flows
            """)
        
        # Create a runner for the CLI
        self.runner = CliRunner()
    
    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)
    
    def test_export_all_with_events(self):
        """Test the exportAll CLI command with an event-driven agent configuration."""
        # Define the output directory
        output_dir = os.path.join(self.test_dir, "output")
        
        # Run the exportAll command
        result = self.runner.invoke(
            app,
            [
                "exportAll",
                "--agent-yaml", self.agent_yaml_path,
                "--univers-catalog", self.univers_catalog_path,
                "--output-dir", output_dir
            ]
        )
        
        # Check that the command succeeded
        self.assertEqual(result.exit_code, 0, f"Command failed with output: {result.output}")
        
        # Check that the output directory was created
        self.assertTrue(os.path.exists(output_dir))
        
        # Check that the agent directory was created
        agent_dir = os.path.join(output_dir, "EventDrivenTestAgent")
        self.assertTrue(os.path.exists(agent_dir))
        
        # Check that the main files were created
        self.assertTrue(os.path.exists(os.path.join(agent_dir, "main.py")))
        self.assertTrue(os.path.exists(os.path.join(agent_dir, "flow.py")))
        self.assertTrue(os.path.exists(os.path.join(agent_dir, "shared_store.py")))
        
        # Check that the nodes directory was created
        nodes_dir = os.path.join(agent_dir, "nodes")
        self.assertTrue(os.path.exists(nodes_dir))
        
        # Check that the node files were created
        self.assertTrue(os.path.exists(os.path.join(nodes_dir, "event_publisher_node.py")))
        self.assertTrue(os.path.exists(os.path.join(nodes_dir, "event_subscriber_node.py")))
        self.assertTrue(os.path.exists(os.path.join(nodes_dir, "scheduler_node.py")))
        
        # Check that the logical graph was created
        self.assertTrue(os.path.exists(os.path.join(agent_dir, "logical_graph.mmd")))
        
        # Check that the audit report was created
        self.assertTrue(os.path.exists(os.path.join(agent_dir, "audit_report.json")))
        
        # Check the content of the flow.py file to ensure it includes EventBus and Scheduler
        with open(os.path.join(agent_dir, "flow.py"), "r") as f:
            flow_content = f.read()
            self.assertIn("EventBus", flow_content)
            self.assertIn("Scheduler", flow_content)
        
        # Check the content of the shared_store.py file
        with open(os.path.join(agent_dir, "shared_store.py"), "r") as f:
            shared_store_content = f.read()
            self.assertIn("SharedStore", shared_store_content)
        
        # Check the content of the event_publisher_node.py file
        with open(os.path.join(nodes_dir, "event_publisher_node.py"), "r") as f:
            node_content = f.read()
            self.assertIn("EventBusNode", node_content)
            self.assertIn("test.event", node_content)
        
        # Check the content of the scheduler_node.py file
        with open(os.path.join(nodes_dir, "scheduler_node.py"), "r") as f:
            node_content = f.read()
            self.assertIn("ScheduleTaskNode", node_content)
            self.assertIn("TestTask", node_content)


if __name__ == "__main__":
    unittest.main()
