"""
Conditional Flow for the Nüm Agents SDK.

This module provides classes for implementing conditional transitions between nodes,
allowing for more complex flow control in agent workflows.
"""

from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from num_agents.core import Flow, Node, SharedStore


class TransitionType(Enum):
    """Enum for different types of transitions between nodes."""
    
    SEQUENTIAL = "sequential"  # Default transition, always proceeds to the next node
    CONDITIONAL = "conditional"  # Proceeds based on a condition
    BRANCH = "branch"  # Branches to one of multiple possible next nodes
    LOOP = "loop"  # Loops back to a previous node if a condition is met
    END = "end"  # Ends the flow


class Transition:
    """
    Represents a transition between nodes in a flow.
    
    A transition defines how the flow proceeds from one node to the next,
    which can be conditional based on the state of the shared store.
    """
    
    def __init__(
        self,
        transition_type: TransitionType,
        condition: Optional[Callable[[SharedStore], bool]] = None,
        target_node: Optional[str] = None,
        branch_conditions: Optional[Dict[str, Callable[[SharedStore], bool]]] = None
    ) -> None:
        """
        Initialize a transition.
        
        Args:
            transition_type: The type of transition
            condition: Optional condition function that takes a SharedStore and returns a boolean.
                      Used for CONDITIONAL and LOOP transitions.
            target_node: Optional name of the target node.
                        Used for LOOP transitions to specify the node to loop back to.
            branch_conditions: Optional dictionary mapping node names to condition functions.
                             Used for BRANCH transitions to determine which branch to take.
        """
        self.transition_type = transition_type
        self.condition = condition
        self.target_node = target_node
        self.branch_conditions = branch_conditions or {}
    
    def get_next_node(self, current_node_index: int, nodes: List[Node], shared_store: SharedStore) -> Optional[int]:
        """
        Get the index of the next node to execute.
        
        Args:
            current_node_index: The index of the current node
            nodes: The list of nodes in the flow
            shared_store: The shared store for the flow
            
        Returns:
            The index of the next node to execute, or None if the flow should end
        """
        if self.transition_type == TransitionType.SEQUENTIAL:
            # Proceed to the next node in sequence
            next_index = current_node_index + 1
            return next_index if next_index < len(nodes) else None
        
        elif self.transition_type == TransitionType.CONDITIONAL:
            # Proceed to the next node only if the condition is met
            if self.condition and self.condition(shared_store):
                next_index = current_node_index + 1
                return next_index if next_index < len(nodes) else None
            return None
        
        elif self.transition_type == TransitionType.BRANCH:
            # Branch to one of multiple possible next nodes
            if not self.branch_conditions:
                return None
            
            for node_name, condition in self.branch_conditions.items():
                if condition(shared_store):
                    # Find the index of the node with the given name
                    for i, node in enumerate(nodes):
                        if node.name == node_name:
                            return i
            
            # If no branch condition is met, return None
            return None
        
        elif self.transition_type == TransitionType.LOOP:
            # Loop back to a previous node if the condition is met
            if self.condition and self.condition(shared_store) and self.target_node:
                # Find the index of the target node
                for i, node in enumerate(nodes):
                    if node.name == self.target_node:
                        return i
            
            # If the condition is not met or the target node is not found,
            # proceed to the next node in sequence
            next_index = current_node_index + 1
            return next_index if next_index < len(nodes) else None
        
        elif self.transition_type == TransitionType.END:
            # End the flow
            return None
        
        # Default: proceed to the next node in sequence
        next_index = current_node_index + 1
        return next_index if next_index < len(nodes) else None


class ConditionalNode(Node):
    """
    A node with conditional transitions.
    
    This class extends the base Node class to add support for conditional
    transitions, allowing the flow to branch, loop, or end based on conditions.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        transition: Optional[Transition] = None
    ) -> None:
        """
        Initialize a conditional node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            transition: Optional transition for this node.
                       If not provided, a default sequential transition will be used.
        """
        super().__init__(name, shared_store)
        self.transition = transition or Transition(TransitionType.SEQUENTIAL)
    
    def get_next_node_index(self, current_index: int, nodes: List[Node]) -> Optional[int]:
        """
        Get the index of the next node to execute.
        
        Args:
            current_index: The index of this node in the flow
            nodes: The list of nodes in the flow
            
        Returns:
            The index of the next node to execute, or None if the flow should end
        """
        return self.transition.get_next_node(current_index, nodes, self.shared_store)


class ConditionalFlow(Flow):
    """
    A flow with conditional transitions between nodes.
    
    This class extends the base Flow class to add support for conditional
    transitions, allowing for more complex flow control.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        nodes: List[Node]
    ) -> None:
        """
        Initialize a conditional flow.
        
        Args:
            name: The name of the flow
            shared_store: The shared store for the agent
            nodes: The list of nodes in the flow
        """
        super().__init__(name, shared_store, nodes)
    
    def run(self) -> None:
        """
        Run the flow with conditional transitions.
        
        This method executes the nodes in the flow, respecting the
        conditional transitions between them.
        """
        if not self.nodes:
            return
        
        # Start with the first node
        current_index = 0
        
        # Execute nodes until we reach the end of the flow
        while current_index is not None and current_index < len(self.nodes):
            # Get the current node
            current_node = self.nodes[current_index]
            
            # Process the current node
            current_node.process()
            
            # Determine the next node to execute
            if isinstance(current_node, ConditionalNode):
                # Use the node's transition to determine the next node
                current_index = current_node.get_next_node_index(current_index, self.nodes)
            else:
                # For regular nodes, proceed to the next node in sequence
                current_index += 1
                if current_index >= len(self.nodes):
                    current_index = None


# Example condition functions
def always_true(shared_store: SharedStore) -> bool:
    """A condition that always returns True."""
    return True


def always_false(shared_store: SharedStore) -> bool:
    """A condition that always returns False."""
    return False


def check_key_exists(key: str) -> Callable[[SharedStore], bool]:
    """
    Create a condition function that checks if a key exists in the shared store.
    
    Args:
        key: The key to check
        
    Returns:
        A condition function that takes a SharedStore and returns a boolean
    """
    def condition(shared_store: SharedStore) -> bool:
        return hasattr(shared_store, key) or (
            hasattr(shared_store, "data") and 
            isinstance(shared_store.data, dict) and 
            key in shared_store.data
        )
    
    return condition


def check_key_equals(key: str, value: Any) -> Callable[[SharedStore], bool]:
    """
    Create a condition function that checks if a key in the shared store equals a value.
    
    Args:
        key: The key to check
        value: The value to compare with
        
    Returns:
        A condition function that takes a SharedStore and returns a boolean
    """
    def condition(shared_store: SharedStore) -> bool:
        if hasattr(shared_store, key):
            return getattr(shared_store, key) == value
        elif hasattr(shared_store, "data") and isinstance(shared_store.data, dict) and key in shared_store.data:
            return shared_store.data[key] == value
        return False
    
    return condition
