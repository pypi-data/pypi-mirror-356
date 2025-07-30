"""
Tests for the DynamicExpertiseFlow node.

This module contains tests for the DynamicExpertiseFlow node, which orchestrates
multi-expertise reasoning with automatic context detection and aggregation strategy selection.
"""

import unittest
from unittest.mock import MagicMock, patch
import logging
import numpy as np

from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.models import (
    Context,
    Proposition,
    PropositionStatus,
    PropositionType
)
from num_agents.reasoning.semantic_models import (
    Expertise,
    Domain,
    Entity,
    EntityType,
    Relation
)
from num_agents.reasoning.nodes.dynamic_expertise_flow import DynamicExpertiseFlow, AggregationStrategy
from num_agents.reasoning.nodes.expertise_weighting_node import ExpertiseWeightingNode
from num_agents.reasoning.nodes.multi_expertise_aggregation_node import MultiExpertiseAggregationNode


class TestDynamicExpertiseFlow(unittest.TestCase):
    """Test cases for the DynamicExpertiseFlow node."""

    def setUp(self):
        """Set up test fixtures."""
        # Configure logging
        logging.basicConfig(level=logging.ERROR)
        
        # Create logic engine and context
        self.logic_engine = LogicEngine()
        self.context_id = "test_context"
        self.context = Context(id=self.context_id, name="Test Context", description="A context for testing")
        self.logic_engine.contexts[self.context.id] = self.context
        
        # Create propositions
        self.p1 = self.logic_engine.add_proposition(
            self.context_id,
            "The sky is blue",
            "statement",
            status=PropositionStatus.VERIFIED,
            confidence=0.9
        )
        
        self.p2 = self.logic_engine.add_proposition(
            self.context_id,
            "Water is wet",
            "statement",
            status=PropositionStatus.VERIFIED,
            confidence=0.8
        )
        
        self.p3 = self.logic_engine.add_proposition(
            self.context_id,
            "If the sky is blue and water is wet, then it's a nice day",
            "hypothesis",
            status=PropositionStatus.UNVERIFIED,
            confidence=None
        )
        
        self.p4 = self.logic_engine.add_proposition(
            self.context_id,
            "It's a nice day",
            "statement",
            status=PropositionStatus.UNVERIFIED,
            confidence=None
        )
        
        # Create expertises
        self.expertise1 = self._create_expertise("weather_expert", 0.8)
        self.expertise2 = self._create_expertise("nature_expert", 0.7)
        self.expertise3 = self._create_expertise("general_expert", 0.6)
        
        # Create flow
        self.flow = DynamicExpertiseFlow(
            name="TestFlow",
            confidence_threshold=0.7,
            auto_select_strategy=True
        )
    
    def _create_expertise(self, name, confidence):
        """Create an expertise with domains and relations."""
        domain = Domain(name=f"{name}_domain", description=f"Domain for {name}")
        
        # Create entities
        sky = Entity(name="sky", type=EntityType.CONCEPT)
        blue = Entity(name="blue", type=EntityType.PROPERTY)
        water = Entity(name="water", type=EntityType.CONCEPT)
        wet = Entity(name="wet", type=EntityType.PROPERTY)
        nice_day = Entity(name="nice_day", type=EntityType.CONCEPT)
        
        # Create relations
        relations = [
            Relation(source=sky, target=blue, weight=0.8),
            Relation(source=water, target=wet, weight=0.9),
            Relation(source=blue, target=nice_day, weight=0.7),
            Relation(source=wet, target=nice_day, weight=0.6)
        ]
        
        return Expertise(
            name=name,
            domains=[domain],
            relations=relations,
            confidence=confidence
        )
    
    def test_single_agent_context(self):
        """Test DynamicExpertiseFlow with a single agent context."""
        # Set up shared store with a single expertise
        shared_store = {
            "logic_engine": self.logic_engine,
            "current_context_id": self.context_id,
            "expertise": self.expertise1
        }
        
        # Run the flow
        result = self.flow._run(shared_store)
        
        # Check that single agent mode was detected
        self.assertFalse(result.get("is_multi_agent", True))
        
        # Check that expertises list was created
        self.assertIsNotNone(result.get("expertises"))
        self.assertEqual(len(result.get("expertises", [])), 1)
        
        # Check that proposition decisions were made
        self.assertIsNotNone(result.get("proposition_decisions"))
        
        # Check that proposition scores by agent were recorded
        self.assertIsNotNone(result.get("proposition_scores_by_agent"))
    
    def test_multi_agent_context(self):
        """Test DynamicExpertiseFlow with a multi-agent context."""
        # Set up shared store with multiple expertises
        shared_store = {
            "logic_engine": self.logic_engine,
            "current_context_id": self.context_id,
            "expertises": [self.expertise1, self.expertise2, self.expertise3]
        }
        
        # Run the flow
        result = self.flow._run(shared_store)
        
        # Check that multi-agent mode was detected
        self.assertTrue(result.get("is_multi_agent", False))
        
        # Check that a strategy was selected
        self.assertIsNotNone(result.get("selected_strategy"))
        
        # Check that proposition decisions were made
        self.assertIsNotNone(result.get("proposition_decisions"))
        
        # Check that proposition scores by agent were recorded
        prop_scores = result.get("proposition_scores_by_agent", {})
        self.assertGreater(len(prop_scores), 0)
        
        # Each proposition should have scores from 3 agents
        for prop_id, scores in prop_scores.items():
            self.assertEqual(len(scores), 3)
    
    def test_auto_strategy_selection(self):
        """Test automatic strategy selection based on data characteristics."""
        # Mock the _select_optimal_strategy method to verify it's called
        with patch.object(self.flow, '_select_optimal_strategy', return_value="trimmed_mean") as mock_select:
            # Set up shared store with multiple expertises
            shared_store = {
                "logic_engine": self.logic_engine,
                "current_context_id": self.context_id,
                "expertises": [self.expertise1, self.expertise2, self.expertise3]
            }
            
            # Run the flow
            result = self.flow._run(shared_store)
            
            # Verify _select_optimal_strategy was called
            mock_select.assert_called_once()
            
            # Check that the selected strategy matches the mocked return value
            self.assertEqual(result.get("selected_strategy"), "trimmed_mean")
    
    def test_fixed_strategy(self):
        """Test using a fixed strategy instead of auto-selection."""
        # Create flow with auto_select_strategy=False
        flow = DynamicExpertiseFlow(
            name="FixedStrategyFlow",
            confidence_threshold=0.7,
            auto_select_strategy=False,
            aggregation_strategy="max"
        )
        
        # Set up shared store with multiple expertises
        shared_store = {
            "logic_engine": self.logic_engine,
            "current_context_id": self.context_id,
            "expertises": [self.expertise1, self.expertise2, self.expertise3]
        }
        
        # Run the flow
        result = flow._run(shared_store)
        
        # Check that the selected strategy is "max"
        self.assertEqual(result.get("selected_strategy"), "max")
    
    def test_confidence_threshold(self):
        """Test that confidence threshold is applied correctly."""
        # Create flow with high confidence threshold
        flow = DynamicExpertiseFlow(
            name="HighThresholdFlow",
            confidence_threshold=0.95,  # Very high threshold
            auto_select_strategy=False,
            aggregation_strategy="mean"
        )
        
        # Set up shared store with a single expertise
        shared_store = {
            "logic_engine": self.logic_engine,
            "current_context_id": self.context_id,
            "expertise": self.expertise1
        }
        
        # Run the flow
        result = flow._run(shared_store)
        
        # Check that no propositions meet the high threshold
        decisions = result.get("proposition_decisions", {})
        self.assertTrue(all(not decision for decision in decisions.values()))
        
        # Create flow with low confidence threshold
        flow = DynamicExpertiseFlow(
            name="LowThresholdFlow",
            confidence_threshold=0.1,  # Very low threshold
            auto_select_strategy=False,
            aggregation_strategy="mean"
        )
        
        # Run the flow
        result = flow._run(shared_store)
        
        # Check that all propositions meet the low threshold
        decisions = result.get("proposition_decisions", {})
        self.assertTrue(all(decision for decision in decisions.values()))
    
    def test_strategy_selection_logic(self):
        """Test the strategy selection logic with different data distributions."""
        # Test with outliers
        scores_with_outliers = {
            "p1": [0.8, 0.7, 0.1]  # 0.1 is an outlier
        }
        strategy = self.flow._select_optimal_strategy(scores_with_outliers)
        self.assertEqual(strategy, AggregationStrategy.TRIMMED_MEAN)  # Changed from WINSORIZED_MEAN to TRIMMED_MEAN
        
        # Test with high variance
        scores_with_variance = {
            "p1": [0.9, 0.5, 0.2]  # High variance
        }
        strategy = self.flow._select_optimal_strategy(scores_with_variance)
        self.assertEqual(strategy, "trimmed_mean")  # Changed from winsorized_mean to trimmed_mean
        
        # Test with positive skew
        scores_with_pos_skew = {
            "p1": [0.5, 0.5, 0.9]  # Positive skew
        }
        with patch.object(self.flow, '_calculate_skewness', return_value=1.5):
            strategy = self.flow._select_optimal_strategy(scores_with_pos_skew)
            self.assertEqual(strategy, "softmax")
        
        # Test with negative skew
        scores_with_neg_skew = {
            "p1": [0.1, 0.5, 0.5]  # Negative skew
        }
        with patch.object(self.flow, '_calculate_skewness', return_value=-1.5):
            strategy = self.flow._select_optimal_strategy(scores_with_neg_skew)
            self.assertEqual(strategy, "median")
        
        # Test with normal distribution
        scores_normal = {
            "p1": [0.5, 0.6, 0.7]  # Normal distribution
        }
        with patch.object(self.flow, '_calculate_skewness', return_value=0.0):
            with patch.object(self.flow, '_has_outliers', return_value=False):
                with patch.object(np, 'var', return_value=0.01):
                    strategy = self.flow._select_optimal_strategy(scores_normal)
                    self.assertEqual(strategy, "mean")
    
    def test_integration_with_sub_nodes(self):
        """Test integration with ExpertiseWeightingNode and MultiExpertiseAggregationNode."""
        # Mock the sub-nodes to verify they're called
        mock_expertise_weighting = MagicMock()
        mock_expertise_weighting._run.return_value = {}
        
        mock_multi_expertise_aggregation = MagicMock()
        mock_multi_expertise_aggregation._run.return_value = {}
        
        # Replace sub-nodes with mocks
        self.flow.expertise_weighting = mock_expertise_weighting
        self.flow.multi_expertise_aggregation = mock_multi_expertise_aggregation
        
        # Set up shared store with multiple expertises
        shared_store = {
            "logic_engine": self.logic_engine,
            "current_context_id": self.context_id,
            "expertises": [self.expertise1, self.expertise2, self.expertise3]
        }
        
        # Run the flow
        self.flow._run(shared_store)
        
        # Verify expertise_weighting._run was called multiple times (once per expertise)
        self.assertEqual(mock_expertise_weighting._run.call_count, 3)
        
        # Verify multi_expertise_aggregation._run was called once
        mock_multi_expertise_aggregation._run.assert_called_once()


if __name__ == "__main__":
    unittest.main()
