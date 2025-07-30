"""
Unit tests for the personas module.
"""

import unittest
from unittest.mock import MagicMock, patch

from num_agents.workflow.personas import (
    PersonaRegistry, architect_persona, planner_persona, 
    designer_persona, coder_persona, registry
)
from num_agents.workflow.task_chain import PersonaContext


class TestPersonaRegistry(unittest.TestCase):
    """Test cases for the PersonaRegistry class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.registry = PersonaRegistry()
    
    def test_register_and_get(self):
        """Test registering and getting a persona."""
        handler = MagicMock()
        self.registry.register("TestPersona", handler)
        
        # Check that the persona is registered
        self.assertIn("TestPersona", self.registry.personas)
        
        # Check that we can get the persona
        retrieved_handler = self.registry.get("TestPersona")
        self.assertEqual(retrieved_handler, handler)
    
    def test_get_nonexistent(self):
        """Test getting a nonexistent persona."""
        handler = self.registry.get("NonexistentPersona")
        self.assertIsNone(handler)
    
    def test_list_personas(self):
        """Test listing personas."""
        # Register some personas
        self.registry.register("Persona1", MagicMock())
        self.registry.register("Persona2", MagicMock())
        self.registry.register("Persona3", MagicMock())
        
        # Check that the list contains all personas
        personas = self.registry.list_personas()
        self.assertEqual(len(personas), 3)
        self.assertIn("Persona1", personas)
        self.assertIn("Persona2", personas)
        self.assertIn("Persona3", personas)


class TestPersonas(unittest.TestCase):
    """Test cases for the predefined personas."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.shared_store = MagicMock()
        self.event_bus = MagicMock()
        
        # Create a context for testing
        self.context = PersonaContext(
            step={
                "index": 0,
                "persona": "TestPersona",
                "description": "Test step",
                "prompt": {
                    "text": "Test prompt",
                    "requires": [],
                    "produces": [],
                    "internal_checks": []
                },
                "outputs": ["output.md"]
            },
            dependencies={},
            shared_store=self.shared_store,
            event_bus=self.event_bus
        )
    
    def test_architect_persona(self):
        """Test the architect persona."""
        result = architect_persona(self.context)
        
        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)
        
        # Check that the output file is in the result
        self.assertIn("output.md", result)
        
        # Check that the shared store was used
        self.shared_store.set.assert_called()
        
        # Check that the event bus was used
        self.event_bus.publish.assert_called()
    
    def test_planner_persona(self):
        """Test the planner persona."""
        # Add a dependency
        self.context.dependencies = {1: {"dep_output.md": "Dependency content"}}
        
        result = planner_persona(self.context)
        
        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)
        
        # Check that the output file is in the result
        self.assertIn("output.md", result)
        
        # Check that the shared store was used
        self.shared_store.set.assert_called()
        
        # Check that the event bus was used
        self.event_bus.publish.assert_called()
    
    def test_designer_persona(self):
        """Test the designer persona."""
        # Change the output to a design file
        self.context.step["outputs"] = ["design.tsx"]
        
        result = designer_persona(self.context)
        
        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)
        
        # Check that the output file is in the result
        self.assertIn("design.tsx", result)
        
        # Check that the shared store was used
        self.shared_store.set.assert_called()
        
        # Check that the event bus was used
        self.event_bus.publish.assert_called()
    
    def test_coder_persona(self):
        """Test the coder persona."""
        # Change the output to a code file
        self.context.step["outputs"] = ["code.py"]
        
        result = coder_persona(self.context)
        
        # Check that the result is a dictionary
        self.assertIsInstance(result, dict)
        
        # Check that the output file is in the result
        self.assertIn("code.py", result)
        
        # Check that the shared store was used
        self.shared_store.set.assert_called()
        
        # Check that the event bus was used
        self.event_bus.publish.assert_called()
    
    def test_global_registry(self):
        """Test the global persona registry."""
        # Check that the global registry has the default personas
        self.assertIn("Architect", registry.personas)
        self.assertIn("Planner", registry.personas)
        self.assertIn("Designer", registry.personas)
        self.assertIn("Coder", registry.personas)


if __name__ == "__main__":
    unittest.main()
