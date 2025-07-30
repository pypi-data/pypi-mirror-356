"""
Adaptive Flow for the Nüm Agents SDK.

This module provides the AdaptiveFlow class, which enables agents to
dynamically adapt their flow based on self-introspection results.
"""

import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

from num_agents.core import Flow, Node, SharedStore
from num_agents.introspection.agent_introspector import AgentIntrospector


class AdaptiveNode(Node):
    """
    A node that can adapt its behavior based on introspection results.
    
    This class extends the base Node class to add adaptive capabilities,
    allowing the node to modify its behavior based on the agent's
    health status and recommendations.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        introspector: Optional[AgentIntrospector] = None,
        adaptation_handlers: Optional[Dict[str, Callable]] = None,
        adaptation_threshold: float = 70.0,
        auto_adapt: bool = True
    ) -> None:
        """
        Initialize the adaptive node.
        
        Args:
            name: The name of the node
            shared_store: The shared store for the agent
            introspector: Optional AgentIntrospector instance.
                         If not provided, the node will not be able to adapt.
            adaptation_handlers: Optional dictionary mapping issue/suggestion types
                                to handler functions that implement adaptation logic.
            adaptation_threshold: The health score threshold below which adaptation is recommended.
            auto_adapt: Whether to automatically adapt when needed.
        """
        super().__init__(name, shared_store)
        self.introspector = introspector
        self.adaptation_handlers = adaptation_handlers or {}
        self.adaptation_threshold = adaptation_threshold
        self.auto_adapt = auto_adapt
        self.has_adapted = False
        self.adaptation_history = []
        
        # Register default adaptation handlers if none are provided
        if not self.adaptation_handlers:
            self._register_default_handlers()
    
    def _register_default_handlers(self) -> None:
        """
        Register default adaptation handlers.
        
        This method registers default handlers for common types of recommendations.
        Subclasses can override this method to register their own default handlers.
        """
        # Default handler for security issues
        self.adaptation_handlers["security"] = self._handle_security_issue
        
        # Default handler for performance issues
        self.adaptation_handlers["performance"] = self._handle_performance_issue
        
        # Default handler for missing modules
        self.adaptation_handlers["missing module"] = self._handle_missing_module
    
    def _handle_security_issue(self, recommendation: Dict[str, Any]) -> None:
        """
        Handle a security issue.
        
        Args:
            recommendation: The recommendation to handle
        """
        # Log the adaptation
        adaptation = {
            "type": "security",
            "description": f"Added security validation for {self.name}",
            "recommendation": recommendation.get("description", "")
        }
        self.adaptation_history.append(adaptation)
        
        # In a real implementation, this would add security validation logic
        # For now, we just log the adaptation
        print(f"[AdaptiveNode] {adaptation['description']}")
    
    def _handle_performance_issue(self, recommendation: Dict[str, Any]) -> None:
        """
        Handle a performance issue.
        
        Args:
            recommendation: The recommendation to handle
        """
        # Log the adaptation
        adaptation = {
            "type": "performance",
            "description": f"Optimized performance for {self.name}",
            "recommendation": recommendation.get("description", "")
        }
        self.adaptation_history.append(adaptation)
        
        # In a real implementation, this would optimize the node's performance
        # For now, we just log the adaptation
        print(f"[AdaptiveNode] {adaptation['description']}")
    
    def _handle_missing_module(self, recommendation: Dict[str, Any]) -> None:
        """
        Handle a missing module issue.
        
        Args:
            recommendation: The recommendation to handle
        """
        # Extract the missing module name
        description = recommendation.get("description", "")
        module_name = description.split("missing module: ")[-1].split(" ")[0] if "missing module: " in description else "unknown"
        
        # Log the adaptation
        adaptation = {
            "type": "missing_module",
            "description": f"Added dependency on {module_name} for {self.name}",
            "recommendation": description,
            "module": module_name
        }
        self.adaptation_history.append(adaptation)
        
        # In a real implementation, this would add the missing module
        # For now, we just log the adaptation
        print(f"[AdaptiveNode] {adaptation['description']}")
    
    def process(self) -> None:
        """
        Process the node's logic, with potential adaptation.
        
        This method first checks if adaptation is needed, and if so,
        applies the appropriate adaptations before executing the
        node's normal processing logic.
        """
        # Check if adaptation is needed
        if self.introspector and self.auto_adapt and not self.has_adapted:
            self._adapt()
        
        # Execute the node's normal processing logic
        self._process()
    
    def _process(self) -> None:
        """
        Execute the node's normal processing logic.
        
        This method should be overridden by subclasses to implement
        the node's specific processing logic.
        """
        # This is a placeholder that should be overridden by subclasses
        pass
    
    def _adapt(self) -> bool:
        """
        Adapt the node's behavior based on introspection results.
        
        This method checks the agent's health status and recommendations,
        and applies the appropriate adaptations if needed.
        
        Returns:
            True if adaptations were applied, False otherwise
        """
        if not self.introspector:
            return False
        
        # Check if adaptation is recommended
        if self.introspector.should_adapt(self.adaptation_threshold):
            # Get adaptation recommendations
            recommendations = self.introspector.get_adaptation_recommendations()
            
            # Track whether any adaptations were applied
            adaptations_applied = False
            
            # Apply adaptations based on recommendations
            for recommendation in recommendations:
                recommendation_type = recommendation.get("type")
                description = recommendation.get("description", "")
                
                # Look for a handler for this type of recommendation
                for pattern, handler in self.adaptation_handlers.items():
                    if pattern in description:
                        # Apply the adaptation
                        handler(recommendation)
                        adaptations_applied = True
                        break
            
            self.has_adapted = adaptations_applied
            return adaptations_applied
        
        return False
    
    def force_adapt(self) -> bool:
        """
        Force the node to adapt regardless of the health score.
        
        Returns:
            True if adaptations were applied, False otherwise
        """
        if not self.introspector:
            return False
        
        # Get adaptation recommendations
        recommendations = self.introspector.get_adaptation_recommendations(refresh=True)
        
        # Track whether any adaptations were applied
        adaptations_applied = False
        
        # Apply adaptations based on recommendations
        for recommendation in recommendations:
            recommendation_type = recommendation.get("type")
            description = recommendation.get("description", "")
            
            # Look for a handler for this type of recommendation
            for pattern, handler in self.adaptation_handlers.items():
                if pattern in description:
                    # Apply the adaptation
                    handler(recommendation)
                    adaptations_applied = True
                    break
        
        self.has_adapted = adaptations_applied
        return adaptations_applied
    
    def get_adaptation_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of adaptations applied to the node.
        
        Returns:
            A list of adaptation dictionaries
        """
        return self.adaptation_history
    
    def register_adaptation_handler(self, pattern: str, handler: Callable) -> None:
        """
        Register a new adaptation handler.
        
        Args:
            pattern: The pattern to match in recommendation descriptions
            handler: The handler function to call when the pattern is matched
        """
        self.adaptation_handlers[pattern] = handler


class AdaptiveFlow(Flow):
    """
    A flow that can adapt its behavior based on introspection results.
    
    This class extends the base Flow class to add adaptive capabilities,
    allowing the flow to modify its behavior and structure based on the
    agent's health status and recommendations.
    """
    
    def __init__(
        self,
        name: str,
        shared_store: SharedStore,
        nodes: List[Node],
        agent_dir: str,
        introspector: Optional[AgentIntrospector] = None,
        adaptation_threshold: float = 70.0,
        auto_adapt: bool = True,
        adaptation_handlers: Optional[Dict[str, Callable]] = None
    ) -> None:
        """
        Initialize the adaptive flow.
        
        Args:
            name: The name of the flow
            shared_store: The shared store for the agent
            nodes: The list of nodes in the flow
            agent_dir: The path to the agent directory
            introspector: Optional AgentIntrospector instance.
                         If not provided, a new one will be created.
            adaptation_threshold: The health score threshold below which adaptation is recommended.
            auto_adapt: Whether to automatically adapt when needed.
            adaptation_handlers: Optional dictionary mapping adaptation types
                                to handler functions that implement adaptation logic.
        """
        super().__init__(name, shared_store, nodes)
        self.agent_dir = agent_dir
        
        # Create an introspector if one wasn't provided
        self.introspector = introspector or AgentIntrospector(agent_dir)
        
        # Initialize adaptation state
        self.adaptation_threshold = adaptation_threshold
        self.auto_adapt = auto_adapt
        self.has_adapted = False
        self.adaptation_history = []
        
        # Initialize adaptation handlers
        self.adaptation_handlers = adaptation_handlers or {}
        if not self.adaptation_handlers:
            self._register_default_handlers()
    
    def _register_default_handlers(self) -> None:
        """
        Register default adaptation handlers.
        
        This method registers default handlers for common types of adaptations.
        Subclasses can override this method to register their own default handlers.
        """
        # Default handler for adding nodes
        self.adaptation_handlers["add_node"] = self._handle_add_node
        
        # Default handler for adding validation
        self.adaptation_handlers["add_validation"] = self._handle_add_validation
        
        # Default handler for optimizing the flow
        self.adaptation_handlers["optimize"] = self._handle_optimize
        
        # Default handler for reordering nodes
        self.adaptation_handlers["reorder"] = self._handle_reorder
    
    def _handle_add_node(self, adaptation: Dict[str, Any]) -> None:
        """
        Handle adding a node to the flow.
        
        Args:
            adaptation: The adaptation to apply
        """
        node_type = adaptation.get("node_type")
        position = adaptation.get("position", "end")
        
        # In a real implementation, this would create and add the node
        # For now, we just log the adaptation
        print(f"[AdaptiveFlow] Adding {node_type} node at position {position}")
    
    def _handle_add_validation(self, adaptation: Dict[str, Any]) -> None:
        """
        Handle adding validation to the flow.
        
        Args:
            adaptation: The adaptation to apply
        """
        # In a real implementation, this would add validation logic
        # For now, we just log the adaptation
        print(f"[AdaptiveFlow] Adding validation: {adaptation.get('description')}")
    
    def _handle_optimize(self, adaptation: Dict[str, Any]) -> None:
        """
        Handle optimizing the flow.
        
        Args:
            adaptation: The adaptation to apply
        """
        # In a real implementation, this would optimize the flow
        # For now, we just log the adaptation
        print(f"[AdaptiveFlow] Optimizing flow: {adaptation.get('description')}")
    
    def _handle_reorder(self, adaptation: Dict[str, Any]) -> None:
        """
        Handle reordering nodes in the flow.
        
        Args:
            adaptation: The adaptation to apply
        """
        # In a real implementation, this would reorder the nodes
        # For now, we just log the adaptation
        print(f"[AdaptiveFlow] Reordering nodes: {adaptation.get('description')}")
    
    def run(self) -> None:
        """
        Run the flow, with potential adaptation.
        
        This method first checks if adaptation is needed, and if so,
        applies the appropriate adaptations before executing the
        flow's normal execution logic.
        """
        # Check if adaptation is needed
        if not self.has_adapted and self.auto_adapt and self.introspector.should_adapt(self.adaptation_threshold):
            self._adapt()
        
        # Execute the flow's normal execution logic
        super().run()
    
    def _adapt(self) -> bool:
        """
        Adapt the flow's behavior based on introspection results.
        
        This method checks the agent's health status and recommendations,
        and applies the appropriate adaptations if needed.
        
        Returns:
            True if adaptations were applied, False otherwise
        """
        # Get adaptation recommendations
        recommendations = self.introspector.get_adaptation_recommendations()
        
        # Track whether any adaptations were applied
        adaptations_applied = False
        
        # Apply adaptations based on recommendations
        for recommendation in recommendations:
            adaptation = self._create_adaptation(recommendation)
            if adaptation:
                self._apply_adaptation(adaptation)
                self.adaptation_history.append(adaptation)
                adaptations_applied = True
        
        self.has_adapted = adaptations_applied
        return adaptations_applied
    
    def force_adapt(self) -> bool:
        """
        Force the flow to adapt regardless of the health score.
        
        Returns:
            True if adaptations were applied, False otherwise
        """
        # Get adaptation recommendations with a refresh
        recommendations = self.introspector.get_adaptation_recommendations(refresh=True)
        
        # Track whether any adaptations were applied
        adaptations_applied = False
        
        # Apply adaptations based on recommendations
        for recommendation in recommendations:
            adaptation = self._create_adaptation(recommendation)
            if adaptation:
                self._apply_adaptation(adaptation)
                self.adaptation_history.append(adaptation)
                adaptations_applied = True
        
        self.has_adapted = adaptations_applied
        return adaptations_applied
    
    def _create_adaptation(self, recommendation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Create an adaptation based on a recommendation.
        
        Args:
            recommendation: The recommendation to create an adaptation for
            
        Returns:
            An adaptation dictionary, or None if no adaptation could be created
        """
        recommendation_type = recommendation.get("type")
        description = recommendation.get("description", "")
        
        # Create different types of adaptations based on the recommendation
        if "missing module" in description:
            # Extract the missing module name
            module_name = description.split("missing module: ")[-1].split(" ")[0] if "missing module: " in description else "unknown"
            
            return {
                "type": "add_node",
                "node_type": module_name,
                "position": "end",  # Add the node at the end of the flow
                "description": f"Added {module_name} to address: {description}",
                "recommendation": description
            }
        
        elif "security" in description.lower():
            return {
                "type": "add_validation",
                "description": f"Added security validation to address: {description}",
                "recommendation": description
            }
        
        elif "performance" in description.lower():
            return {
                "type": "optimize",
                "description": f"Optimized flow to address: {description}",
                "recommendation": description
            }
        
        elif "order" in description.lower() or "sequence" in description.lower():
            return {
                "type": "reorder",
                "description": f"Reordered nodes to address: {description}",
                "recommendation": description
            }
        
        # If no specific adaptation type was identified, create a generic one
        return {
            "type": "generic",
            "description": f"Applied adaptation for: {description}",
            "recommendation": description
        }
    
    def _apply_adaptation(self, adaptation: Dict[str, Any]) -> None:
        """
        Apply an adaptation to the flow.
        
        Args:
            adaptation: The adaptation to apply
        """
        adaptation_type = adaptation.get("type")
        
        # Look for a handler for this type of adaptation
        if adaptation_type in self.adaptation_handlers:
            # Apply the adaptation using the registered handler
            self.adaptation_handlers[adaptation_type](adaptation)
        else:
            # Log the adaptation if no handler is registered
            print(f"[AdaptiveFlow] No handler for adaptation type: {adaptation_type}")
            print(f"[AdaptiveFlow] {adaptation.get('description')}")
    
    def get_adaptation_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of adaptations applied to the flow.
        
        Returns:
            A list of adaptation dictionaries
        """
        return self.adaptation_history
    
    def register_adaptation_handler(self, adaptation_type: str, handler: Callable) -> None:
        """
        Register a new adaptation handler.
        
        Args:
            adaptation_type: The type of adaptation to handle
            handler: The handler function to call for this type of adaptation
        """
        self.adaptation_handlers[adaptation_type] = handler
    
    def get_node_by_name(self, node_name: str) -> Optional[Node]:
        """
        Get a node by its name.
        
        Args:
            node_name: The name of the node to get
            
        Returns:
            The node with the specified name, or None if no such node exists
        """
        for node in self.nodes:
            if node.name == node_name:
                return node
        return None
    
    def add_node(self, node: Node, position: int = -1) -> None:
        """
        Add a node to the flow.
        
        Args:
            node: The node to add
            position: The position at which to add the node.
                     If -1, the node will be added at the end of the flow.
        """
        if position == -1 or position >= len(self.nodes):
            self.nodes.append(node)
        else:
            self.nodes.insert(position, node)
    
    def remove_node(self, node_name: str) -> bool:
        """
        Remove a node from the flow.
        
        Args:
            node_name: The name of the node to remove
            
        Returns:
            True if the node was removed, False otherwise
        """
        for i, node in enumerate(self.nodes):
            if node.name == node_name:
                self.nodes.pop(i)
                return True
        return False
    
    def reorder_nodes(self, node_names: List[str]) -> bool:
        """
        Reorder the nodes in the flow.
        
        Args:
            node_names: The names of the nodes in the desired order
            
        Returns:
            True if the nodes were reordered, False otherwise
        """
        # Check that all node names are valid
        for name in node_names:
            if not any(node.name == name for node in self.nodes):
                return False
        
        # Check that all nodes are accounted for
        if len(node_names) != len(self.nodes):
            return False
        
        # Create a new list of nodes in the desired order
        new_nodes = []
        for name in node_names:
            for node in self.nodes:
                if node.name == name:
                    new_nodes.append(node)
                    break
        
        # Update the nodes list
        self.nodes = new_nodes
        return True
