"""
Agent Introspector for the Nüm Agents SDK.

This module provides the AgentIntrospector class, which enables agents to
access their own metadata, logical graph, and audit report at runtime,
facilitating self-diagnosis and dynamic adaptation.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from num_agents.orchestrator.meta_orchestrator import MetaOrchestrator


class AgentIntrospector:
    """
    Introspector for agent self-analysis and adaptation.
    
    This class provides mechanisms for a running agent to access its own
    metadata, logical graph, and audit report, enabling self-diagnosis
    and dynamic adaptation of its flow.
    """
    
    def __init__(
        self,
        agent_dir: str,
        agent_spec_path: Optional[str] = None,
        univers_catalog_path: Optional[str] = None,
        rules_path: Optional[str] = None
    ) -> None:
        """
        Initialize the agent introspector.
        
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
        
        # Set the agent specification path
        if agent_spec_path:
            self.agent_spec_path = agent_spec_path
        else:
            self.agent_spec_path = os.path.join(agent_dir, "agent.yaml")
        
        # Set paths for metadata
        self.logical_graph_path = os.path.join(agent_dir, "logical_graph.mmd")
        self.audit_report_path = os.path.join(agent_dir, "audit_report.json")
        
        # Create a MetaOrchestrator instance for on-demand analysis
        self.meta_orchestrator = MetaOrchestrator(
            agent_dir=agent_dir,
            agent_spec_path=agent_spec_path,
            univers_catalog_path=univers_catalog_path,
            rules_path=rules_path
        )
    
    def get_logical_graph(self, refresh: bool = False) -> str:
        """
        Get the agent's logical graph.
        
        Args:
            refresh: If True, regenerate the logical graph before returning it.
                    Otherwise, use the existing file if available.
        
        Returns:
            The logical graph as a Mermaid flowchart string
        """
        if refresh or not os.path.exists(self.logical_graph_path):
            # TODO: Implement logic to regenerate the logical graph
            # For now, we'll just use the MetaOrchestrator to analyze the agent
            # and assume the logical graph is generated as a side effect
            self.meta_orchestrator.analyze()
        
        # Read the logical graph file
        if os.path.exists(self.logical_graph_path):
            with open(self.logical_graph_path, "r") as f:
                return f.read()
        else:
            return "No logical graph available"
    
    def get_audit_report(self, refresh: bool = False) -> Dict[str, Any]:
        """
        Get the agent's audit report.
        
        Args:
            refresh: If True, regenerate the audit report before returning it.
                    Otherwise, use the existing file if available.
        
        Returns:
            The audit report as a dictionary
        """
        if refresh or not os.path.exists(self.audit_report_path):
            # Generate a new audit report
            report = self.meta_orchestrator.analyze()
            
            # Write the report to the audit report path
            with open(self.audit_report_path, "w") as f:
                json.dump(report, f, indent=2)
            
            return report
        else:
            # Read the existing audit report
            with open(self.audit_report_path, "r") as f:
                return json.load(f)
    
    def get_health_status(self, refresh: bool = False) -> Dict[str, Any]:
        """
        Get the agent's health status.
        
        Args:
            refresh: If True, regenerate the health status before returning it.
                    Otherwise, use the existing audit report if available.
        
        Returns:
            A dictionary containing the agent's health status
        """
        # Get the audit report
        report = self.get_audit_report(refresh)
        
        # Extract the health status
        validation = report.get("validation", {})
        
        return {
            "agent_name": validation.get("agent_name", "Unknown"),
            "status": validation.get("status", "unknown"),
            "health_score": validation.get("health_score", 0),
            "completeness": validation.get("completeness", 0),
            "issue_count": len(validation.get("issues", [])),
            "critical_suggestion_count": len(validation.get("suggestions", {}).get("critical", [])),
            "high_suggestion_count": len(validation.get("suggestions", {}).get("high", [])),
            "medium_suggestion_count": len(validation.get("suggestions", {}).get("medium", [])),
            "low_suggestion_count": len(validation.get("suggestions", {}).get("low", []))
        }
    
    def get_critical_issues(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get the agent's critical issues.
        
        Args:
            refresh: If True, regenerate the audit report before returning issues.
                    Otherwise, use the existing audit report if available.
        
        Returns:
            A list of critical issues
        """
        # Get the audit report
        report = self.get_audit_report(refresh)
        
        # Extract critical issues
        validation = report.get("validation", {})
        issues = validation.get("issues", [])
        
        # Filter for critical issues (missing modules, etc.)
        return [issue for issue in issues if issue.get("severity", "") == "critical"]
    
    def get_critical_suggestions(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get the agent's critical suggestions.
        
        Args:
            refresh: If True, regenerate the audit report before returning suggestions.
                    Otherwise, use the existing audit report if available.
        
        Returns:
            A list of critical suggestions
        """
        # Get the audit report
        report = self.get_audit_report(refresh)
        
        # Extract critical suggestions
        validation = report.get("validation", {})
        suggestions = validation.get("suggestions", {})
        
        return suggestions.get("critical", [])
    
    def get_node_metadata(self, node_name: str, refresh: bool = False) -> Dict[str, Any]:
        """
        Get metadata for a specific node.
        
        Args:
            node_name: The name of the node
            refresh: If True, regenerate the audit report before returning node metadata.
                    Otherwise, use the existing audit report if available.
        
        Returns:
            A dictionary containing metadata for the specified node
        """
        # Get the audit report
        report = self.get_audit_report(refresh)
        
        # Extract node metadata
        validation = report.get("validation", {})
        nodes = validation.get("nodes", {})
        
        return nodes.get(node_name, {"status": "unknown", "issues": [], "suggestions": []})
    
    def should_adapt(self, health_threshold: float = 70.0, refresh: bool = False) -> bool:
        """
        Determine if the agent should adapt based on its health status.
        
        Args:
            health_threshold: The health score threshold below which adaptation is recommended
            refresh: If True, regenerate the health status before making the determination.
                    Otherwise, use the existing audit report if available.
        
        Returns:
            True if adaptation is recommended, False otherwise
        """
        # Get the health status
        health_status = self.get_health_status(refresh)
        
        # Check if the health score is below the threshold
        return health_status["health_score"] < health_threshold
    
    def get_adaptation_recommendations(self, refresh: bool = False) -> List[Dict[str, Any]]:
        """
        Get recommendations for adapting the agent.
        
        Args:
            refresh: If True, regenerate the audit report before returning recommendations.
                    Otherwise, use the existing audit report if available.
        
        Returns:
            A list of adaptation recommendations
        """
        # Get critical issues and suggestions
        critical_issues = self.get_critical_issues(refresh)
        critical_suggestions = self.get_critical_suggestions(refresh)
        
        # Combine issues and suggestions into recommendations
        recommendations = []
        
        # Add recommendations for critical issues
        for issue in critical_issues:
            recommendations.append({
                "type": "issue",
                "severity": "critical",
                "description": issue.get("description", ""),
                "recommendation": f"Fix {issue.get('type', 'unknown')} issue: {issue.get('description', '')}"
            })
        
        # Add recommendations for critical suggestions
        for suggestion in critical_suggestions:
            recommendations.append({
                "type": "suggestion",
                "severity": "critical",
                "description": suggestion.get("text", ""),
                "recommendation": suggestion.get("text", "")
            })
        
        return recommendations
