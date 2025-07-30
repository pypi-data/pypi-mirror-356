"""
Unit tests for the task chain module.
"""

import os
import json
import yaml
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from num_agents.workflow.task_chain import (
    TaskPrompt, TaskStep, TaskChain, PersonaContext, WorkflowEngine
)


class TestTaskPrompt(unittest.TestCase):
    """Test cases for the TaskPrompt class."""
    
    def test_task_prompt_creation(self):
        """Test creating a TaskPrompt."""
        prompt = TaskPrompt(
            text="Test prompt",
            requires=["input.txt"],
            produces=["output.txt"],
            internal_checks=["Check 1", "Check 2"]
        )
        
        self.assertEqual(prompt.text, "Test prompt")
        self.assertEqual(prompt.requires, ["input.txt"])
        self.assertEqual(prompt.produces, ["output.txt"])
        self.assertEqual(prompt.internal_checks, ["Check 1", "Check 2"])
    
    def test_task_prompt_defaults(self):
        """Test TaskPrompt default values."""
        prompt = TaskPrompt(text="Test prompt")
        
        self.assertEqual(prompt.text, "Test prompt")
        self.assertEqual(prompt.requires, [])
        self.assertEqual(prompt.produces, [])
        self.assertEqual(prompt.internal_checks, [])


class TestTaskStep(unittest.TestCase):
    """Test cases for the TaskStep class."""
    
    def test_task_step_creation(self):
        """Test creating a TaskStep."""
        prompt = TaskPrompt(text="Test prompt")
        step = TaskStep(
            index=1,
            persona="Tester",
            depends_on=[0],
            description="Test step",
            prompt=prompt,
            outputs=["output.txt"]
        )
        
        self.assertEqual(step.index, 1)
        self.assertEqual(step.persona, "Tester")
        self.assertEqual(step.depends_on, [0])
        self.assertEqual(step.description, "Test step")
        self.assertEqual(step.prompt, prompt)
        self.assertEqual(step.outputs, ["output.txt"])
    
    def test_task_step_defaults(self):
        """Test TaskStep default values."""
        prompt = TaskPrompt(text="Test prompt")
        step = TaskStep(
            index=1,
            persona="Tester",
            description="Test step",
            prompt=prompt
        )
        
        self.assertEqual(step.depends_on, [])
        self.assertEqual(step.outputs, [])
    
    def test_validate_dependencies(self):
        """Test dependency validation."""
        prompt = TaskPrompt(text="Test prompt")
        
        # Valid dependencies
        step = TaskStep(
            index=2,
            persona="Tester",
            depends_on=[0, 1],
            description="Test step",
            prompt=prompt
        )
        self.assertEqual(step.depends_on, [0, 1])
        
        # Invalid dependencies
        with self.assertRaises(ValueError):
            TaskStep(
                index=2,
                persona="Tester",
                depends_on=[0, 2, 3],
                description="Test step",
                prompt=prompt
            )


class TestTaskChain(unittest.TestCase):
    """Test cases for the TaskChain class."""
    
    def test_task_chain_creation(self):
        """Test creating a TaskChain."""
        prompt1 = TaskPrompt(text="Prompt 1")
        prompt2 = TaskPrompt(text="Prompt 2")
        
        step1 = TaskStep(
            index=0,
            persona="Tester1",
            description="Step 1",
            prompt=prompt1
        )
        
        step2 = TaskStep(
            index=1,
            persona="Tester2",
            depends_on=[0],
            description="Step 2",
            prompt=prompt2
        )
        
        chain = TaskChain(
            steps=[step1, step2],
            reflect="Test reflection",
            err=["Error 1"],
            note=["Note 1"],
            warn=["Warning 1"]
        )
        
        self.assertEqual(len(chain.steps), 2)
        self.assertEqual(chain.reflect, "Test reflection")
        self.assertEqual(chain.err, ["Error 1"])
        self.assertEqual(chain.note, ["Note 1"])
        self.assertEqual(chain.warn, ["Warning 1"])
    
    def test_task_chain_defaults(self):
        """Test TaskChain default values."""
        prompt = TaskPrompt(text="Prompt")
        step = TaskStep(
            index=0,
            persona="Tester",
            description="Step",
            prompt=prompt
        )
        
        chain = TaskChain(steps=[step])
        
        self.assertEqual(chain.reflect, None)
        self.assertEqual(chain.err, [])
        self.assertEqual(chain.note, [])
        self.assertEqual(chain.warn, [])
    
    def test_validate_steps(self):
        """Test step validation."""
        prompt = TaskPrompt(text="Prompt")
        
        # Valid steps
        step1 = TaskStep(index=0, persona="Tester1", description="Step 1", prompt=prompt)
        step2 = TaskStep(index=1, persona="Tester2", description="Step 2", prompt=prompt)
        
        chain = TaskChain(steps=[step1, step2])
        self.assertEqual(len(chain.steps), 2)
        
        # Invalid steps (duplicate indices)
        step3 = TaskStep(index=0, persona="Tester3", description="Step 3", prompt=prompt)
        
        with self.assertRaises(ValueError):
            TaskChain(steps=[step1, step2, step3])


class TestWorkflowEngine(unittest.TestCase):
    """Test cases for the WorkflowEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.event_bus = MagicMock()
        self.shared_store = MagicMock()
        self.engine = WorkflowEngine(event_bus=self.event_bus, shared_store=self.shared_store)
        
        # Create a sample chain
        prompt1 = TaskPrompt(text="Prompt 1")
        prompt2 = TaskPrompt(text="Prompt 2", requires=["output1.txt"])
        
        self.step1 = TaskStep(
            index=0,
            persona="Tester1",
            description="Step 1",
            prompt=prompt1,
            outputs=["output1.txt"]
        )
        
        self.step2 = TaskStep(
            index=1,
            persona="Tester2",
            depends_on=[0],
            description="Step 2",
            prompt=prompt2,
            outputs=["output2.txt"]
        )
        
        self.chain = TaskChain(steps=[self.step1, self.step2])
        
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Clean up after tests."""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_register_persona(self):
        """Test registering a persona."""
        handler = MagicMock()
        self.engine.register_persona("TestPersona", handler)
        
        self.assertIn("TestPersona", self.engine.personas)
        self.assertEqual(self.engine.personas["TestPersona"], handler)
    
    def test_load_and_save_chain(self):
        """Test loading and saving a task chain."""
        # Save the chain to a file
        chain_file = os.path.join(self.temp_dir, "test_chain.yaml")
        self.engine.save_chain(self.chain, chain_file)
        
        # Load the chain from the file
        loaded_chain = self.engine.load_chain(chain_file)
        
        # Check that the loaded chain matches the original
        self.assertEqual(len(loaded_chain.steps), len(self.chain.steps))
        self.assertEqual(loaded_chain.steps[0].index, self.chain.steps[0].index)
        self.assertEqual(loaded_chain.steps[0].persona, self.chain.steps[0].persona)
        self.assertEqual(loaded_chain.steps[0].description, self.chain.steps[0].description)
        self.assertEqual(loaded_chain.steps[1].depends_on, self.chain.steps[1].depends_on)
    
    def test_sort_steps_by_dependencies(self):
        """Test sorting steps by dependencies."""
        # Create steps with dependencies
        prompt = TaskPrompt(text="Prompt")
        
        step1 = TaskStep(index=0, persona="Tester1", description="Step 1", prompt=prompt)
        step2 = TaskStep(index=1, persona="Tester2", depends_on=[0], description="Step 2", prompt=prompt)
        step3 = TaskStep(index=2, persona="Tester3", depends_on=[1], description="Step 3", prompt=prompt)
        
        # Shuffle the steps
        steps = [step3, step1, step2]
        
        # Sort the steps
        sorted_steps = self.engine._sort_steps_by_dependencies(steps)
        
        # Check that the steps are sorted correctly
        self.assertEqual(sorted_steps[0].index, 0)
        self.assertEqual(sorted_steps[1].index, 1)
        self.assertEqual(sorted_steps[2].index, 2)
    
    def test_sort_steps_circular_dependency(self):
        """Test sorting steps with circular dependencies."""
        # Create steps with circular dependencies
        prompt = TaskPrompt(text="Prompt")
        
        step1 = TaskStep(index=0, persona="Tester1", depends_on=[2], description="Step 1", prompt=prompt)
        step2 = TaskStep(index=1, persona="Tester2", depends_on=[0], description="Step 2", prompt=prompt)
        step3 = TaskStep(index=2, persona="Tester3", depends_on=[1], description="Step 3", prompt=prompt)
        
        # Try to sort the steps
        with self.assertRaises(ValueError):
            self.engine._sort_steps_by_dependencies([step1, step2, step3])
    
    def test_execute_chain(self):
        """Test executing a task chain."""
        # Register persona handlers
        handler1 = MagicMock(return_value={"output1.txt": "Result 1"})
        handler2 = MagicMock(return_value={"output2.txt": "Result 2"})
        
        self.engine.register_persona("Tester1", handler1)
        self.engine.register_persona("Tester2", handler2)
        
        # Execute the chain
        results = self.engine.execute_chain(self.chain)
        
        # Check that the handlers were called
        handler1.assert_called_once()
        handler2.assert_called_once()
        
        # Check that the results were stored
        self.assertIn(0, results)
        self.assertIn(1, results)
        self.assertEqual(results[0], {"output1.txt": "Result 1"})
        self.assertEqual(results[1], {"output2.txt": "Result 2"})
        
        # Check that the event bus was used
        self.event_bus.publish.assert_called()
    
    def test_execute_chain_missing_persona(self):
        """Test executing a chain with a missing persona."""
        # Register only one persona
        handler1 = MagicMock(return_value={"output1.txt": "Result 1"})
        self.engine.register_persona("Tester1", handler1)
        
        # Try to execute the chain
        with self.assertRaises(ValueError):
            self.engine.execute_chain(self.chain)
    
    def test_execute_chain_handler_error(self):
        """Test executing a chain with a handler that raises an error."""
        # Register persona handlers
        handler1 = MagicMock(side_effect=Exception("Test error"))
        handler2 = MagicMock(return_value={"output2.txt": "Result 2"})
        
        self.engine.register_persona("Tester1", handler1)
        self.engine.register_persona("Tester2", handler2)
        
        # Try to execute the chain
        with self.assertRaises(ValueError):
            self.engine.execute_chain(self.chain)
        
        # Check that the event bus was used to publish an error event
        self.event_bus.publish.assert_called()


if __name__ == "__main__":
    unittest.main()
