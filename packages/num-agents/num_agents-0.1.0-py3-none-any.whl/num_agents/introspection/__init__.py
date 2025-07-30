"""
Introspection package for the Nüm Agents SDK.

This package provides mechanisms for agents to access their own metadata,
logical graph, and audit report at runtime, facilitating self-diagnosis
and dynamic adaptation.
"""

from num_agents.introspection.agent_introspector import AgentIntrospector
from num_agents.introspection.adaptive_flow import AdaptiveFlow, AdaptiveNode

__all__ = ["AgentIntrospector", "AdaptiveFlow", "AdaptiveNode"]
