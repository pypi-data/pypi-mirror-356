"""
Flow module for the Nüm Agents SDK.

This module provides classes for implementing different types of flows,
including conditional and parallel flows.
"""

from num_agents.flow.conditional_flow import (
    ConditionalFlow,
    ConditionalNode,
    Transition,
    TransitionType,
    check_key_equals,
    check_key_exists,
)
