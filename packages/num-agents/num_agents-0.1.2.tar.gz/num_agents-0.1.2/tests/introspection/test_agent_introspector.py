"""
Tests for the AgentIntrospector class.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock

from num_agents.introspection.agent_introspector import AgentIntrospector


@pytest.fixture
def mock_agent_dir(tmp_path):
    """Create a mock agent directory with test files."""
    agent_dir = tmp_path / "test_agent"
    agent_dir.mkdir()
    
    # Create a mock agent.yaml file
    agent_yaml = """
name: TestAgent
description: A test agent
universes:
  - core
  - llm
modules:
  - InputNode
  - ProcessingNode
  - OutputNode
protocol: simple
llm:
  provider: openai
  model: gpt-4
memory:
  type: simple
"""
    with open(agent_dir / "agent.yaml", "w") as f:
        f.write(agent_yaml)
    
    # Create a mock logical_graph.mmd file
    logical_graph = """
flowchart TD
    InputNode --> ProcessingNode
    ProcessingNode --> OutputNode
"""
    with open(agent_dir / "logical_graph.mmd", "w") as f:
        f.write(logical_graph)
    
    # Create a mock audit_report.json file
    audit_report = {
        "validation": {
            "agent_name": "TestAgent",
            "status": "healthy",
            "health_score": 85,
            "completeness": 1.0,
            "issues": [],
            "suggestions": {
                "critical": [],
                "high": [],
                "medium": [
                    {
                        "text": "Consider adding logging to InputNode"
                    }
                ],
                "low": [
                    {
                        "text": "Consider adding documentation to ProcessingNode"
                    }
                ]
            },
            "nodes": {
                "InputNode": {
                    "status": "healthy",
                    "issues": [],
                    "suggestions": [
                        {
                            "text": "Consider adding logging to InputNode"
                        }
                    ]
                },
                "ProcessingNode": {
                    "status": "healthy",
                    "issues": [],
                    "suggestions": [
                        {
                            "text": "Consider adding documentation to ProcessingNode"
                        }
                    ]
                },
                "OutputNode": {
                    "status": "healthy",
                    "issues": [],
                    "suggestions": []
                }
            }
        }
    }
    with open(agent_dir / "audit_report.json", "w") as f:
        json.dump(audit_report, f)
    
    return str(agent_dir)


@pytest.fixture
def mock_unhealthy_agent_dir(tmp_path):
    """Create a mock unhealthy agent directory with test files."""
    agent_dir = tmp_path / "unhealthy_agent"
    agent_dir.mkdir()
    
    # Create a mock agent.yaml file
    agent_yaml = """
name: UnhealthyAgent
description: An unhealthy test agent
universes:
  - core
  - llm
modules:
  - InputNode
  - ProcessingNode
  # OutputNode is missing
protocol: simple
llm:
  provider: openai
  model: gpt-4
memory:
  type: simple
"""
    with open(agent_dir / "agent.yaml", "w") as f:
        f.write(agent_yaml)
    
    # Create a mock logical_graph.mmd file
    logical_graph = """
flowchart TD
    InputNode --> ProcessingNode
    ProcessingNode --> End
"""
    with open(agent_dir / "logical_graph.mmd", "w") as f:
        f.write(logical_graph)
    
    # Create a mock audit_report.json file
    audit_report = {
        "validation": {
            "agent_name": "UnhealthyAgent",
            "status": "warning",
            "health_score": 65,
            "completeness": 0.67,
            "issues": [
                {
                    "type": "missing_module",
                    "severity": "critical",
                    "description": "Missing module: OutputNode is declared in the universe catalog but not used in the agent"
                }
            ],
            "suggestions": {
                "critical": [
                    {
                        "text": "Add OutputNode to the agent to handle output formatting"
                    }
                ],
                "high": [
                    {
                        "text": "Add input validation to InputNode to improve security"
                    }
                ],
                "medium": [],
                "low": []
            },
            "nodes": {
                "InputNode": {
                    "status": "warning",
                    "issues": [
                        {
                            "type": "security",
                            "severity": "high",
                            "description": "InputNode does not validate user input"
                        }
                    ],
                    "suggestions": [
                        {
                            "text": "Add input validation to InputNode"
                        }
                    ]
                },
                "ProcessingNode": {
                    "status": "healthy",
                    "issues": [],
                    "suggestions": []
                }
            }
        }
    }
    with open(agent_dir / "audit_report.json", "w") as f:
        json.dump(audit_report, f)
    
    return str(agent_dir)


def test_init(mock_agent_dir):
    """Test initialization of AgentIntrospector."""
    introspector = AgentIntrospector(mock_agent_dir)
    
    assert introspector.agent_dir == mock_agent_dir
    assert introspector.agent_spec_path == os.path.join(mock_agent_dir, "agent.yaml")
    assert introspector.logical_graph_path == os.path.join(mock_agent_dir, "logical_graph.mmd")
    assert introspector.audit_report_path == os.path.join(mock_agent_dir, "audit_report.json")


def test_get_logical_graph(mock_agent_dir):
    """Test getting the logical graph."""
    introspector = AgentIntrospector(mock_agent_dir)
    
    # Get the logical graph
    logical_graph = introspector.get_logical_graph()
    
    # Check that the logical graph is correct
    assert "flowchart TD" in logical_graph
    assert "InputNode --> ProcessingNode" in logical_graph
    assert "ProcessingNode --> OutputNode" in logical_graph


def test_get_audit_report(mock_agent_dir):
    """Test getting the audit report."""
    introspector = AgentIntrospector(mock_agent_dir)
    
    # Get the audit report
    report = introspector.get_audit_report()
    
    # Check that the report is correct
    assert report["validation"]["agent_name"] == "TestAgent"
    assert report["validation"]["status"] == "healthy"
    assert report["validation"]["health_score"] == 85
    assert report["validation"]["completeness"] == 1.0
    assert len(report["validation"]["issues"]) == 0
    assert len(report["validation"]["suggestions"]["critical"]) == 0
    assert len(report["validation"]["suggestions"]["high"]) == 0
    assert len(report["validation"]["suggestions"]["medium"]) == 1
    assert len(report["validation"]["suggestions"]["low"]) == 1


def test_get_health_status(mock_agent_dir):
    """Test getting the health status."""
    introspector = AgentIntrospector(mock_agent_dir)
    
    # Get the health status
    health_status = introspector.get_health_status()
    
    # Check that the health status is correct
    assert health_status["agent_name"] == "TestAgent"
    assert health_status["status"] == "healthy"
    assert health_status["health_score"] == 85
    assert health_status["completeness"] == 1.0
    assert health_status["issue_count"] == 0
    assert health_status["critical_suggestion_count"] == 0
    assert health_status["high_suggestion_count"] == 0
    assert health_status["medium_suggestion_count"] == 1
    assert health_status["low_suggestion_count"] == 1


def test_get_critical_issues(mock_unhealthy_agent_dir):
    """Test getting critical issues."""
    introspector = AgentIntrospector(mock_unhealthy_agent_dir)
    
    # Get critical issues
    critical_issues = introspector.get_critical_issues()
    
    # Check that the critical issues are correct
    assert len(critical_issues) == 1
    assert critical_issues[0]["type"] == "missing_module"
    assert critical_issues[0]["severity"] == "critical"
    assert "OutputNode" in critical_issues[0]["description"]


def test_get_critical_suggestions(mock_unhealthy_agent_dir):
    """Test getting critical suggestions."""
    introspector = AgentIntrospector(mock_unhealthy_agent_dir)
    
    # Get critical suggestions
    critical_suggestions = introspector.get_critical_suggestions()
    
    # Check that the critical suggestions are correct
    assert len(critical_suggestions) == 1
    assert "OutputNode" in critical_suggestions[0]["text"]


def test_get_node_metadata(mock_agent_dir):
    """Test getting node metadata."""
    introspector = AgentIntrospector(mock_agent_dir)
    
    # Get node metadata
    node_metadata = introspector.get_node_metadata("InputNode")
    
    # Check that the node metadata is correct
    assert node_metadata["status"] == "healthy"
    assert len(node_metadata["issues"]) == 0
    assert len(node_metadata["suggestions"]) == 1
    assert "logging" in node_metadata["suggestions"][0]["text"]


def test_should_adapt(mock_agent_dir, mock_unhealthy_agent_dir):
    """Test determining if adaptation is needed."""
    # Test with a healthy agent
    healthy_introspector = AgentIntrospector(mock_agent_dir)
    assert not healthy_introspector.should_adapt()  # Default threshold is 70.0
    assert healthy_introspector.should_adapt(90.0)  # Higher threshold
    
    # Test with an unhealthy agent
    unhealthy_introspector = AgentIntrospector(mock_unhealthy_agent_dir)
    assert unhealthy_introspector.should_adapt()  # Default threshold is 70.0
    assert not unhealthy_introspector.should_adapt(60.0)  # Lower threshold


def test_get_adaptation_recommendations(mock_unhealthy_agent_dir):
    """Test getting adaptation recommendations."""
    introspector = AgentIntrospector(mock_unhealthy_agent_dir)
    
    # Get adaptation recommendations
    recommendations = introspector.get_adaptation_recommendations()
    
    # Check that the recommendations are correct
    assert len(recommendations) > 0
    
    # Check that critical issues are included
    critical_issues_included = False
    for recommendation in recommendations:
        if recommendation.get("type") == "issue" and recommendation.get("severity") == "critical":
            critical_issues_included = True
            break
    assert critical_issues_included
    
    # Check that critical suggestions are included
    critical_suggestions_included = False
    for recommendation in recommendations:
        if recommendation.get("type") == "suggestion" and recommendation.get("severity") == "critical":
            critical_suggestions_included = True
            break
    assert critical_suggestions_included


@patch("num_agents.orchestrator.meta_orchestrator.MetaOrchestrator")
def test_refresh(mock_meta_orchestrator, mock_agent_dir):
    """Test refreshing the introspector data."""
    # Create a mock MetaOrchestrator instance
    mock_instance = MagicMock()
    mock_meta_orchestrator.return_value = mock_instance
    
    # Create a mock analyze result
    mock_result = {
        "validation": {
            "agent_name": "TestAgent",
            "status": "healthy",
            "health_score": 90,  # Changed from 85
            "completeness": 1.0,
            "issues": [],
            "suggestions": {"critical": [], "high": [], "medium": [], "low": []}
        }
    }
    mock_instance.analyze.return_value = mock_result
    
    # Create an introspector
    introspector = AgentIntrospector(mock_agent_dir)
    
    # Get the health status with refresh
    health_status = introspector.get_health_status(refresh=True)
    
    # Check that the meta orchestrator was called
    mock_instance.analyze.assert_called_once()
    
    # Check that the health status reflects the refreshed data
    assert health_status["health_score"] == 90
