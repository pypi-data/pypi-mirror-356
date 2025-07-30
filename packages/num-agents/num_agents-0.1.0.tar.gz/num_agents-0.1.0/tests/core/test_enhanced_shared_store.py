"""
Tests for the enhanced SharedStore with working memory integration.
"""

import unittest
from unittest.mock import patch, MagicMock

from num_agents.core import SharedStore


class TestEnhancedSharedStore(unittest.TestCase):
    """Test cases for the enhanced SharedStore with working memory support."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_agent_spec = {
            "agent": {
                "name": "TestAgent",
                "working_memory": {
                    "goals": ["Goal 1", "Goal 2"],
                    "context": {
                        "domain": "test domain",
                        "project_type": "test project"
                    },
                    "constraints": ["Constraint 1"],
                    "preferences": {
                        "style": "test style"
                    }
                }
            }
        }

    def test_init_with_agent_spec(self):
        """Test initializing SharedStore with agent specification."""
        store = SharedStore(self.mock_agent_spec)
        
        # Test that working memory was properly initialized
        self.assertIn("working_memory", store)
        self.assertIn("goals", store)
        self.assertIn("context", store)
        self.assertIn("constraints", store)
        self.assertIn("preferences", store)
        
        # Test working memory specific methods
        working_memory = store.get_working_memory()
        self.assertIsInstance(working_memory, dict)
        self.assertIn("goals", working_memory)
        
        goals = store.get_goals()
        self.assertEqual(len(goals), 2)
        self.assertEqual(goals[0], "Goal 1")
        
        context = store.get_context()
        self.assertEqual(context["domain"], "test domain")
        self.assertEqual(context["project_type"], "test project")
        
        constraints = store.get_constraints()
        self.assertEqual(len(constraints), 1)
        self.assertEqual(constraints[0], "Constraint 1")
        
        preferences = store.get_preferences()
        self.assertEqual(preferences["style"], "test style")

    def test_update_working_memory(self):
        """Test updating working memory."""
        store = SharedStore(self.mock_agent_spec)
        
        # Initial state
        self.assertEqual(store.get_goals()[0], "Goal 1")
        
        # Update working memory
        store.update_working_memory({
            "goals": ["New Goal 1", "New Goal 2"],
            "context": {
                "domain": "new domain",
                "additional_info": "new info"
            }
        })
        
        # Check that working memory was updated
        self.assertEqual(store.get_goals()[0], "New Goal 1")
        self.assertEqual(len(store.get_goals()), 2)
        
        # Check that context was merged, not replaced
        context = store.get_context()
        self.assertEqual(context["domain"], "new domain")
        self.assertEqual(context["project_type"], "test project")
        self.assertEqual(context["additional_info"], "new info")
        
        # Check that constraints and preferences were not affected
        self.assertEqual(store.get_constraints()[0], "Constraint 1")
        self.assertEqual(store.get_preferences()["style"], "test style")


if __name__ == "__main__":
    unittest.main()
