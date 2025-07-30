"""
Tests for the AgentYamlSuggester class.
"""

import os
import pytest
from typing import Dict, Any, List

from num_agents.orchestrator.agent_yaml_suggester import AgentYamlSuggester


@pytest.fixture
def sample_agent_spec() -> Dict[str, Any]:
    """
    Sample agent specification for testing.
    """
    return {
        "agent": {
            "name": "test_agent",
            "description": "A test agent for unit testing",
            "univers": ["core", "tools"],
            "modules": ["ManagerGoalNode", "ToolAdapterNode"],
            "tags": ["test", "demo"]
        }
    }


@pytest.fixture
def sample_univers_catalog() -> Dict[str, Any]:
    """
    Sample universe catalog for testing.
    """
    return {
        "univers_catalog": {
            "core": {
                "description": "Core universe with essential modules",
                "modules": ["ManagerGoalNode", "MemoryNode", "OutputNode"]
            },
            "tools": {
                "description": "Tool-related modules",
                "modules": ["ToolAdapterNode", "ToolResultNode"]
            },
            "security": {
                "description": "Security-related modules",
                "modules": ["SandboxNode", "ValidationNode"]
            },
            "learning": {
                "description": "Learning-related modules",
                "modules": ["ActiveLearningNode", "FeedbackNode"]
            }
        }
    }


@pytest.fixture
def sample_consistency_results() -> Dict[str, Any]:
    """
    Sample consistency check results for testing.
    """
    return {
        "declared_modules": ["ManagerGoalNode", "ToolAdapterNode"],
        "graph_nodes": ["ManagerGoalNode", "ToolAdapterNode"],
        "missing_modules": ["ValidationNode"],
        "unused_modules": [],
        "is_consistent": False
    }


@pytest.fixture
def sample_suggestions() -> List[Dict[str, Any]]:
    """
    Sample suggestions for testing.
    """
    return [
        {
            "rule_id": "security_validation",
            "text": "Consider adding ValidationNode to validate inputs for security",
            "priority": "critical"
        },
        {
            "rule_id": "domain_specific_conversational",
            "text": "For conversational agents, consider adding MemoryNode to maintain context",
            "priority": "high"
        }
    ]


def test_init(sample_agent_spec, sample_univers_catalog, sample_consistency_results, sample_suggestions):
    """
    Test initialization of AgentYamlSuggester.
    """
    suggester = AgentYamlSuggester(
        sample_agent_spec,
        sample_univers_catalog,
        sample_consistency_results,
        sample_suggestions
    )
    
    assert suggester.agent_spec == sample_agent_spec
    assert suggester.univers_catalog == sample_univers_catalog
    assert suggester.consistency_results == sample_consistency_results
    assert suggester.suggestions == sample_suggestions
    
    # Check that the univers_modules map is built correctly
    assert "core" in suggester.univers_modules
    assert "tools" in suggester.univers_modules
    assert "security" in suggester.univers_modules
    assert "learning" in suggester.univers_modules
    
    assert "ManagerGoalNode" in suggester.univers_modules["core"]
    assert "MemoryNode" in suggester.univers_modules["core"]
    assert "OutputNode" in suggester.univers_modules["core"]
    
    assert "ToolAdapterNode" in suggester.univers_modules["tools"]
    assert "ToolResultNode" in suggester.univers_modules["tools"]
    
    assert "SandboxNode" in suggester.univers_modules["security"]
    assert "ValidationNode" in suggester.univers_modules["security"]
    
    assert "ActiveLearningNode" in suggester.univers_modules["learning"]
    assert "FeedbackNode" in suggester.univers_modules["learning"]


def test_find_universe_for_module(sample_agent_spec, sample_univers_catalog, sample_consistency_results, sample_suggestions):
    """
    Test _find_universe_for_module method.
    """
    suggester = AgentYamlSuggester(
        sample_agent_spec,
        sample_univers_catalog,
        sample_consistency_results,
        sample_suggestions
    )
    
    # Test finding universes for existing modules
    assert suggester._find_universe_for_module("ManagerGoalNode") == "core"
    assert suggester._find_universe_for_module("ToolAdapterNode") == "tools"
    assert suggester._find_universe_for_module("ValidationNode") == "security"
    assert suggester._find_universe_for_module("ActiveLearningNode") == "learning"
    
    # Test with a module that doesn't exist in any universe
    assert suggester._find_universe_for_module("NonExistentModule") is None


def test_extract_domain_keywords(sample_agent_spec, sample_univers_catalog, sample_consistency_results, sample_suggestions):
    """
    Test _extract_domain_keywords method.
    """
    suggester = AgentYamlSuggester(
        sample_agent_spec,
        sample_univers_catalog,
        sample_consistency_results,
        sample_suggestions
    )
    
    # Test with various texts
    assert "conversational" in suggester._extract_domain_keywords(
        "For conversational agents, consider adding MemoryNode to maintain context"
    )
    
    assert "data" in suggester._extract_domain_keywords(
        "For data analysis tasks, consider adding AnalyticsNode"
    )
    
    assert "research" in suggester._extract_domain_keywords(
        "This agent seems to be focused on research and knowledge gathering"
    )
    
    # Test with text that doesn't contain any domain keywords
    assert suggester._extract_domain_keywords(
        "This is a generic suggestion with no domain specifics"
    ) == []


def test_suggest_yaml_changes(sample_agent_spec, sample_univers_catalog, sample_consistency_results, sample_suggestions):
    """
    Test suggest_yaml_changes method.
    """
    suggester = AgentYamlSuggester(
        sample_agent_spec,
        sample_univers_catalog,
        sample_consistency_results,
        sample_suggestions
    )
    
    changes = suggester.suggest_yaml_changes()
    
    # Check that the security universe is suggested to be added
    assert "security" in changes["add_universes"]
    
    # Check that no modules are suggested to be added as custom modules
    # since ValidationNode is in the security universe
    assert len(changes["add_modules"]) == 0
    
    # Check that no modules are suggested to be removed
    assert len(changes["remove_modules"]) == 0
    
    # Check that conversational is added as a tag
    assert "conversational" in changes["add_tags"]
    
    # Check that the description is updated with a security note
    assert changes["update_description"] is not None
    assert "SECURITY NOTE" in changes["update_description"]


def test_generate_yaml_diff(sample_agent_spec, sample_univers_catalog, sample_consistency_results, sample_suggestions):
    """
    Test generate_yaml_diff method.
    """
    suggester = AgentYamlSuggester(
        sample_agent_spec,
        sample_univers_catalog,
        sample_consistency_results,
        sample_suggestions
    )
    
    diff = suggester.generate_yaml_diff()
    
    # Check that the diff is a non-empty string
    assert isinstance(diff, str)
    assert diff != ""
    
    # Check that the diff contains the expected sections
    assert "# Add the following universes:" in diff
    assert "+ univers: security" in diff
    
    assert "# Add the following tags:" in diff
    assert "+ tag: conversational" in diff
    
    assert "# Update the description:" in diff
    assert "- description: A test agent for unit testing" in diff
    assert "+ description: A test agent for unit testing" in diff
    assert "SECURITY NOTE" in diff


def test_suggest_yaml_changes_with_unused_modules(sample_agent_spec, sample_univers_catalog, sample_consistency_results, sample_suggestions):
    """
    Test suggest_yaml_changes method with unused modules.
    """
    # Modify the consistency results to include unused modules
    sample_consistency_results["unused_modules"] = ["ToolAdapterNode"]
    
    suggester = AgentYamlSuggester(
        sample_agent_spec,
        sample_univers_catalog,
        sample_consistency_results,
        sample_suggestions
    )
    
    changes = suggester.suggest_yaml_changes()
    
    # Check that ToolAdapterNode is suggested to be removed
    assert "ToolAdapterNode" in changes["remove_modules"]


def test_suggest_yaml_changes_with_missing_custom_module(sample_agent_spec, sample_univers_catalog, sample_consistency_results, sample_suggestions):
    """
    Test suggest_yaml_changes method with a missing custom module.
    """
    # Modify the consistency results to include a missing custom module
    sample_consistency_results["missing_modules"] = ["ValidationNode", "CustomModule"]
    
    suggester = AgentYamlSuggester(
        sample_agent_spec,
        sample_univers_catalog,
        sample_consistency_results,
        sample_suggestions
    )
    
    changes = suggester.suggest_yaml_changes()
    
    # Check that security universe is suggested to be added
    assert "security" in changes["add_universes"]
    
    # Check that CustomModule is suggested to be added as a custom module
    assert "CustomModule" in changes["add_modules"]
