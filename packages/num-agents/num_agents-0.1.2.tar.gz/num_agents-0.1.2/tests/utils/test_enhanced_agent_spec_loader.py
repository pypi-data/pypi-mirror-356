"""
Tests for the enhanced AgentSpecLoader with working memory, expertise, and semantic entities.
"""

import os
import unittest
from unittest.mock import patch, mock_open

from num_agents.utils.file_io import AgentSpecLoader


class TestEnhancedAgentSpecLoader(unittest.TestCase):
    """Test cases for the enhanced AgentSpecLoader."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_yaml_content = """
agent:
  name: "TestAgent"
  description: "A test agent"
  univers:
    - TestUniverse
  protocol: N2A
  llm: gpt-4o
  
  working_memory:
    goals:
      - "Goal 1"
      - "Goal 2"
    context:
      domain: "test domain"
      project_type: "test project"
    constraints:
      - "Constraint 1"
    preferences:
      style: "test style"
  
  expertise:
    domains:
      - name: "domain1"
        proficiency: 0.9
    skills:
      - name: "skill1"
        proficiency: 0.8
    knowledge_bases:
      - name: "kb1"
        source: "internal"
  
  semantic_entities:
    - name: "Entity1"
      properties:
        - name: "prop1"
          type: "string"
      relations:
        - name: "relates_to"
          target: "Entity2"
"""

    @patch("num_agents.utils.file_io.read_yaml")
    def test_load_enhanced_spec(self, mock_read_yaml):
        """Test loading an enhanced agent specification."""
        # Mock the read_yaml function to return our test YAML content
        import yaml
        mock_read_yaml.return_value = yaml.safe_load(self.mock_yaml_content)
        
        # Create an AgentSpecLoader instance
        loader = AgentSpecLoader("dummy_path.yaml")
        spec = loader.load()
        
        # Basic assertions
        self.assertEqual(loader.get_agent_name(), "TestAgent")
        self.assertEqual(loader.get_agent_description(), "A test agent")
        
        # Test working memory methods
        working_memory = loader.get_working_memory()
        self.assertIsInstance(working_memory, dict)
        self.assertIn("goals", working_memory)
        
        goals = loader.get_goals()
        self.assertEqual(len(goals), 2)
        self.assertEqual(goals[0], "Goal 1")
        
        context = loader.get_context()
        self.assertEqual(context["domain"], "test domain")
        self.assertEqual(context["project_type"], "test project")
        
        constraints = loader.get_constraints()
        self.assertEqual(len(constraints), 1)
        self.assertEqual(constraints[0], "Constraint 1")
        
        preferences = loader.get_preferences()
        self.assertEqual(preferences["style"], "test style")
        
        # Test expertise methods
        expertise = loader.get_expertise()
        self.assertIsInstance(expertise, dict)
        
        domains = loader.get_domains()
        self.assertEqual(len(domains), 1)
        self.assertEqual(domains[0]["name"], "domain1")
        self.assertEqual(domains[0]["proficiency"], 0.9)
        
        skills = loader.get_skills()
        self.assertEqual(len(skills), 1)
        self.assertEqual(skills[0]["name"], "skill1")
        
        knowledge_bases = loader.get_knowledge_bases()
        self.assertEqual(len(knowledge_bases), 1)
        self.assertEqual(knowledge_bases[0]["name"], "kb1")
        
        # Test semantic entities
        semantic_entities = loader.get_semantic_entities()
        self.assertEqual(len(semantic_entities), 1)
        self.assertEqual(semantic_entities[0]["name"], "Entity1")
        self.assertEqual(len(semantic_entities[0]["properties"]), 1)
        self.assertEqual(semantic_entities[0]["properties"][0]["name"], "prop1")


if __name__ == "__main__":
    unittest.main()
