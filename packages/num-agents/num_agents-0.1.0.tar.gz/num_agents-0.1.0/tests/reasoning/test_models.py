"""
Tests for the logical reasoning models.
"""

import pytest
from pydantic import ValidationError

from num_agents.reasoning.models import (
    Proposition, PropositionType, PropositionStatus, PropositionSource,
    Evidence, EvidenceType,
    ProofStep, Proof,
    Criterion, CriterionType, CriterionEvaluation,
    LogicalContext
)


class TestProposition:
    """Tests for the Proposition model."""
    
    def test_valid_proposition(self):
        """Test creating a valid proposition."""
        prop = Proposition(
            id="prop1",
            type=PropositionType.STATEMENT,
            text="The sky is blue."
        )
        assert prop.id == "prop1"
        assert prop.type == PropositionType.STATEMENT
        assert prop.text == "The sky is blue."
        assert prop.status == PropositionStatus.UNVERIFIED
        assert prop.confidence is None
        assert prop.source is None
        assert prop.metadata == {}
    
    def test_proposition_with_source(self):
        """Test creating a proposition with a source."""
        source = PropositionSource(type="user", identifier="user123")
        prop = Proposition(
            id="prop2",
            type=PropositionType.HYPOTHESIS,
            text="Coffee improves programming performance.",
            source=source
        )
        assert prop.source.type == "user"
        assert prop.source.identifier == "user123"
    
    def test_proposition_with_confidence(self):
        """Test creating a proposition with a confidence level."""
        prop = Proposition(
            id="prop3",
            type=PropositionType.CONCLUSION,
            text="This algorithm runs in O(n) time.",
            confidence=0.95
        )
        assert prop.confidence == 0.95
    
    def test_invalid_confidence(self):
        """Test that invalid confidence values are rejected."""
        with pytest.raises(ValidationError):
            Proposition(
                id="prop4",
                type=PropositionType.STATEMENT,
                text="This test should fail.",
                confidence=1.5  # Invalid: > 1.0
            )
        
        with pytest.raises(ValidationError):
            Proposition(
                id="prop5",
                type=PropositionType.STATEMENT,
                text="This test should also fail.",
                confidence=-0.1  # Invalid: < 0.0
            )


class TestEvidence:
    """Tests for the Evidence model."""
    
    def test_valid_evidence(self):
        """Test creating valid evidence."""
        evidence = Evidence(
            id="ev1",
            type=EvidenceType.DIRECT,
            text="Empirical measurements show X.",
            strength=0.8,
            related_propositions=["prop1", "prop2"]
        )
        assert evidence.id == "ev1"
        assert evidence.type == EvidenceType.DIRECT
        assert evidence.text == "Empirical measurements show X."
        assert evidence.strength == 0.8
        assert evidence.related_propositions == ["prop1", "prop2"]
        assert evidence.metadata == {}
    
    def test_invalid_strength(self):
        """Test that invalid strength values are rejected."""
        with pytest.raises(ValidationError):
            Evidence(
                id="ev2",
                type=EvidenceType.SUPPORTING,
                text="This should fail.",
                strength=1.2  # Invalid: > 1.0
            )
        
        with pytest.raises(ValidationError):
            Evidence(
                id="ev3",
                type=EvidenceType.COUNTER,
                text="This should also fail.",
                strength=-0.3  # Invalid: < 0.0
            )


class TestProof:
    """Tests for the Proof and ProofStep models."""
    
    def test_valid_proof_step(self):
        """Test creating a valid proof step."""
        step = ProofStep(
            id="step1",
            from_propositions=["p1", "p2"],
            to_propositions=["p3"],
            rule="modus_ponens",
            justification="If p1 and p1 implies p3, then p3."
        )
        assert step.id == "step1"
        assert step.from_propositions == ["p1", "p2"]
        assert step.to_propositions == ["p3"]
        assert step.rule == "modus_ponens"
        assert step.justification == "If p1 and p1 implies p3, then p3."
        assert step.metadata == {}
    
    def test_valid_proof(self):
        """Test creating a valid proof."""
        step1 = ProofStep(
            id="step1",
            from_propositions=["p1", "p2"],
            to_propositions=["p3"],
            rule="modus_ponens",
            justification="Step 1"
        )
        step2 = ProofStep(
            id="step2",
            from_propositions=["p3"],
            to_propositions=["p4"],
            rule="modus_ponens",
            justification="Step 2"
        )
        
        proof = Proof(
            id="proof1",
            premise_ids=["p1", "p2"],
            conclusion_ids=["p4"],
            steps=[step1, step2]
        )
        
        assert proof.id == "proof1"
        assert proof.premise_ids == ["p1", "p2"]
        assert proof.conclusion_ids == ["p4"]
        assert len(proof.steps) == 2
        assert proof.steps[0].id == "step1"
        assert proof.steps[1].id == "step2"
        assert proof.metadata == {}


class TestCriterion:
    """Tests for the Criterion model."""
    
    def test_valid_criterion(self):
        """Test creating a valid criterion."""
        criterion = Criterion(
            id="crit1",
            type=CriterionType.CONSISTENCY,
            description="All propositions must be consistent with each other.",
            weight=0.9
        )
        assert criterion.id == "crit1"
        assert criterion.type == CriterionType.CONSISTENCY
        assert criterion.description == "All propositions must be consistent with each other."
        assert criterion.weight == 0.9
        assert criterion.metadata == {}
    
    def test_invalid_weight(self):
        """Test that invalid weight values are rejected."""
        with pytest.raises(ValidationError):
            Criterion(
                id="crit2",
                type=CriterionType.COMPLETENESS,
                description="This should fail.",
                weight=1.1  # Invalid: > 1.0
            )
        
        with pytest.raises(ValidationError):
            Criterion(
                id="crit3",
                type=CriterionType.SOUNDNESS,
                description="This should also fail.",
                weight=-0.1  # Invalid: < 0.0
            )


class TestCriterionEvaluation:
    """Tests for the CriterionEvaluation model."""
    
    def test_valid_evaluation(self):
        """Test creating a valid criterion evaluation."""
        eval = CriterionEvaluation(
            criterion_id="crit1",
            target_id="prop1",
            target_type="proposition",
            score=0.75,
            justification="The proposition is mostly consistent with others."
        )
        assert eval.criterion_id == "crit1"
        assert eval.target_id == "prop1"
        assert eval.target_type == "proposition"
        assert eval.score == 0.75
        assert eval.justification == "The proposition is mostly consistent with others."
        assert eval.metadata == {}
    
    def test_invalid_score(self):
        """Test that invalid score values are rejected."""
        with pytest.raises(ValidationError):
            CriterionEvaluation(
                criterion_id="crit1",
                target_id="prop1",
                target_type="proposition",
                score=1.5,  # Invalid: > 1.0
                justification="This should fail."
            )
        
        with pytest.raises(ValidationError):
            CriterionEvaluation(
                criterion_id="crit1",
                target_id="prop1",
                target_type="proposition",
                score=-0.2,  # Invalid: < 0.0
                justification="This should also fail."
            )


class TestLogicalContext:
    """Tests for the LogicalContext model."""
    
    def test_create_empty_context(self):
        """Test creating an empty logical context."""
        context = LogicalContext(
            id="ctx1",
            name="Test Context",
            description="A test logical context"
        )
        assert context.id == "ctx1"
        assert context.name == "Test Context"
        assert context.description == "A test logical context"
        assert context.propositions == {}
        assert context.evidence == {}
        assert context.proofs == {}
        assert context.criteria == {}
        assert context.evaluations == []
        assert context.metadata == {}
    
    def test_create_context_with_elements(self):
        """Test creating a logical context with elements."""
        prop = Proposition(
            id="prop1",
            type=PropositionType.STATEMENT,
            text="P1"
        )
        
        evidence = Evidence(
            id="ev1",
            type=EvidenceType.SUPPORTING,
            text="Evidence for P1",
            strength=0.7,
            related_propositions=["prop1"]
        )
        
        criterion = Criterion(
            id="crit1",
            type=CriterionType.CONSISTENCY,
            description="Consistency criterion",
            weight=0.8
        )
        
        eval = CriterionEvaluation(
            criterion_id="crit1",
            target_id="prop1",
            target_type="proposition",
            score=0.9,
            justification="P1 is consistent"
        )
        
        context = LogicalContext(
            id="ctx1",
            name="Test Context",
            description="A test logical context",
            propositions={"prop1": prop},
            evidence={"ev1": evidence},
            criteria={"crit1": criterion},
            evaluations=[eval]
        )
        
        assert context.propositions["prop1"].id == "prop1"
        assert context.evidence["ev1"].id == "ev1"
        assert context.criteria["crit1"].id == "crit1"
        assert len(context.evaluations) == 1
        assert context.evaluations[0].criterion_id == "crit1"
