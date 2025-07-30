import unittest
from typing import Dict, List, Any
import logging

from num_agents.reasoning.nodes.model_router_node import (
    ModelRouterNode,
    InputType,
    OutputType,
    TaskType,
    OptimizationPriority
)

# Configure logging
logging.basicConfig(level=logging.INFO)


class TestModelRouterNode(unittest.TestCase):
    """Tests for the ModelRouterNode class."""

    def setUp(self):
        """Set up test fixtures."""
        # Define API keys for testing
        self.api_keys = {
            "openai": "test_openai_key",
            "gemini": "test_gemini_key"
        }

    def test_initialization(self):
        """Test that the ModelRouterNode initializes correctly."""
        node = ModelRouterNode(
            name="test_router",
            providers=["openai", "gemini"],
            optimization_priority=OptimizationPriority.BALANCED,
            api_keys=self.api_keys
        )
        
        self.assertEqual(node.name, "test_router")
        self.assertEqual(node.providers, ["openai", "gemini"])
        self.assertEqual(node.optimization_priority, OptimizationPriority.BALANCED)
        self.assertEqual(node.api_keys, self.api_keys)
        self.assertIsNotNone(node.model_registry)

    def test_detect_input_types(self):
        """Test input type detection."""
        node = ModelRouterNode(name="test_router", providers=["openai", "gemini"])
        
        # Test text detection
        input_data = {"text": "Hello world"}
        detected = node._detect_input_types(input_data)
        self.assertEqual(detected, [InputType.TEXT])
        
        # Test image detection
        input_data = {"image_url": "http://example.com/image.jpg"}
        detected = node._detect_input_types(input_data)
        self.assertEqual(detected, [InputType.IMAGE])
        
        # Test multiple types detection
        input_data = {"text": "Describe this image", "image": "base64_encoded_image"}
        detected = node._detect_input_types(input_data)
        self.assertIn(InputType.TEXT, detected)
        self.assertIn(InputType.IMAGE, detected)
        
        # Test default to text when empty
        input_data = {}
        detected = node._detect_input_types(input_data)
        self.assertEqual(detected, [InputType.TEXT])

    def test_model_selection_text_only(self):
        """Test model selection for text-only input."""
        node = ModelRouterNode(
            name="test_router",
            providers=["openai", "gemini"],
            optimization_priority=OptimizationPriority.QUALITY
        )
        
        provider, model = node.select_optimal_model(
            input_types=[InputType.TEXT],
            output_type=OutputType.TEXT,
            task_type=TaskType.REASONING
        )
        
        # For quality optimization with text input and reasoning task,
        # we expect a high-quality model
        self.assertIn(provider, ["openai", "gemini"])
        if provider == "openai":
            self.assertEqual(model, "gpt-4o")
        elif provider == "gemini":
            self.assertIn(model, ["gemini-2.5-pro", "gemini-1.5-pro"])

    def test_model_selection_multimodal(self):
        """Test model selection for multimodal input."""
        node = ModelRouterNode(
            name="test_router",
            providers=["openai", "gemini"],
            optimization_priority=OptimizationPriority.BALANCED
        )
        
        provider, model = node.select_optimal_model(
            input_types=[InputType.TEXT, InputType.IMAGE],
            output_type=OutputType.TEXT,
            task_type=TaskType.MULTIMODAL
        )
        
        # For multimodal input, we expect a model that supports images
        self.assertIn(provider, ["openai", "gemini"])
        if provider == "openai":
            self.assertIn(model, ["gpt-4o", "gpt-4o-mini"])
        elif provider == "gemini":
            self.assertIn("gemini", model)  # All Gemini models support images

    def test_model_selection_cost_optimization(self):
        """Test model selection with cost optimization."""
        node = ModelRouterNode(
            name="test_router",
            providers=["openai", "gemini"],
            optimization_priority=OptimizationPriority.COST
        )
        
        provider, model = node.select_optimal_model(
            input_types=[InputType.TEXT],
            output_type=OutputType.TEXT,
            task_type=TaskType.GENERAL
        )
        
        # For cost optimization with text input, we expect a cheaper model
        self.assertIn(provider, ["openai", "gemini"])
        if provider == "openai":
            self.assertEqual(model, "gpt-3.5-turbo")
        elif provider == "gemini":
            self.assertIn(model, ["gemini-2.5-flash-lite-preview", "gemini-1.5-flash"])

    def test_model_selection_with_constraints(self):
        """Test model selection with specific constraints."""
        node = ModelRouterNode(
            name="test_router",
            providers=["openai", "gemini"],
            optimization_priority=OptimizationPriority.BALANCED
        )
        
        constraints = {"min_quality": "medium", "max_cost": "medium"}
        provider, model = node.select_optimal_model(
            input_types=[InputType.TEXT],
            output_type=OutputType.TEXT,
            task_type=TaskType.GENERAL,
            constraints=constraints
        )
        
        # With these constraints, we expect a medium-tier model
        self.assertIn(provider, ["openai", "gemini"])

    def test_run_method(self):
        """Test the _run method with a shared store."""
        node = ModelRouterNode(
            name="test_router",
            providers=["openai", "gemini"],
            optimization_priority=OptimizationPriority.BALANCED,
            api_keys=self.api_keys
        )
        
        # Create a sample shared store
        shared_store = {
            "input_data": {"text": "What is machine learning?"},
            "task_type": TaskType.GENERAL,
            "expected_output_type": OutputType.TEXT
        }
        
        # Run the node
        result = node._run(shared_store)
        
        # Check that the shared store was updated with model selection
        self.assertIn("selected_llm_provider", result)
        self.assertIn("selected_llm_model", result)
        self.assertIn("llm_api_key", result)
        
        # Verify the API key was set correctly
        provider = result["selected_llm_provider"]
        self.assertEqual(result["llm_api_key"], self.api_keys.get(provider))


if __name__ == "__main__":
    unittest.main()
