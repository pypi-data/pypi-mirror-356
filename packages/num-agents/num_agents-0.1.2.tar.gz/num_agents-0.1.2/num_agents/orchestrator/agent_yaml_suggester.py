"""
Agent YAML Suggester for the Nüm Agents SDK.

This module provides the AgentYamlSuggester class, which is responsible for
analyzing an agent design and suggesting modifications to the agent.yaml file.
"""

import os
from typing import Any, Dict, List, Optional, Set, Tuple

from num_agents.utils.file_io import read_yaml


class AgentYamlSuggester:
    """
    Suggester for agent.yaml modifications.
    
    This class is responsible for analyzing an agent design and suggesting
    modifications to the agent.yaml file to improve the agent's design.
    """
    
    def __init__(
        self,
        agent_spec: Dict[str, Any],
        univers_catalog: Dict[str, Any],
        consistency_results: Dict[str, Any],
        suggestions: List[Dict[str, Any]]
    ) -> None:
        """
        Initialize the agent.yaml suggester.
        
        Args:
            agent_spec: The agent specification
            univers_catalog: The universe catalog
            consistency_results: The results of the consistency check
            suggestions: The list of suggestions from the SuggestionEngine
        """
        self.agent_spec = agent_spec
        self.univers_catalog = univers_catalog
        self.consistency_results = consistency_results
        self.suggestions = suggestions
        
        # Map of universes to their modules
        self.univers_modules = self._build_univers_modules_map()
    
    def _build_univers_modules_map(self) -> Dict[str, Set[str]]:
        """
        Build a map of universes to their modules.
        
        Returns:
            A dictionary mapping universe names to sets of module names
        """
        univers_modules = {}
        
        # Extract universes and their modules from the universe catalog
        for univers_name, univers_data in self.univers_catalog.get("univers_catalog", {}).items():
            modules = set(univers_data.get("modules", []))
            univers_modules[univers_name] = modules
        
        return univers_modules
    
    def suggest_yaml_changes(self) -> Dict[str, Any]:
        """
        Suggest changes to the agent.yaml file.
        
        Returns:
            A dictionary containing suggested changes to the agent.yaml file
        """
        changes = {
            "add_universes": [],
            "add_modules": [],
            "remove_modules": [],
            "add_tags": [],
            "update_description": None
        }
        
        # Process missing modules
        missing_modules = set(self.consistency_results.get("missing_modules", []))
        if missing_modules:
            # Find universes that contain the missing modules
            for module in missing_modules:
                univers_for_module = self._find_universe_for_module(module)
                if univers_for_module:
                    # Check if the universe is already in the agent spec
                    if univers_for_module not in self.agent_spec.get("agent", {}).get("univers", []):
                        if univers_for_module not in changes["add_universes"]:
                            changes["add_universes"].append(univers_for_module)
                else:
                    # If no universe contains the module, suggest adding it as a custom module
                    changes["add_modules"].append(module)
        
        # Process unused modules
        unused_modules = set(self.consistency_results.get("unused_modules", []))
        if unused_modules:
            changes["remove_modules"].extend(list(unused_modules))
        
        # Process suggestions for tags and description
        for suggestion in self.suggestions:
            rule_id = suggestion.get("rule_id", "")
            
            # If it's a domain-specific suggestion, consider adding tags
            if rule_id.startswith("domain_specific_"):
                # Extract domain keywords from the suggestion
                text = suggestion.get("text", "")
                domain_keywords = self._extract_domain_keywords(text)
                
                # Add domain keywords as tags if they're not already present
                current_tags = self.agent_spec.get("agent", {}).get("tags", [])
                for keyword in domain_keywords:
                    if keyword not in current_tags and keyword not in changes["add_tags"]:
                        changes["add_tags"].append(keyword)
        
        # If there are critical security suggestions, add a note to the description
        has_security_issues = any(
            suggestion.get("rule_id", "").startswith("security_") and 
            suggestion.get("priority", "") == "critical"
            for suggestion in self.suggestions
        )
        
        if has_security_issues:
            current_description = self.agent_spec.get("agent", {}).get("description", "")
            security_note = "SECURITY NOTE: This agent has critical security issues that should be addressed."
            
            if security_note not in current_description:
                changes["update_description"] = f"{current_description}\n\n{security_note}"
        
        return changes
    
    def _find_universe_for_module(self, module: str) -> Optional[str]:
        """
        Find a universe that contains the specified module.
        
        Args:
            module: The module name
            
        Returns:
            The name of a universe containing the module, or None if not found
        """
        for univers_name, modules in self.univers_modules.items():
            if module in modules:
                return univers_name
        
        return None
    
    def _extract_domain_keywords(self, text: str) -> List[str]:
        """
        Extract domain keywords from a suggestion text.
        
        Args:
            text: The suggestion text
            
        Returns:
            A list of domain keywords
        """
        # This is a simple implementation that extracts domain-related words
        # In a real implementation, this would be more sophisticated
        domain_keywords = []
        
        # Look for common domain indicators in the text
        domain_indicators = [
            "conversational", "chatbot", "assistant",
            "data", "analysis", "analytics",
            "research", "knowledge", "information"
        ]
        
        for indicator in domain_indicators:
            if indicator in text.lower():
                domain_keywords.append(indicator)
        
        return domain_keywords
    
    def generate_yaml_diff(self) -> str:
        """
        Generate a human-readable diff of suggested changes to agent.yaml.
        
        Returns:
            A string containing a human-readable diff
        """
        changes = self.suggest_yaml_changes()
        diff_lines = []
        
        # Add universes
        if changes["add_universes"]:
            diff_lines.append("# Add the following universes:")
            for univers in changes["add_universes"]:
                diff_lines.append(f"+ univers: {univers}")
            diff_lines.append("")
        
        # Add modules (custom modules not in any universe)
        if changes["add_modules"]:
            diff_lines.append("# Add the following custom modules:")
            for module in changes["add_modules"]:
                diff_lines.append(f"+ custom_module: {module}")
            diff_lines.append("")
        
        # Remove modules
        if changes["remove_modules"]:
            diff_lines.append("# Remove the following unused modules:")
            for module in changes["remove_modules"]:
                diff_lines.append(f"- module: {module}")
            diff_lines.append("")
        
        # Add tags
        if changes["add_tags"]:
            diff_lines.append("# Add the following tags:")
            for tag in changes["add_tags"]:
                diff_lines.append(f"+ tag: {tag}")
            diff_lines.append("")
        
        # Update description
        if changes["update_description"]:
            diff_lines.append("# Update the description:")
            diff_lines.append(f"- description: {self.agent_spec.get('agent', {}).get('description', '')}")
            diff_lines.append(f"+ description: {changes['update_description']}")
            diff_lines.append("")
        
        return "\n".join(diff_lines)
