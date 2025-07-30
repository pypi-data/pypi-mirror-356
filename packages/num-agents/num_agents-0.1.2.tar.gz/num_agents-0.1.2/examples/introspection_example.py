#!/usr/bin/env python
"""
Example of using the introspection and adaptation capabilities of the Nüm Agents SDK.

This example demonstrates how to create an agent that can introspect itself
and adapt its behavior based on the results of the introspection.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Any, List

# Add the parent directory to the path so we can import the SDK
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from num_agents.core import Node, SharedStore
from num_agents.introspection import AgentIntrospector, AdaptiveFlow, AdaptiveNode


class ExampleSharedStore(SharedStore):
    """Example shared store for the introspection example."""
    
    def __init__(self) -> None:
        """Initialize the example shared store."""
        super().__init__()
        self.data = {}
        self.messages = []
        self.results = []
    
    def add_message(self, message: str) -> None:
        """Add a message to the shared store."""
        self.messages.append(message)
    
    def add_result(self, result: Dict[str, Any]) -> None:
        """Add a result to the shared store."""
        self.results.append(result)
    
    def get_messages(self) -> List[str]:
        """Get all messages from the shared store."""
        return self.messages
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get all results from the shared store."""
        return self.results


class InputNode(AdaptiveNode):
    """Example input node that can adapt its behavior."""
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        introspector: AgentIntrospector = None
    ) -> None:
        """Initialize the input node."""
        super().__init__(name, shared_store, introspector)
        self.input_validation = False
    
    def _process(self) -> None:
        """Process the node's logic."""
        # Simulate getting input
        user_input = "Example user input"
        
        # Apply input validation if adapted
        if self.input_validation:
            # Enhanced input validation
            self.shared_store.add_message(f"[{self.name}] Validating input: {user_input}")
            # Simulate validation
            self.shared_store.add_message(f"[{self.name}] Input validation passed")
        else:
            # Basic processing
            self.shared_store.add_message(f"[{self.name}] Received input: {user_input}")
        
        # Store the input
        self.shared_store.data["user_input"] = user_input
    
    def _handle_security_issue(self, recommendation: Dict[str, Any]) -> None:
        """Handle a security issue by enabling input validation."""
        self.input_validation = True
        
        # Log the adaptation
        adaptation = {
            "type": "security",
            "description": f"Enabled input validation for {self.name}",
            "recommendation": recommendation.get("description", "")
        }
        self.adaptation_history.append(adaptation)
        
        # Log the adaptation
        print(f"[AdaptiveNode] {adaptation['description']}")


class ProcessingNode(AdaptiveNode):
    """Example processing node that can adapt its behavior."""
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        introspector: AgentIntrospector = None
    ) -> None:
        """Initialize the processing node."""
        super().__init__(name, shared_store, introspector)
        self.use_caching = False
    
    def _process(self) -> None:
        """Process the node's logic."""
        # Get the input from the shared store
        user_input = self.shared_store.data.get("user_input", "")
        
        # Apply caching if adapted
        if self.use_caching:
            # Enhanced processing with caching
            self.shared_store.add_message(f"[{self.name}] Using cached processing for: {user_input}")
            # Simulate cached processing
            result = {"input": user_input, "output": f"Processed (cached): {user_input}"}
        else:
            # Basic processing
            self.shared_store.add_message(f"[{self.name}] Processing input: {user_input}")
            # Simulate processing
            result = {"input": user_input, "output": f"Processed: {user_input}"}
        
        # Store the result
        self.shared_store.data["processing_result"] = result
        self.shared_store.add_result(result)
    
    def _handle_performance_issue(self, recommendation: Dict[str, Any]) -> None:
        """Handle a performance issue by enabling caching."""
        self.use_caching = True
        
        # Log the adaptation
        adaptation = {
            "type": "performance",
            "description": f"Enabled caching for {self.name}",
            "recommendation": recommendation.get("description", "")
        }
        self.adaptation_history.append(adaptation)
        
        # Log the adaptation
        print(f"[AdaptiveNode] {adaptation['description']}")


class OutputNode(AdaptiveNode):
    """Example output node that can adapt its behavior."""
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        introspector: AgentIntrospector = None
    ) -> None:
        """Initialize the output node."""
        super().__init__(name, shared_store, introspector)
        self.format_output = False
    
    def _process(self) -> None:
        """Process the node's logic."""
        # Get the processing result from the shared store
        result = self.shared_store.data.get("processing_result", {})
        
        # Apply formatting if adapted
        if self.format_output:
            # Enhanced output with formatting
            self.shared_store.add_message(f"[{self.name}] Formatting output")
            # Simulate formatting
            output = json.dumps(result, indent=2)
        else:
            # Basic output
            output = str(result)
        
        # Output the result
        self.shared_store.add_message(f"[{self.name}] Output: {output}")
    
    def _handle_missing_module(self, recommendation: Dict[str, Any]) -> None:
        """Handle a missing module issue by enabling output formatting."""
        self.format_output = True
        
        # Log the adaptation
        adaptation = {
            "type": "missing_module",
            "description": f"Enabled output formatting for {self.name}",
            "recommendation": recommendation.get("description", "")
        }
        self.adaptation_history.append(adaptation)
        
        # Log the adaptation
        print(f"[AdaptiveNode] {adaptation['description']}")


def create_example_agent(agent_dir: str) -> None:
    """
    Create an example agent with introspection and adaptation capabilities.
    
    Args:
        agent_dir: The directory where the agent files will be created
    """
    # Create the agent directory if it doesn't exist
    os.makedirs(agent_dir, exist_ok=True)
    
    # Create a minimal agent.yaml file
    agent_yaml = """
name: IntrospectionExampleAgent
description: An example agent that demonstrates introspection and adaptation capabilities
universes:
  - core
  - llm
modules:
  - InputNode
  - ProcessingNode
  # OutputNode is intentionally missing to demonstrate adaptation
protocol: simple
llm:
  provider: openai
  model: gpt-4
memory:
  type: simple
"""
    
    # Write the agent.yaml file
    with open(os.path.join(agent_dir, "agent.yaml"), "w") as f:
        f.write(agent_yaml)
    
    # Create a minimal logical_graph.mmd file
    logical_graph = """
flowchart TD
    InputNode --> ProcessingNode
    ProcessingNode --> End
"""
    
    # Write the logical_graph.mmd file
    with open(os.path.join(agent_dir, "logical_graph.mmd"), "w") as f:
        f.write(logical_graph)
    
    # Create a minimal audit_report.json file
    audit_report = {
        "validation": {
            "agent_name": "IntrospectionExampleAgent",
            "status": "warning",
            "health_score": 65,
            "completeness": 0.67,
            "issues": [
                {
                    "type": "missing_module",
                    "severity": "critical",
                    "description": "Missing module: OutputNode is declared in the universe catalog but not used in the agent"
                }
            ],
            "suggestions": {
                "critical": [
                    {
                        "text": "Add OutputNode to the agent to handle output formatting"
                    }
                ],
                "high": [
                    {
                        "text": "Add input validation to InputNode to improve security"
                    }
                ],
                "medium": [
                    {
                        "text": "Consider using caching in ProcessingNode to improve performance"
                    }
                ],
                "low": []
            },
            "nodes": {
                "InputNode": {
                    "status": "warning",
                    "issues": [
                        {
                            "type": "security",
                            "severity": "high",
                            "description": "InputNode does not validate user input"
                        }
                    ],
                    "suggestions": [
                        {
                            "text": "Add input validation to InputNode"
                        }
                    ]
                },
                "ProcessingNode": {
                    "status": "warning",
                    "issues": [
                        {
                            "type": "performance",
                            "severity": "medium",
                            "description": "ProcessingNode does not use caching"
                        }
                    ],
                    "suggestions": [
                        {
                            "text": "Consider using caching in ProcessingNode"
                        }
                    ]
                }
            }
        }
    }
    
    # Write the audit_report.json file
    with open(os.path.join(agent_dir, "audit_report.json"), "w") as f:
        json.dump(audit_report, f, indent=2)


def run_example() -> None:
    """Run the introspection and adaptation example."""
    # Create a temporary directory for the example agent
    agent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "example_agent")
    
    # Create the example agent
    create_example_agent(agent_dir)
    
    print(f"Created example agent in {agent_dir}")
    
    # Create an introspector for the agent
    introspector = AgentIntrospector(agent_dir)
    
    # Create a shared store
    shared_store = ExampleSharedStore()
    
    # Create nodes
    input_node = InputNode("InputNode", shared_store, introspector)
    processing_node = ProcessingNode("ProcessingNode", shared_store, introspector)
    output_node = OutputNode("OutputNode", shared_store, introspector)
    
    # Create an adaptive flow
    flow = AdaptiveFlow(
        name="ExampleFlow",
        shared_store=shared_store,
        nodes=[input_node, processing_node],  # Intentionally missing output_node
        agent_dir=agent_dir,
        introspector=introspector
    )
    
    print("\n=== Running flow without adaptation ===")
    
    # Disable auto-adaptation for the first run
    flow.auto_adapt = False
    for node in flow.nodes:
        if isinstance(node, AdaptiveNode):
            node.auto_adapt = False
    
    # Run the flow without adaptation
    flow.run()
    
    # Print the messages
    for message in shared_store.get_messages():
        print(message)
    
    # Clear the messages
    shared_store.messages = []
    
    print("\n=== Running flow with adaptation ===")
    
    # Enable auto-adaptation for the second run
    flow.auto_adapt = True
    for node in flow.nodes:
        if isinstance(node, AdaptiveNode):
            node.auto_adapt = True
    
    # Force adaptation
    flow.force_adapt()
    
    # Run the flow with adaptation
    flow.run()
    
    # Print the messages
    for message in shared_store.get_messages():
        print(message)
    
    # Print the adaptation history
    print("\n=== Adaptation History ===")
    for adaptation in flow.get_adaptation_history():
        print(f"Type: {adaptation.get('type')}, Description: {adaptation.get('description')}")
    
    for node in flow.nodes:
        if isinstance(node, AdaptiveNode) and node.adaptation_history:
            print(f"\nNode: {node.name}")
            for adaptation in node.get_adaptation_history():
                print(f"Type: {adaptation.get('type')}, Description: {adaptation.get('description')}")


if __name__ == "__main__":
    run_example()
