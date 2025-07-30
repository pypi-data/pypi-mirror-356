"""
Unit tests for advanced features of the LogicEngine.
"""

import unittest
import logging
from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.models import PropositionType, PropositionStatus


class TestAdvancedLogicEngine(unittest.TestCase):
    """Test suite for advanced LogicEngine functionalities."""

    def setUp(self):
        """Set up the test case."""
        self.engine = LogicEngine()
        self.context = self.engine.create_context(
            name="Advanced Test Context",
            description="Context for testing advanced features"
        )
        logging.basicConfig(level=logging.INFO)

    def test_modus_ponens_inference(self):
        """Test the Modus Ponens inference rule."""
        # Add premise: If it is raining, then the ground is wet.
        premise_a = self.engine.add_proposition(
            self.context.id, "If A then B", PropositionType.STATEMENT, 
            status=PropositionStatus.VERIFIED
        )
        premise_b = self.engine.add_proposition(
            self.context.id, "A", PropositionType.STATEMENT, 
            status=PropositionStatus.VERIFIED
        )
        
        # Run inference
        self.engine.run_inference_engine(self.context.id)
        
        # Check for the conclusion
        conclusion = self.engine.query_context(
            context_id=self.context.id,
            text_contains="B"
        )
        self.assertIsNotNone(conclusion)
        self.assertGreaterEqual(len(conclusion), 1)
        self.assertEqual(conclusion[0].status, PropositionStatus.VERIFIED)

    def test_query_context(self):
        """Test the query_context method."""
        self.engine.add_proposition(
            context_id=self.context.id,
            text="The sky is blue",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.9,
            metadata={"source": "observation"}
        )
        self.engine.add_proposition(
            context_id=self.context.id,
            text="The sky is green",
            prop_type=PropositionType.HYPOTHESIS,
            status=PropositionStatus.UNVERIFIED
        )
        
        # Query by text
        results = self.engine.query_context(self.context.id, text_contains="blue")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "The sky is blue")
        
        # Query by type
        results = self.engine.query_context(self.context.id, prop_type=PropositionType.HYPOTHESIS)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].text, "The sky is green")
        
        # Query by status
        results = self.engine.query_context(self.context.id, status=PropositionStatus.VERIFIED)
        self.assertEqual(len(results), 1)
        
        # Query by confidence
        results = self.engine.query_context(self.context.id, min_confidence=0.8)
        self.assertEqual(len(results), 1)
        
        # Query by metadata
        results = self.engine.query_context(self.context.id, metadata_filter={"source": "observation"})
        self.assertEqual(len(results), 1)
        
        # Combined query
        results = self.engine.query_context(
            self.context.id, 
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        self.assertEqual(len(results), 1)

    def test_revise_belief_and_propagation(self):
        """Test the revise_belief method and its propagation."""
        # Add premises
        p1 = self.engine.add_proposition(
            context_id=self.context.id,
            text="If A then B",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        premise_b = self.engine.add_proposition(
            context_id=self.context.id,
            text="A",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        # Run inference to get conclusion B
        self.engine.run_inference_engine(self.context.id)
        # Find the specific proposition "B" more robustly
        possible_b_props = self.engine.query_context(self.context.id, text_contains="B")
        conclusion_b_list = [p for p in possible_b_props if p.text == "B"]
        self.assertEqual(len(conclusion_b_list), 1, f"Could not uniquely find proposition 'B'. Found: {[p.text for p in possible_b_props]}")
        conclusion_b = conclusion_b_list[0]
        self.assertEqual(conclusion_b.status, PropositionStatus.VERIFIED)
        
        # Revise the belief about "A"
        affected = self.engine.revise_belief(
            context_id=self.context.id,
            proposition_id=premise_b.id,
            new_status=PropositionStatus.REFUTED,
            justification="Test case revising belief"
        )
        
        # The conclusion "B" (identified by conclusion_b.id) should now be UNVERIFIED
        # Get the updated proposition from the context using its ID
        updated_b = self.engine.get_context(self.context.id).propositions[conclusion_b.id]
        self.assertEqual(updated_b.status, PropositionStatus.UNVERIFIED)


if __name__ == '__main__':
    unittest.main()
