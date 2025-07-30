"""
Core components for the Nüm Agents SDK.

This module defines the fundamental building blocks for agent flows:
- Node: Base class for all processing nodes
- Flow: Container and orchestrator for nodes
- SharedStore: Shared memory for data exchange between nodes
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import uuid


class SharedStore:
    """
    Shared memory store for data exchange between nodes in a flow.
    
    The SharedStore acts as a central repository for data that needs to be
    accessed and modified by different nodes during flow execution.
    
    It can also be initialized with working memory from an agent specification,
    providing access to goals, context, constraints, and preferences.
    """
    
    def __init__(self, agent_spec: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize a shared store, optionally with working memory from an agent specification.
        
        Args:
            agent_spec: Optional agent specification dictionary from AgentSpecLoader.load()
        """
        self._data: Dict[str, Any] = {}
        
        # Initialize working memory section if agent_spec is provided
        if agent_spec and "agent" in agent_spec and "working_memory" in agent_spec["agent"]:
            self._data["working_memory"] = agent_spec["agent"]["working_memory"]
            
            # For convenience, also store top-level working memory sections directly
            wm = agent_spec["agent"]["working_memory"]
            if "goals" in wm:
                self._data["goals"] = wm["goals"]
            if "context" in wm:
                self._data["context"] = wm["context"]
            if "constraints" in wm:
                self._data["constraints"] = wm["constraints"]
            if "preferences" in wm:
                self._data["preferences"] = wm["preferences"]
    
    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the shared store.
        
        Args:
            key: The key to store the value under
            value: The value to store
        """
        self._data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the shared store.
        
        Args:
            key: The key to retrieve
            default: Value to return if key doesn't exist
            
        Returns:
            The value associated with the key, or default if not found
        """
        return self._data.get(key, default)
    
    def has(self, key: str) -> bool:
        """
        Check if a key exists in the shared store.
        
        Args:
            key: The key to check
            
        Returns:
            True if the key exists, False otherwise
        """
        return key in self._data
    
    def delete(self, key: str) -> None:
        """
        Delete a key from the shared store.
        
        Args:
            key: The key to delete
        """
        if key in self._data:
            del self._data[key]
    
    def clear(self) -> None:
        """Clear all data from the shared store."""
        self._data.clear()
    
    def keys(self) -> Set[str]:
        """
        Get all keys in the shared store.
        
        Returns:
            A set of all keys in the store
        """
        return set(self._data.keys())
    
    def __contains__(self, key: str) -> bool:
        """Support for 'in' operator."""
        return key in self._data
    
    # Working Memory specific methods
    
    def get_working_memory(self) -> Dict[str, Any]:
        """
        Get the complete working memory.
        
        Returns:
            The working memory as a dictionary, or an empty dictionary if not available
        """
        return self.get("working_memory", {})
    
    def get_goals(self) -> List[str]:
        """
        Get the goals from working memory.
        
        Returns:
            The list of goals, or an empty list if not available
        """
        return self.get("goals", [])
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get the context from working memory.
        
        Context includes domain, project_type, user_expertise, etc.
        
        Returns:
            The context as a dictionary, or an empty dictionary if not available
        """
        return self.get("context", {})
    
    def get_constraints(self) -> List[str]:
        """
        Get the constraints from working memory.
        
        Returns:
            The list of constraints, or an empty list if not available
        """
        return self.get("constraints", [])
    
    def get_preferences(self) -> Dict[str, Any]:
        """
        Get the preferences from working memory.
        
        Returns:
            The preferences as a dictionary, or an empty dictionary if not available
        """
        return self.get("preferences", {})
    
    def update_working_memory(self, working_memory: Dict[str, Any]) -> None:
        """
        Update the working memory with new data.
        
        This will merge the new data with the existing working memory,
        replacing any existing values for the same keys.
        
        Args:
            working_memory: The new working memory data to merge
        """
        current_wm = self.get_working_memory()
        
        # Deep merge the working memory sections
        updated_wm = dict(current_wm)  # Create a copy to avoid modifying the original
        
        # Merge each section separately
        for section, values in working_memory.items():
            if section in current_wm and isinstance(current_wm[section], dict) and isinstance(values, dict):
                # For dictionary sections like context and preferences, merge them
                updated_wm[section] = {**current_wm[section], **values}
            else:
                # For list sections like goals and constraints, replace them
                updated_wm[section] = values
        
        self.set("working_memory", updated_wm)
        
        # Also update top-level sections for convenience
        if "goals" in working_memory:
            self.set("goals", working_memory["goals"])
        if "context" in working_memory:
            # Merge context dictionaries
            current_context = self.get_context()
            self.set("context", {**current_context, **working_memory["context"]})
        if "constraints" in working_memory:
            self.set("constraints", working_memory["constraints"])
        if "preferences" in working_memory:
            # Merge preferences dictionaries
            current_preferences = self.get_preferences()
            self.set("preferences", {**current_preferences, **working_memory["preferences"]})


class Node:
    """
    Base class for all processing nodes in a flow.
    
    A Node represents a single unit of processing in an agent flow.
    Each node can read from and write to the SharedStore, and can
    have transitions to other nodes.
    """
    
    def __init__(self, name: Optional[str] = None) -> None:
        """
        Initialize a new node.
        
        Args:
            name: Optional name for the node. If not provided, a UUID will be used.
        """
        self.id = str(uuid.uuid4())
        self.name = name or self.__class__.__name__
        self._next_nodes: List["Node"] = []
    
    def exec(self, shared: SharedStore) -> Dict[str, Any]:
        """
        Execute the node's processing logic.
        
        This method should be overridden by subclasses to implement
        the specific processing logic of the node.
        
        Args:
            shared: The shared store for accessing and storing data
            
        Returns:
            A dictionary containing the results of the node's execution
        """
        raise NotImplementedError("Node subclasses must implement exec method")
    
    def add_next(self, node: "Node") -> "Node":
        """
        Add a node to execute after this one.
        
        Args:
            node: The node to execute next
            
        Returns:
            The current node (self) for method chaining
        """
        self._next_nodes.append(node)
        return self
    
    def get_next_nodes(self) -> List["Node"]:
        """
        Get the list of nodes to execute after this one.
        
        Returns:
            List of next nodes
        """
        return self._next_nodes
    
    def __str__(self) -> str:
        """String representation of the node."""
        return f"{self.name}({self.id[:8]})"


class Flow:
    """
    Container and orchestrator for a sequence of nodes.
    
    A Flow represents a complete agent processing pipeline, consisting
    of multiple interconnected nodes that share data through a SharedStore.
    """
    
    def __init__(self, nodes: Optional[List[Node]] = None) -> None:
        """
        Initialize a new flow.
        
        Args:
            nodes: Optional list of nodes to add to the flow
        """
        self.nodes: List[Node] = nodes or []
        self.shared = SharedStore()
        self._start_node: Optional[Node] = None
        
        # If nodes were provided, automatically connect them in sequence
        if self.nodes:
            self._connect_nodes_in_sequence()
            self._start_node = self.nodes[0]
    
    def _connect_nodes_in_sequence(self) -> None:
        """Connect the nodes in the flow in sequence."""
        for i in range(len(self.nodes) - 1):
            self.nodes[i].add_next(self.nodes[i + 1])
    
    def add_node(self, node: Node) -> "Flow":
        """
        Add a node to the flow.
        
        Args:
            node: The node to add
            
        Returns:
            The flow instance for method chaining
        """
        self.nodes.append(node)
        if not self._start_node:
            self._start_node = node
        return self
    
    def add_transition(self, from_node: Node, to_node: Node) -> "Flow":
        """
        Add a transition between two nodes.
        
        Args:
            from_node: The source node
            to_node: The destination node
            
        Returns:
            The flow instance for method chaining
        """
        from_node.add_next(to_node)
        return self
    
    def set_start(self, node: Node) -> "Flow":
        """
        Set the starting node for the flow.
        
        Args:
            node: The node to start execution from
            
        Returns:
            The flow instance for method chaining
        """
        if node not in self.nodes:
            self.nodes.append(node)
        self._start_node = node
        return self
    
    def execute(self) -> Dict[str, Any]:
        """
        Execute the flow from the start node.
        
        Returns:
            The final results from the flow execution
        """
        if not self._start_node:
            raise ValueError("No start node defined for flow")
        
        results = {}
        current_nodes = [self._start_node]
        
        while current_nodes:
            next_nodes = []
            for node in current_nodes:
                node_results = node.exec(self.shared)
                results[node.name] = node_results
                next_nodes.extend(node.get_next_nodes())
            current_nodes = next_nodes
        
        return results
    
    def reset(self) -> None:
        """Reset the flow's shared store."""
        self.shared.clear()
    
    def get_nodes(self) -> List[Node]:
        """
        Get all nodes in the flow.
        
        Returns:
            List of all nodes
        """
        return self.nodes
