"""
Tests for the AdaptiveFlow and AdaptiveNode classes.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock, call

from num_agents.core import SharedStore
from num_agents.introspection.agent_introspector import AgentIntrospector
from num_agents.introspection.adaptive_flow import AdaptiveNode, AdaptiveFlow


class TestSharedStore(SharedStore):
    """Test shared store for adaptive flow tests."""
    
    def __init__(self):
        """Initialize the test shared store."""
        super().__init__()
        self.data = {}
        self.processed = []
    
    def add_processed(self, name):
        """Add a processed node name."""
        self.processed.append(name)


class TestNode(AdaptiveNode):
    """Test node for adaptive flow tests."""
    
    def __init__(
        self,
        name,
        shared_store,
        introspector=None,
        adaptation_handlers=None,
        adaptation_threshold=70.0,
        auto_adapt=True
    ):
        """Initialize the test node."""
        super().__init__(
            name,
            shared_store,
            introspector,
            adaptation_handlers,
            adaptation_threshold,
            auto_adapt
        )
        self.processed = False
    
    def _process(self):
        """Process the node's logic."""
        self.processed = True
        self.shared_store.add_processed(self.name)


@pytest.fixture
def mock_introspector():
    """Create a mock introspector."""
    mock = MagicMock(spec=AgentIntrospector)
    
    # Mock the should_adapt method
    mock.should_adapt.return_value = True
    
    # Mock the get_adaptation_recommendations method
    mock.get_adaptation_recommendations.return_value = [
        {
            "type": "issue",
            "severity": "critical",
            "description": "Missing module: OutputNode"
        },
        {
            "type": "suggestion",
            "severity": "high",
            "description": "Add input validation to improve security"
        },
        {
            "type": "suggestion",
            "severity": "medium",
            "description": "Consider using caching to improve performance"
        }
    ]
    
    return mock


@pytest.fixture
def shared_store():
    """Create a test shared store."""
    return TestSharedStore()


def test_adaptive_node_init():
    """Test initialization of AdaptiveNode."""
    shared_store = TestSharedStore()
    node = AdaptiveNode("TestNode", shared_store)
    
    assert node.name == "TestNode"
    assert node.shared_store == shared_store
    assert node.introspector is None
    assert node.adaptation_threshold == 70.0
    assert node.auto_adapt is True
    assert node.has_adapted is False
    assert len(node.adaptation_history) == 0
    assert len(node.adaptation_handlers) > 0  # Default handlers should be registered


def test_adaptive_node_register_default_handlers():
    """Test registering default handlers in AdaptiveNode."""
    shared_store = TestSharedStore()
    node = AdaptiveNode("TestNode", shared_store)
    
    # Check that default handlers are registered
    assert "security" in node.adaptation_handlers
    assert "performance" in node.adaptation_handlers
    assert "missing module" in node.adaptation_handlers


def test_adaptive_node_process_without_adaptation():
    """Test processing without adaptation in AdaptiveNode."""
    shared_store = TestSharedStore()
    node = TestNode("TestNode", shared_store, auto_adapt=False)
    
    # Process the node
    node.process()
    
    # Check that the node was processed
    assert node.processed is True
    assert shared_store.processed == ["TestNode"]
    assert node.has_adapted is False
    assert len(node.adaptation_history) == 0


def test_adaptive_node_process_with_adaptation(mock_introspector):
    """Test processing with adaptation in AdaptiveNode."""
    shared_store = TestSharedStore()
    node = TestNode("TestNode", shared_store, mock_introspector)
    
    # Add a test adaptation handler
    test_handler = MagicMock()
    node.adaptation_handlers["security"] = test_handler
    
    # Process the node
    node.process()
    
    # Check that the node was processed
    assert node.processed is True
    assert shared_store.processed == ["TestNode"]
    
    # Check that adaptation was attempted
    mock_introspector.should_adapt.assert_called_once_with(70.0)
    mock_introspector.get_adaptation_recommendations.assert_called_once()


def test_adaptive_node_force_adapt(mock_introspector):
    """Test forcing adaptation in AdaptiveNode."""
    shared_store = TestSharedStore()
    node = TestNode("TestNode", shared_store, mock_introspector, auto_adapt=False)
    
    # Add a test adaptation handler
    test_handler = MagicMock()
    node.adaptation_handlers["security"] = test_handler
    
    # Force adaptation
    result = node.force_adapt()
    
    # Check that adaptation was forced
    assert result is True
    mock_introspector.get_adaptation_recommendations.assert_called_once_with(refresh=True)


def test_adaptive_node_register_adaptation_handler():
    """Test registering an adaptation handler in AdaptiveNode."""
    shared_store = TestSharedStore()
    node = AdaptiveNode("TestNode", shared_store)
    
    # Register a new handler
    test_handler = MagicMock()
    node.register_adaptation_handler("test", test_handler)
    
    # Check that the handler was registered
    assert "test" in node.adaptation_handlers
    assert node.adaptation_handlers["test"] == test_handler


def test_adaptive_flow_init():
    """Test initialization of AdaptiveFlow."""
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent")
    
    assert flow.name == "TestFlow"
    assert flow.shared_store == shared_store
    assert flow.nodes == [node1, node2]
    assert flow.agent_dir == "/path/to/agent"
    assert flow.introspector is not None
    assert flow.adaptation_threshold == 70.0
    assert flow.auto_adapt is True
    assert flow.has_adapted is False
    assert len(flow.adaptation_history) == 0
    assert len(flow.adaptation_handlers) > 0  # Default handlers should be registered


def test_adaptive_flow_register_default_handlers():
    """Test registering default handlers in AdaptiveFlow."""
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent")
    
    # Check that default handlers are registered
    assert "add_node" in flow.adaptation_handlers
    assert "add_validation" in flow.adaptation_handlers
    assert "optimize" in flow.adaptation_handlers
    assert "reorder" in flow.adaptation_handlers


def test_adaptive_flow_run_without_adaptation():
    """Test running without adaptation in AdaptiveFlow."""
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    # Create a flow with auto_adapt=False
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent", auto_adapt=False)
    
    # Run the flow
    flow.run()
    
    # Check that the nodes were processed
    assert shared_store.processed == ["Node1", "Node2"]
    assert node1.processed is True
    assert node2.processed is True
    assert flow.has_adapted is False
    assert len(flow.adaptation_history) == 0


@patch("num_agents.introspection.agent_introspector.AgentIntrospector")
def test_adaptive_flow_run_with_adaptation(mock_introspector_class):
    """Test running with adaptation in AdaptiveFlow."""
    # Create a mock introspector
    mock_introspector = MagicMock()
    mock_introspector.should_adapt.return_value = True
    mock_introspector.get_adaptation_recommendations.return_value = [
        {
            "type": "issue",
            "severity": "critical",
            "description": "Missing module: OutputNode"
        }
    ]
    mock_introspector_class.return_value = mock_introspector
    
    # Create a shared store and nodes
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    # Create a flow
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent")
    
    # Add a test adaptation handler
    test_handler = MagicMock()
    flow.adaptation_handlers["add_node"] = test_handler
    
    # Run the flow
    flow.run()
    
    # Check that the nodes were processed
    assert shared_store.processed == ["Node1", "Node2"]
    assert node1.processed is True
    assert node2.processed is True
    
    # Check that adaptation was attempted
    mock_introspector.should_adapt.assert_called_with(70.0)
    mock_introspector.get_adaptation_recommendations.assert_called_once()


def test_adaptive_flow_force_adapt(mock_introspector):
    """Test forcing adaptation in AdaptiveFlow."""
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    # Create a flow with auto_adapt=False
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent", mock_introspector, auto_adapt=False)
    
    # Add a test adaptation handler
    test_handler = MagicMock()
    flow.adaptation_handlers["add_node"] = test_handler
    
    # Force adaptation
    result = flow.force_adapt()
    
    # Check that adaptation was forced
    assert result is True
    mock_introspector.get_adaptation_recommendations.assert_called_once_with(refresh=True)


def test_adaptive_flow_create_adaptation():
    """Test creating adaptations in AdaptiveFlow."""
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent")
    
    # Test creating an adaptation for a missing module
    adaptation = flow._create_adaptation({
        "type": "issue",
        "severity": "critical",
        "description": "Missing module: OutputNode"
    })
    
    assert adaptation["type"] == "add_node"
    assert adaptation["node_type"] == "OutputNode"
    assert adaptation["position"] == "end"
    assert "OutputNode" in adaptation["description"]
    
    # Test creating an adaptation for a security issue
    adaptation = flow._create_adaptation({
        "type": "suggestion",
        "severity": "high",
        "description": "Add input validation to improve security"
    })
    
    assert adaptation["type"] == "add_validation"
    assert "security" in adaptation["description"]
    
    # Test creating an adaptation for a performance issue
    adaptation = flow._create_adaptation({
        "type": "suggestion",
        "severity": "medium",
        "description": "Consider using caching to improve performance"
    })
    
    assert adaptation["type"] == "optimize"
    assert "performance" in adaptation["description"]
    
    # Test creating an adaptation for a node ordering issue
    adaptation = flow._create_adaptation({
        "type": "suggestion",
        "severity": "medium",
        "description": "Consider reordering nodes for better sequence"
    })
    
    assert adaptation["type"] == "reorder"
    assert "sequence" in adaptation["description"]
    
    # Test creating a generic adaptation
    adaptation = flow._create_adaptation({
        "type": "suggestion",
        "severity": "low",
        "description": "Some other suggestion"
    })
    
    assert adaptation["type"] == "generic"
    assert "Some other suggestion" in adaptation["description"]


def test_adaptive_flow_apply_adaptation():
    """Test applying adaptations in AdaptiveFlow."""
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent")
    
    # Replace the default handlers with mocks
    flow.adaptation_handlers = {
        "add_node": MagicMock(),
        "add_validation": MagicMock(),
        "optimize": MagicMock(),
        "reorder": MagicMock()
    }
    
    # Apply an adaptation with a registered handler
    adaptation = {
        "type": "add_node",
        "node_type": "OutputNode",
        "position": "end",
        "description": "Added OutputNode"
    }
    flow._apply_adaptation(adaptation)
    
    # Check that the handler was called
    flow.adaptation_handlers["add_node"].assert_called_once_with(adaptation)
    
    # Apply an adaptation without a registered handler
    adaptation = {
        "type": "unknown",
        "description": "Unknown adaptation"
    }
    flow._apply_adaptation(adaptation)
    
    # No handler should be called for unknown adaptation types


def test_adaptive_flow_node_management():
    """Test node management methods in AdaptiveFlow."""
    shared_store = TestSharedStore()
    node1 = TestNode("Node1", shared_store)
    node2 = TestNode("Node2", shared_store)
    
    flow = AdaptiveFlow("TestFlow", shared_store, [node1, node2], "/path/to/agent")
    
    # Test get_node_by_name
    assert flow.get_node_by_name("Node1") == node1
    assert flow.get_node_by_name("Node2") == node2
    assert flow.get_node_by_name("NonExistentNode") is None
    
    # Test add_node
    node3 = TestNode("Node3", shared_store)
    flow.add_node(node3)
    assert flow.nodes == [node1, node2, node3]
    
    node4 = TestNode("Node4", shared_store)
    flow.add_node(node4, position=1)
    assert flow.nodes == [node1, node4, node2, node3]
    
    # Test remove_node
    assert flow.remove_node("Node4") is True
    assert flow.nodes == [node1, node2, node3]
    assert flow.remove_node("NonExistentNode") is False
    
    # Test reorder_nodes
    assert flow.reorder_nodes(["Node3", "Node1", "Node2"]) is True
    assert [node.name for node in flow.nodes] == ["Node3", "Node1", "Node2"]
    
    # Test reorder_nodes with invalid node names
    assert flow.reorder_nodes(["Node3", "Node1", "NonExistentNode"]) is False
    
    # Test reorder_nodes with incomplete node list
    assert flow.reorder_nodes(["Node3", "Node1"]) is False
