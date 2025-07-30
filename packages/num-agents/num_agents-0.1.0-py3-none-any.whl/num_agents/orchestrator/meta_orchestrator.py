"""
Meta-Orchestrator implementation for the Nüm Agents SDK.

This module provides the MetaOrchestrator class, which is responsible for
validating agent designs, checking for consistency, and providing suggestions
for improvements.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from num_agents.orchestrator.agent_yaml_suggester import AgentYamlSuggester
from num_agents.univers.univers_catalog_loader import UniversCatalogLoader
from num_agents.utils.file_io import AgentSpecLoader, read_yaml


class ConsistencyChecker:
    """
    Checker for agent design consistency.
    
    This class is responsible for checking the consistency of an agent design,
    comparing the declared modules with the nodes present in the flow.
    """
    
    def __init__(
        self,
        agent_spec: Dict[str, Any],
        univers_catalog: Dict[str, Any],
        graph_nodes: Set[str]
    ) -> None:
        """
        Initialize the consistency checker.
        
        Args:
            agent_spec: The agent specification
            univers_catalog: The universe catalog
            graph_nodes: The set of node names in the logical graph
        """
        self.agent_spec = agent_spec
        self.univers_catalog = univers_catalog
        self.graph_nodes = graph_nodes
    
    def check(self) -> Dict[str, Any]:
        """
        Check the consistency of the agent design.
        
        Returns:
            A dictionary containing the results of the consistency check
        """
        # Get the declared universes
        universes = self.agent_spec["agent"]["univers"]
        
        # Resolve the declared modules
        declared_modules = set()
        for universe in universes:
            universe_modules = self.univers_catalog.get("univers_catalog", {}).get(universe, {}).get("modules", [])
            declared_modules.update(universe_modules)
        
        # Find missing modules (nodes in the graph but not declared)
        missing_modules = self.graph_nodes - declared_modules
        
        # Find unused modules (declared but not in the graph)
        unused_modules = declared_modules - self.graph_nodes
        
        return {
            "declared_modules": list(declared_modules),
            "graph_nodes": list(self.graph_nodes),
            "missing_modules": list(missing_modules),
            "unused_modules": list(unused_modules),
            "is_consistent": len(missing_modules) == 0
        }


class SuggestionEngine:
    """
    Engine for suggesting improvements to agent designs.
    
    This class is responsible for analyzing an agent design and suggesting
    improvements based on best practices and common patterns. It uses a rule-based
    system defined in a configuration file to generate context-aware suggestions.
    """
    
    def __init__(
        self,
        agent_spec: Dict[str, Any],
        univers_catalog: Dict[str, Any],
        consistency_results: Dict[str, Any],
        rules_path: Optional[str] = None
    ) -> None:
        """
        Initialize the suggestion engine.
        
        Args:
            agent_spec: The agent specification
            univers_catalog: The universe catalog
            consistency_results: The results of the consistency check
            rules_path: Optional path to the suggestion rules YAML file.
                       If not provided, the default path will be used.
        """
        self.agent_spec = agent_spec
        self.univers_catalog = univers_catalog
        self.consistency_results = consistency_results
        
        # Load suggestion rules
        if not rules_path:
            # Default path is in the config directory
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            rules_path = os.path.join(base_dir, "config", "suggestion_rules.yaml")
        
        self.rules = self._load_rules(rules_path)
    
    def _load_rules(self, rules_path: str) -> Dict[str, Any]:
        """
        Load suggestion rules from a YAML file.
        
        Args:
            rules_path: Path to the suggestion rules YAML file
            
        Returns:
            A dictionary containing the suggestion rules
        """
        if os.path.exists(rules_path):
            return read_yaml(rules_path)
        else:
            # Return empty rules if file doesn't exist
            return {"rules": {}}
    
    def suggest(self) -> List[Dict[str, Any]]:
        """
        Generate suggestions for improving the agent design.
        
        Returns:
            A list of suggestion dictionaries, each containing the suggestion text,
            priority, and rule ID.
        """
        suggestions = []
        
        # Get the active modules
        active_modules = set(self.consistency_results["graph_nodes"])
        
        # Add basic suggestions for missing and unused modules
        suggestions.extend(self._suggest_missing_modules())
        suggestions.extend(self._suggest_unused_modules())
        
        # Apply rule-based suggestions
        suggestions.extend(self._apply_module_combination_rules(active_modules))
        suggestions.extend(self._apply_missing_dependency_rules(active_modules))
        suggestions.extend(self._apply_domain_specific_rules(active_modules))
        suggestions.extend(self._apply_performance_rules(active_modules))
        suggestions.extend(self._apply_security_rules(active_modules))
        
        # Sort suggestions by priority
        priority_map = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        suggestions.sort(key=lambda x: priority_map.get(x.get("priority", "low"), 3))
        
        return suggestions
    
    def get_suggestion_texts(self) -> List[str]:
        """
        Get the suggestion texts for backward compatibility.
        
        Returns:
            A list of suggestion strings
        """
        suggestions = self.suggest()
        return [s["text"] for s in suggestions]
    
    def _suggest_missing_modules(self) -> List[Dict[str, Any]]:
        """
        Suggest adding missing modules.
        
        Returns:
            A list of suggestion dictionaries
        """
        suggestions = []
        for module in self.consistency_results["missing_modules"]:
            suggestions.append({
                "text": f"Add '{module}' to the agent specification (it's used in the flow but not declared).",
                "priority": "critical",
                "rule_id": "basic_missing_module"
            })
        return suggestions
    
    def _suggest_unused_modules(self) -> List[Dict[str, Any]]:
        """
        Suggest removing unused modules.
        
        Returns:
            A list of suggestion dictionaries
        """
        suggestions = []
        for module in self.consistency_results["unused_modules"]:
            suggestions.append({
                "text": f"Consider removing '{module}' from the agent specification (it's declared but not used in the flow).",
                "priority": "low",
                "rule_id": "basic_unused_module"
            })
        return suggestions
    
    def _apply_module_combination_rules(self, active_modules: Set[str]) -> List[Dict[str, Any]]:
        """
        Apply module combination rules.
        
        Args:
            active_modules: Set of active module names
            
        Returns:
            A list of suggestion dictionaries
        """
        suggestions = []
        
        # Get module combination rules
        combination_rules = self.rules.get("rules", {}).get("module_combination", [])
        
        for rule in combination_rules:
            # Check if the rule condition is met
            present_modules = set(rule.get("condition", {}).get("present", []))
            absent_modules = set(rule.get("condition", {}).get("absent", []))
            
            if present_modules.issubset(active_modules) and not absent_modules.intersection(active_modules):
                suggestions.append({
                    "text": rule.get("suggestion", ""),
                    "priority": rule.get("priority", "medium"),
                    "rule_id": rule.get("id", "unknown")
                })
        
        return suggestions
    
    def _apply_missing_dependency_rules(self, active_modules: Set[str]) -> List[Dict[str, Any]]:
        """
        Apply missing dependency rules.
        
        Args:
            active_modules: Set of active module names
            
        Returns:
            A list of suggestion dictionaries
        """
        suggestions = []
        
        # Get missing dependency rules
        dependency_rules = self.rules.get("rules", {}).get("missing_dependency", [])
        
        for rule in dependency_rules:
            # Check if the rule condition is met
            present_modules = set(rule.get("condition", {}).get("present", []))
            absent_modules = set(rule.get("condition", {}).get("absent", []))
            
            if present_modules.issubset(active_modules) and absent_modules.isdisjoint(active_modules):
                suggestions.append({
                    "text": rule.get("suggestion", ""),
                    "priority": rule.get("priority", "high"),
                    "rule_id": rule.get("id", "unknown")
                })
        
        return suggestions
    
    def _apply_domain_specific_rules(self, active_modules: Set[str]) -> List[Dict[str, Any]]:
        """
        Apply domain-specific rules based on the agent's declared domain.
        
        Args:
            active_modules: Set of active module names
            
        Returns:
            A list of suggestion dictionaries
        """
        suggestions = []
        
        # Get domain-specific rules
        domain_rules = self.rules.get("rules", {}).get("domain_specific", [])
        
        # Extract agent domain from description or tags if available
        agent_domain = []
        if "agent" in self.agent_spec:
            # Extract keywords from description
            description = self.agent_spec["agent"].get("description", "").lower()
            if description:
                # Simple keyword extraction
                agent_domain.extend([word.strip() for word in description.split()])
            
            # Extract tags if available
            tags = self.agent_spec["agent"].get("tags", [])
            if tags:
                agent_domain.extend([tag.lower() for tag in tags])
        
        for rule in domain_rules:
            # Check if any domain keywords match
            domain_keywords = set(rule.get("condition", {}).get("domain", []))
            absent_modules = set(rule.get("condition", {}).get("absent", []))
            
            # If any domain keyword matches and the absent modules are not present
            if any(keyword in agent_domain for keyword in domain_keywords) and \
               absent_modules.isdisjoint(active_modules):
                suggestions.append({
                    "text": rule.get("suggestion", ""),
                    "priority": rule.get("priority", "medium"),
                    "rule_id": rule.get("id", "unknown")
                })
        
        return suggestions
    
    def _apply_performance_rules(self, active_modules: Set[str]) -> List[Dict[str, Any]]:
        """
        Apply performance optimization rules.
        
        Args:
            active_modules: Set of active module names
            
        Returns:
            A list of suggestion dictionaries
        """
        suggestions = []
        
        # Get performance rules
        performance_rules = self.rules.get("rules", {}).get("performance", [])
        
        for rule in performance_rules:
            # Check if the rule condition is met
            present_modules = set(rule.get("condition", {}).get("present", []))
            absent_modules = set(rule.get("condition", {}).get("absent", []))
            node_count_condition = rule.get("condition", {}).get("node_count", "")
            
            # Check node count condition if specified
            node_count_met = True
            if node_count_condition:
                node_count = len(active_modules)
                if node_count_condition.startswith(">"):
                    threshold = int(node_count_condition[1:])
                    node_count_met = node_count > threshold
                elif node_count_condition.startswith("<"):
                    threshold = int(node_count_condition[1:])
                    node_count_met = node_count < threshold
                elif node_count_condition.startswith("="):
                    threshold = int(node_count_condition[1:])
                    node_count_met = node_count == threshold
            
            if present_modules.issubset(active_modules) and \
               absent_modules.isdisjoint(active_modules) and \
               node_count_met:
                suggestions.append({
                    "text": rule.get("suggestion", ""),
                    "priority": rule.get("priority", "medium"),
                    "rule_id": rule.get("id", "unknown")
                })
        
        return suggestions
    
    def _apply_security_rules(self, active_modules: Set[str]) -> List[Dict[str, Any]]:
        """
        Apply security best practice rules.
        
        Args:
            active_modules: Set of active module names
            
        Returns:
            A list of suggestion dictionaries
        """
        suggestions = []
        
        # Get security rules
        security_rules = self.rules.get("rules", {}).get("security", [])
        
        for rule in security_rules:
            # Check if the rule condition is met
            present_modules = set(rule.get("condition", {}).get("present", []))
            absent_modules = set(rule.get("condition", {}).get("absent", []))
            
            if present_modules.issubset(active_modules) and absent_modules.isdisjoint(active_modules):
                suggestions.append({
                    "text": rule.get("suggestion", ""),
                    "priority": rule.get("priority", "critical"),
                    "rule_id": rule.get("id", "unknown")
                })
        
        return suggestions


class ReportBuilder:
    """
    Builder for agent audit reports.
    
    This class is responsible for building audit reports for agent designs,
    summarizing the results of consistency checks and suggestions.
    """
    
    def __init__(
        self,
        agent_spec: Dict[str, Any],
        consistency_results: Dict[str, Any],
        suggestions: List[Dict[str, Any]]
    ) -> None:
        """
        Initialize the report builder.
        
        Args:
            agent_spec: The agent specification
            consistency_results: The results of the consistency check
            suggestions: The list of suggestion dictionaries
        """
        self.agent_spec = agent_spec
        self.consistency_results = consistency_results
        self.suggestions = suggestions
    
    def build(self) -> Dict[str, Any]:
        """
        Build the audit report.
        
        Returns:
            A dictionary containing the audit report
        """
        # Calculate completeness percentage
        total_modules = len(self.consistency_results["declared_modules"])
        if total_modules > 0:
            unused_modules = len(self.consistency_results["unused_modules"])
            completeness = 100 - (unused_modules * 100 / total_modules)
        else:
            completeness = 0
        
        # Group suggestions by priority
        critical_suggestions = []
        high_priority_suggestions = []
        medium_priority_suggestions = []
        low_priority_suggestions = []
        
        for suggestion in self.suggestions:
            priority = suggestion.get("priority", "medium")
            if priority == "critical":
                critical_suggestions.append(suggestion)
            elif priority == "high":
                high_priority_suggestions.append(suggestion)
            elif priority == "medium":
                medium_priority_suggestions.append(suggestion)
            else:
                low_priority_suggestions.append(suggestion)
        
        # Calculate health score based on issues and critical suggestions
        missing_modules_count = len(self.consistency_results["missing_modules"])
        critical_suggestions_count = len(critical_suggestions)
        health_score = 100
        
        # Deduct points for missing modules (10 points each)
        health_score -= min(50, missing_modules_count * 10)
        
        # Deduct points for critical suggestions (5 points each)
        health_score -= min(30, critical_suggestions_count * 5)
        
        # Ensure health score is between 0 and 100
        health_score = max(0, min(100, health_score))
        
        return {
            "validation": {
                "agent_name": self.agent_spec["agent"]["name"],
                "status": "valid" if self.consistency_results["is_consistent"] else "invalid",
                "health_score": health_score,
                "issues": [
                    {"type": "missing_module", "module": module}
                    for module in self.consistency_results["missing_modules"]
                ] + [
                    {"type": "unused_module", "module": module}
                    for module in self.consistency_results["unused_modules"]
                ],
                "suggestions": {
                    "critical": critical_suggestions,
                    "high": high_priority_suggestions,
                    "medium": medium_priority_suggestions,
                    "low": low_priority_suggestions
                },
                "completeness": f"{completeness:.1f}%",
                "declared_modules": self.consistency_results["declared_modules"],
                "graph_nodes": self.consistency_results["graph_nodes"]
            }
        }


class MetaOrchestrator:
    """
    Orchestrator for validating and supervising agent designs.
    
    This class is responsible for coordinating the validation and supervision
    of agent designs, using the ConsistencyChecker, SuggestionEngine, and
    ReportBuilder. It provides advanced capabilities for analyzing agent designs,
    generating context-aware suggestions, and calculating a health score.
    """
    
    def __init__(
        self,
        agent_dir: str,
        agent_spec_path: Optional[str] = None,
        univers_catalog_path: Optional[str] = None,
        rules_path: Optional[str] = None
    ) -> None:
        """
        Initialize the meta-orchestrator.
        
        Args:
            agent_dir: Path to the agent directory
            agent_spec_path: Optional path to the agent specification YAML file.
                            If not provided, it will be looked for in the agent directory.
            univers_catalog_path: Optional path to the universe catalog YAML file.
                                  If not provided, the default path will be used.
            rules_path: Optional path to the suggestion rules YAML file.
                       If not provided, the default path will be used.
        """
        self.agent_dir = agent_dir
        self.rules_path = rules_path
        
        # Set the agent specification path
        if agent_spec_path:
            self.agent_spec_path = agent_spec_path
        else:
            self.agent_spec_path = os.path.join(agent_dir, "agent.yaml")
        
        # Load the agent specification
        self.agent_spec_loader = AgentSpecLoader(self.agent_spec_path)
        self.agent_spec = self.agent_spec_loader.load()
        
        # Load the universe catalog
        self.univers_catalog_loader = UniversCatalogLoader(univers_catalog_path)
        self.univers_catalog = self.univers_catalog_loader.load()
        
        # Set the logical graph path
        self.logical_graph_path = os.path.join(agent_dir, "logical_graph.mmd")
    
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the agent design.
        
        This method coordinates the validation and supervision of the agent design,
        using the ConsistencyChecker, SuggestionEngine, and ReportBuilder.
        
        Returns:
            A dictionary containing the audit report with validation status,
            health score, issues, and prioritized suggestions.
        """
        # Extract node names from the logical graph
        graph_nodes = self._extract_nodes_from_graph()
        
        # Check consistency
        checker = ConsistencyChecker(self.agent_spec, self.univers_catalog, graph_nodes)
        consistency_results = checker.check()
        
        # Generate suggestions with the enhanced rule-based system
        suggestion_engine = SuggestionEngine(
            self.agent_spec, 
            self.univers_catalog, 
            consistency_results,
            self.rules_path
        )
        suggestions = suggestion_engine.suggest()
        
        # Build the report with the new format
        report_builder = ReportBuilder(self.agent_spec, consistency_results, suggestions)
        report = report_builder.build()
        
        return report
    
    def export_report(self, output_path: Optional[str] = None) -> str:
        """
        Export the audit report to a file.
        
        Args:
            output_path: Optional path to write the report to.
                        If not provided, it will be written to audit_report.json
                        in the agent directory.
        
        Returns:
            The path to the exported report
        """
        # Generate the report
        report = self.analyze()
        
        # Set the output path
        if not output_path:
            output_path = os.path.join(self.agent_dir, "audit_report.json")
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the report
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)
        
        return output_path
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the agent analysis.
        
        Returns:
            A dictionary containing a summary of the analysis, including
            the agent name, status, health score, and counts of issues and
            suggestions by priority.
        """
        report = self.analyze()
        validation = report["validation"]
        
        # Count issues and suggestions
        issue_count = len(validation["issues"])
        suggestion_counts = {
            "critical": len(validation["suggestions"]["critical"]),
            "high": len(validation["suggestions"]["high"]),
            "medium": len(validation["suggestions"]["medium"]),
            "low": len(validation["suggestions"]["low"])
        }
        
        return {
            "agent_name": validation["agent_name"],
            "status": validation["status"],
            "health_score": validation["health_score"],
            "completeness": validation["completeness"],
            "issue_count": issue_count,
            "suggestion_counts": suggestion_counts
        }
    
    def get_critical_suggestions(self) -> List[str]:
        """
        Get a list of critical suggestions that should be addressed.
        
        Returns:
            A list of critical suggestion texts
        """
        report = self.analyze()
        critical_suggestions = report["validation"]["suggestions"]["critical"]
        return [suggestion["text"] for suggestion in critical_suggestions]
        
    def suggest_yaml_modifications(self) -> Dict[str, Any]:
        """
        Suggest modifications to the agent.yaml file.
        
        This method analyzes the agent design and suggests modifications to the
        agent.yaml file to improve the agent's design based on the validation
        results and suggestions.
        
        Returns:
            A dictionary containing suggested changes to the agent.yaml file
        """
        # Get validation results and suggestions
        report = self.analyze()
        validation = report["validation"]
        suggestions = []
        
        # Flatten suggestions from all priority levels
        for priority in ["critical", "high", "medium", "low"]:
            suggestions.extend(validation["suggestions"][priority])
        
        # Create an AgentYamlSuggester instance
        yaml_suggester = AgentYamlSuggester(
            self.agent_spec,
            self.univers_catalog,
            {
                "declared_modules": validation["declared_modules"],
                "graph_nodes": validation["graph_nodes"],
                "missing_modules": [issue["module"] for issue in validation["issues"] 
                                   if issue["type"] == "missing_module"],
                "unused_modules": [issue["module"] for issue in validation["issues"]
                                  if issue["type"] == "unused_module"],
                "is_consistent": validation["status"] == "valid"
            },
            suggestions
        )
        
        # Get suggested changes
        return yaml_suggester.suggest_yaml_changes()
        
    def generate_yaml_diff(self) -> str:
        """
        Generate a human-readable diff of suggested changes to agent.yaml.
        
        Returns:
            A string containing a human-readable diff
        """
        # Get validation results and suggestions
        report = self.analyze()
        validation = report["validation"]
        suggestions = []
        
        # Flatten suggestions from all priority levels
        for priority in ["critical", "high", "medium", "low"]:
            suggestions.extend(validation["suggestions"][priority])
        
        # Create an AgentYamlSuggester instance
        yaml_suggester = AgentYamlSuggester(
            self.agent_spec,
            self.univers_catalog,
            {
                "declared_modules": validation["declared_modules"],
                "graph_nodes": validation["graph_nodes"],
                "missing_modules": [issue["module"] for issue in validation["issues"] 
                                   if issue["type"] == "missing_module"],
                "unused_modules": [issue["module"] for issue in validation["issues"]
                                  if issue["type"] == "unused_module"],
                "is_consistent": validation["status"] == "valid"
            },
            suggestions
        )
        
        # Generate diff
        return yaml_suggester.generate_yaml_diff()
        
    def export_yaml_suggestions(self, output_path: Optional[str] = None) -> str:
        """
        Export the suggested changes to the agent.yaml file.
        
        Args:
            output_path: Optional path to write the suggestions to.
                        If not provided, it will be written to agent_yaml_suggestions.txt
                        in the agent directory.
        
        Returns:
            The path to the exported suggestions
        """
        # Generate the diff
        diff = self.generate_yaml_diff()
        
        # Set the output path
        if not output_path:
            output_path = os.path.join(self.agent_dir, "agent_yaml_suggestions.txt")
        
        # Create directory if it doesn't exist
        directory = os.path.dirname(output_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Write the diff
        with open(output_path, "w") as f:
            f.write(diff)
        
        return output_path
    
    def _extract_nodes_from_graph(self) -> Set[str]:
        """
        Extract node names from the logical graph.
        
        Returns:
            A set of node names
        """
        if not os.path.exists(self.logical_graph_path):
            return set()
        
        nodes = set()
        with open(self.logical_graph_path, "r") as f:
            for line in f:
                # Look for node definitions (e.g., "NodeName[\"NodeName\n(description)\"]")
                if "[" in line and "]" in line:
                    node_name = line.split("[")[0].strip()
                    nodes.add(node_name)
                
                # Look for edges (e.g., "NodeA --> NodeB")
                elif "-->" in line:
                    parts = line.strip().split("-->")
                    if len(parts) == 2:
                        nodes.add(parts[0].strip())
                        nodes.add(parts[1].strip())
        
        return nodes


def analyze_agent(
    agent_dir: str,
    agent_spec_path: Optional[str] = None,
    univers_catalog_path: Optional[str] = None,
    output_path: Optional[str] = None
) -> str:
    """
    Analyze an agent and generate an audit report.
    
    Args:
        agent_dir: Path to the agent directory
        agent_spec_path: Optional path to the agent specification YAML file
        univers_catalog_path: Optional path to the universe catalog YAML file
        output_path: Optional path to write the report to
        
    Returns:
        The path to the exported report
    """
    orchestrator = MetaOrchestrator(agent_dir, agent_spec_path, univers_catalog_path)
    return orchestrator.export_report(output_path)
