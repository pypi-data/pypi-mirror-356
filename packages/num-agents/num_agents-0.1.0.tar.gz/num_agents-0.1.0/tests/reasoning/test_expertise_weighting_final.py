"""
Tests for expertise-based weighting in the LogicEngine.
"""
import pytest
from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.models import (
    Proposition, 
    PropositionType, 
    PropositionStatus,
    LogicalContext
)
from num_agents.reasoning.semantic_models import (
    Expertise,
    ExpertiseDomain,
    SemanticEntity
)


class TestExpertiseWeighting:
    """Test cases for expertise-based weighting in LogicEngine."""
    
    def test_domain_relevance_inference(self):
        """Test that domain relevance is correctly inferred for propositions."""
        # Create a logic engine with expertise
        engine = LogicEngine()
        
        # Set up expertise with domains
        engine.expertise = Expertise(
            domains=[
                ExpertiseDomain(
                    name="finance",
                    description="Financial analysis and investment strategies",
                    proficiency=0.8
                ),
                ExpertiseDomain(
                    name="technology",
                    description="Software development and computer science",
                    proficiency=0.4
                )
            ]
        )
        
        # Create a context
        context_id = engine.create_context("test_context", "Test context for domain relevance inference")
        
        # Add propositions related to different domains
        finance_prop = engine.add_proposition(
            context_id=context_id,
            text="The stock market is volatile today",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.7
        )
        
        tech_prop = engine.add_proposition(
            context_id=context_id,
            text="Python is a programming language",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.7
        )
        
        unrelated_prop = engine.add_proposition(
            context_id=context_id,
            text="The sky is blue",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.7
        )
        
        # Manually trigger domain relevance inference
        engine._infer_domain_relevance(finance_prop)
        engine._infer_domain_relevance(tech_prop)
        engine._infer_domain_relevance(unrelated_prop)
        
        # Check that domain relevance was correctly inferred
        assert "finance" in finance_prop.domain_relevance
        assert finance_prop.domain_relevance["finance"] > 0.5
        
        assert "technology" in tech_prop.domain_relevance
        assert tech_prop.domain_relevance["technology"] > 0.5
        
        # Unrelated proposition should have no domain relevance or very low
        assert not unrelated_prop.domain_relevance or all(
            score < 0.3 for score in unrelated_prop.domain_relevance.values()
        )
    
    def test_expertise_confidence_calculation(self):
        """Test that confidence is correctly adjusted based on expertise."""
        # Create a logic engine with expertise
        engine = LogicEngine()
        
        # Set up expertise with domains
        engine.expertise = Expertise(
            domains=[
                ExpertiseDomain(
                    name="finance",
                    description="Financial analysis and investment strategies",
                    proficiency=0.9  # High expertise
                ),
                ExpertiseDomain(
                    name="technology",
                    description="Software development and computer science",
                    proficiency=0.3  # Low expertise
                )
            ]
        )
        
        # Create propositions with different domain relevance
        finance_prop = Proposition(
            id="finance_prop_2",
            text="The stock market is volatile today",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.7
        )
        finance_prop.set_domain_relevance("finance", 0.9)  # High finance relevance
        
        tech_prop = Proposition(
            id="tech_prop_2",
            text="Python is a programming language",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.7
        )
        tech_prop.set_domain_relevance("technology", 0.9)  # High tech relevance
        
        mixed_prop = Proposition(
            id="mixed_prop_1",
            text="Financial software systems need robust testing",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.7
        )
        # Make sure mixed_prop has a different expertise factor by setting domain relevance
        # to trigger different thresholds in _calculate_expertise_confidence
        mixed_prop.set_domain_relevance("finance", 0.4)  # Medium finance relevance
        mixed_prop.set_domain_relevance("technology", 0.4)  # Medium tech relevance
        
        # Calculate expertise confidence factors
        finance_factor = engine._calculate_expertise_confidence(finance_prop)
        tech_factor = engine._calculate_expertise_confidence(tech_prop)
        mixed_factor = engine._calculate_expertise_confidence(mixed_prop)
        
        # High expertise should increase confidence or keep it the same
        assert finance_factor >= 1.0
        
        # Low expertise should decrease confidence
        assert tech_factor < 1.0
        
        # Based on the implementation of _calculate_expertise_confidence,
        # we expect tech_factor to be 0.7 (low expertise), mixed_factor to be 0.9 (medium expertise),
        # and finance_factor to be 1.1 (high expertise)
        assert tech_factor < mixed_factor < finance_factor
    
    def test_inference_with_expertise_weighting(self):
        """Test that inference results are weighted by expertise."""
        # Create a logic engine with expertise
        engine = LogicEngine()
        
        # Set up expertise with domains
        engine.expertise = Expertise(
            domains=[
                ExpertiseDomain(
                    name="finance",
                    description="Financial analysis and investment strategies",
                    proficiency=0.9  # High expertise
                ),
                ExpertiseDomain(
                    name="technology",
                    description="Software development and computer science",
                    proficiency=0.3  # Low expertise
                )
            ]
        )
        
        # Create a context
        context_id = engine.create_context("test_context", "Test context for inference with expertise weighting")
        
        # Add a rule that will derive new propositions
        from num_agents.reasoning.rules import Conjunction
        engine.register_rule("conjunction", Conjunction())
        
        # Add propositions that will trigger the rule
        finance_prop1 = engine.add_proposition(
            context_id=context_id,
            text="The stock market is trending upward",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.8,
            domain_relevance={"finance": 0.9}
        )
        
        finance_prop2 = engine.add_proposition(
            context_id=context_id,
            text="Interest rates are decreasing",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.8,
            domain_relevance={"finance": 0.9}
        )
        
        tech_prop1 = engine.add_proposition(
            context_id=context_id,
            text="Python 3.9 has new features",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.8,
            domain_relevance={"technology": 0.9}
        )
        
        tech_prop2 = engine.add_proposition(
            context_id=context_id,
            text="TypeScript improves JavaScript",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED,
            confidence=0.8,
            domain_relevance={"technology": 0.9}
        )
        
        # Apply inference
        new_props = engine.apply_inference(context_id)
        
        # Find the derived conjunction propositions
        finance_conjunction = None
        tech_conjunction = None
        
        for prop in new_props:
            if "stock market" in prop.text and "interest rates" in prop.text:
                finance_conjunction = prop
            elif "Python" in prop.text and "TypeScript" in prop.text:
                tech_conjunction = prop
        
        # Both conjunctions should exist
        assert finance_conjunction is not None, "Finance conjunction not found"
        assert tech_conjunction is not None, "Tech conjunction not found"
        
        # The finance conjunction should have higher confidence due to higher expertise
        assert finance_conjunction.confidence > tech_conjunction.confidence
        
        # The finance conjunction confidence should be close to the original confidence
        assert abs(finance_conjunction.confidence - 0.8) < 0.1
        
        # The tech conjunction confidence should be lower due to low expertise
        assert tech_conjunction.confidence < 0.8 * 0.9  # Assuming factor around 0.7-0.9
