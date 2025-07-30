import unittest
from unittest.mock import MagicMock, patch

from num_agents.core import SharedStore
from num_agents.reasoning.models import Proposition
from num_agents.reasoning.semantic_models import Expertise, ExpertiseDomain
from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.nodes.expertise_weighting_node import ExpertiseWeightingNode

class TestExpertiseWeightingNode(unittest.TestCase):
    def setUp(self):
        # Mock LLM Provider
        self.mock_llm_provider = MagicMock()
        
        # Patch the factory
        self.patcher = patch(
            "num_agents.reasoning.llm.LLMProviderFactory.create_provider",
            return_value=self.mock_llm_provider,
        )
        self.mock_create_provider = self.patcher.start()
        
        # Shared Store and Logic Engine
        self.shared_store = SharedStore()
        self.logic_engine = LogicEngine()
        self.context = self.logic_engine.create_context("test_context", "Test context for expertise weighting node")
        self.context_id = self.context.id
        
        # Expertise
        self.expertise = Expertise(
            domains=[
                ExpertiseDomain(name="Physics", proficiency=0.9),
                ExpertiseDomain(name="Biology", proficiency=0.3),
            ]
        )
        
        # Populate Shared Store
        self.shared_store.set("logic_engine", self.logic_engine)
        self.shared_store.set("expertise", self.expertise)
        self.shared_store.set("current_context_id", self.context_id)
        
        # Node instance
        self.node = ExpertiseWeightingNode(
            name="TestExpertiseNode",
            llm_provider="mock_provider",
            llm_model="mock_model",
        )

    def tearDown(self):
        self.patcher.stop()

    def test_initialization(self):
        self.mock_create_provider.assert_called_once_with(
            provider_name="mock_provider",
            model="mock_model",
            api_key=None,
            temperature=0.1,
            max_tokens=1000,
        )
        self.assertIsNotNone(self.node.llm_provider)

    def test_run_with_no_propositions(self):
        self.node._run(self.shared_store)
        self.mock_llm_provider.generate_json.assert_not_called()

    def test_process_proposition_full_flow(self):
        # Add a proposition
        prop = self.logic_engine.add_proposition(
            self.context_id, "Photosynthesis converts sunlight into energy", "statement", confidence=0.8
        )
        
        # Mock LLM responses
        self.mock_llm_provider.generate_json.side_effect = [
            {"Physics": 0.95, "Biology": 0.05},
            {"confidence_factor": 1.2},
        ]
        
        # Mock logic engine methods
        self.logic_engine.update_proposition_confidence = MagicMock()
        
        # Run the node
        self.node._run(self.shared_store)
        
        # Verify domain relevance call
        self.mock_llm_provider.generate_json.assert_any_call(
            self.node._get_domain_relevance_prompt(
                prop.text, ["Physics", "Biology"]
            )
        )
        
        # Verify confidence adjustment call
        self.mock_llm_provider.generate_json.assert_any_call(
            self.node._get_confidence_adjustment_prompt(
                prop.text, {"Physics": 0.95}, self.expertise
            )
        )
        
        # Verify confidence update
        expected_new_confidence = 0.8 * 1.2
        self.logic_engine.update_proposition_confidence.assert_called_once_with(
            prop.id, expected_new_confidence
        )

    def test_run_with_existing_domain_relevance(self):
        # Add proposition with existing domain relevance
        prop = self.logic_engine.add_proposition(
            self.context_id, "Mitochondria is the powerhouse of the cell", "statement"
        )
        prop.domain_relevance = {"Biology": 0.98}  # Direct dictionary assignment
        
        # Mock LLM response
        self.mock_llm_provider.generate_json.return_value = {"confidence_factor": 0.8}
        self.logic_engine.update_proposition_confidence = MagicMock()
        
        # Run the node
        self.node._run(self.shared_store)
        
        # Verify only one call (confidence adjustment)
        self.assertEqual(self.mock_llm_provider.generate_json.call_count, 1)
        self.logic_engine.update_proposition_confidence.assert_called_once()

    def test_run_handles_missing_shared_store_items(self):
        empty_store = SharedStore()
        result_store = self.node._run(empty_store)
        self.assertIs(result_store, empty_store)
        self.mock_llm_provider.generate_json.assert_not_called()

if __name__ == "__main__":
    unittest.main()
