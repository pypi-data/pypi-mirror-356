"""
Tests for the LogicEngine class.
"""

import pytest
import uuid
from unittest.mock import patch, MagicMock

from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.models import (
    Proposition, PropositionType, PropositionStatus, PropositionSource,
    Evidence, EvidenceType,
    ProofStep, Proof,
    Criterion, CriterionType, CriterionEvaluation
)


class TestLogicEngine:
    """Tests for the LogicEngine class."""
    
    def test_create_context(self):
        """Test creating a logical context."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        assert context.id in engine.contexts
        assert engine.contexts[context.id] == context
        assert context.name == "Test Context"
        assert context.description == "A test context"
    
    def test_get_context(self):
        """Test retrieving a context by ID."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        retrieved_context = engine.get_context(context.id)
        assert retrieved_context == context
        
        # Test retrieving a non-existent context
        assert engine.get_context("non-existent") is None
    
    def test_add_proposition(self):
        """Test adding a proposition to a context."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        source = PropositionSource(type="user", identifier="user123")
        prop = engine.add_proposition(
            context_id=context.id,
            text="The sky is blue",
            prop_type=PropositionType.STATEMENT,
            source=source,
            confidence=0.9,
            metadata={"tag": "weather"}
        )
        
        # Check that the proposition was added to the context
        assert prop.id in context.propositions
        assert context.propositions[prop.id] == prop
        assert prop.text == "The sky is blue"
        assert prop.type == PropositionType.STATEMENT
        assert prop.source == source
        assert prop.confidence == 0.9
        assert prop.metadata == {"tag": "weather"}
        
        # Test adding to a non-existent context
        with pytest.raises(ValueError):
            engine.add_proposition(
                context_id="non-existent",
                text="This should fail",
                prop_type=PropositionType.STATEMENT
            )
    
    def test_add_evidence(self):
        """Test adding evidence to a context."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        # Add a proposition first
        prop = engine.add_proposition(
            context_id=context.id,
            text="The sky is blue",
            prop_type=PropositionType.STATEMENT
        )
        
        # Add evidence related to the proposition
        evidence = engine.add_evidence(
            context_id=context.id,
            text="Visual observation confirms blue color",
            evidence_type=EvidenceType.DIRECT,
            strength=0.95,
            related_propositions=[prop.id],
            metadata={"observer": "John Doe"}
        )
        
        # Check that the evidence was added to the context
        assert evidence.id in context.evidence
        assert context.evidence[evidence.id] == evidence
        assert evidence.text == "Visual observation confirms blue color"
        assert evidence.type == EvidenceType.DIRECT
        assert evidence.strength == 0.95
        assert evidence.related_propositions == [prop.id]
        assert evidence.metadata == {"observer": "John Doe"}
        
        # Test adding evidence with non-existent proposition
        with pytest.raises(ValueError):
            engine.add_evidence(
                context_id=context.id,
                text="This should fail",
                evidence_type=EvidenceType.SUPPORTING,
                strength=0.8,
                related_propositions=["non-existent"]
            )
        
        # Test adding to a non-existent context
        with pytest.raises(ValueError):
            engine.add_evidence(
                context_id="non-existent",
                text="This should fail",
                evidence_type=EvidenceType.SUPPORTING,
                strength=0.8
            )
    
    def test_create_proof(self):
        """Test creating a proof in a context."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        # Add premises and conclusion
        premise1 = engine.add_proposition(
            context_id=context.id,
            text="If it rains, the ground is wet",
            prop_type=PropositionType.STATEMENT
        )
        
        premise2 = engine.add_proposition(
            context_id=context.id,
            text="It is raining",
            prop_type=PropositionType.STATEMENT
        )
        
        conclusion = engine.add_proposition(
            context_id=context.id,
            text="The ground is wet",
            prop_type=PropositionType.STATEMENT
        )
        
        # Create a proof step
        step = ProofStep(
            id="step1",
            from_propositions=[premise1.id, premise2.id],
            to_propositions=[conclusion.id],
            rule="modus_ponens",
            justification="From 'If it rains, the ground is wet' and 'It is raining', we can deduce 'The ground is wet'"
        )
        
        # Create the proof
        proof = engine.create_proof(
            context_id=context.id,
            premise_ids=[premise1.id, premise2.id],
            conclusion_ids=[conclusion.id],
            steps=[step],
            metadata={"complexity": "simple"}
        )
        
        # Check that the proof was added to the context
        assert proof.id in context.proofs
        assert context.proofs[proof.id] == proof
        assert proof.premise_ids == [premise1.id, premise2.id]
        assert proof.conclusion_ids == [conclusion.id]
        assert len(proof.steps) == 1
        assert proof.steps[0].id == "step1"
        assert proof.metadata == {"complexity": "simple"}
        
        # Check that the conclusion's status was updated
        updated_conclusion = context.propositions[conclusion.id]
        assert updated_conclusion.status == PropositionStatus.VERIFIED
        
        # Test creating a proof with non-existent propositions
        with pytest.raises(ValueError):
            engine.create_proof(
                context_id=context.id,
                premise_ids=[premise1.id],
                conclusion_ids=["non-existent"],
                steps=[step]
            )
        
        # Test creating a proof in a non-existent context
        with pytest.raises(ValueError):
            engine.create_proof(
                context_id="non-existent",
                premise_ids=[premise1.id, premise2.id],
                conclusion_ids=[conclusion.id],
                steps=[step]
            )
    
    def test_add_criterion(self):
        """Test adding a criterion to a context."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        criterion = engine.add_criterion(
            context_id=context.id,
            criterion_type=CriterionType.CONSISTENCY,
            description="All propositions must be consistent",
            weight=0.9,
            metadata={"priority": "high"}
        )
        
        # Check that the criterion was added to the context
        assert criterion.id in context.criteria
        assert context.criteria[criterion.id] == criterion
        assert criterion.type == CriterionType.CONSISTENCY
        assert criterion.description == "All propositions must be consistent"
        assert criterion.weight == 0.9
        assert criterion.metadata == {"priority": "high"}
        
        # Test adding to a non-existent context
        with pytest.raises(ValueError):
            engine.add_criterion(
                context_id="non-existent",
                criterion_type=CriterionType.CONSISTENCY,
                description="This should fail"
            )
    
    def test_evaluate_proposition(self):
        """Test evaluating a proposition against a criterion."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        # Add a proposition and criterion
        prop = engine.add_proposition(
            context_id=context.id,
            text="E=mc²",
            prop_type=PropositionType.STATEMENT
        )
        
        criterion = engine.add_criterion(
            context_id=context.id,
            criterion_type=CriterionType.CLARITY,
            description="Propositions should be clear and unambiguous"
        )
        
        # Evaluate the proposition
        evaluation = engine.evaluate_proposition(
            context_id=context.id,
            proposition_id=prop.id,
            criterion_id=criterion.id,
            score=0.85,
            justification="The proposition is clear and precise",
            metadata={"evaluator": "peer_review"}
        )
        
        # Check that the evaluation was added to the context
        assert evaluation in context.evaluations
        assert evaluation.criterion_id == criterion.id
        assert evaluation.target_id == prop.id
        assert evaluation.target_type == "proposition"
        assert evaluation.score == 0.85
        assert evaluation.justification == "The proposition is clear and precise"
        assert evaluation.metadata == {"evaluator": "peer_review"}
        
        # Test evaluating with non-existent proposition
        with pytest.raises(ValueError):
            engine.evaluate_proposition(
                context_id=context.id,
                proposition_id="non-existent",
                criterion_id=criterion.id,
                score=0.7,
                justification="This should fail"
            )
        
        # Test evaluating with non-existent criterion
        with pytest.raises(ValueError):
            engine.evaluate_proposition(
                context_id=context.id,
                proposition_id=prop.id,
                criterion_id="non-existent",
                score=0.7,
                justification="This should fail"
            )
        
        # Test evaluating in a non-existent context
        with pytest.raises(ValueError):
            engine.evaluate_proposition(
                context_id="non-existent",
                proposition_id=prop.id,
                criterion_id=criterion.id,
                score=0.7,
                justification="This should fail"
            )
    
    def test_check_consistency(self):
        """Test checking consistency of a logical context."""
        engine = LogicEngine()
        context = engine.create_context("Test Context", "A test context")
        
        # Add consistent propositions
        prop1 = engine.add_proposition(
            context_id=context.id,
            text="All men are mortal",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        prop2 = engine.add_proposition(
            context_id=context.id,
            text="Socrates is a man",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        prop3 = engine.add_proposition(
            context_id=context.id,
            text="Socrates is mortal",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        # Check consistency - should be consistent
        is_consistent, inconsistencies = engine.check_consistency(context.id)
        assert is_consistent is True
        assert len(inconsistencies) == 0
        
        # Add an inconsistent proposition
        prop4 = engine.add_proposition(
            context_id=context.id,
            text="Socrates is immortal",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        # Also mark prop3 as refuted to create a direct contradiction
        context.propositions[prop3.id].status = PropositionStatus.REFUTED
        
        # Check consistency again - should be inconsistent
        is_consistent, inconsistencies = engine.check_consistency(context.id)
        assert is_consistent is False
        assert len(inconsistencies) > 0
        
        # Test checking consistency of a non-existent context
        with pytest.raises(ValueError):
            engine.check_consistency("non-existent")
    
    def test_export_import_context(self):
        """Test exporting and importing a logical context."""
        engine = LogicEngine()
        original_context = engine.create_context("Test Context", "A test context")
        
        # Add a proposition
        prop = engine.add_proposition(
            context_id=original_context.id,
            text="Test proposition",
            prop_type=PropositionType.STATEMENT
        )
        
        # Export the context
        exported_data = engine.export_context(original_context.id)
        
        # Create a new engine and import the context
        new_engine = LogicEngine()
        imported_context = new_engine.import_context(exported_data)
        
        # Check that the imported context matches the original
        assert imported_context.id == original_context.id
        assert imported_context.name == original_context.name
        assert imported_context.description == original_context.description
        assert prop.id in imported_context.propositions
        assert imported_context.propositions[prop.id].text == "Test proposition"
        
        # Test exporting a non-existent context
        with pytest.raises(ValueError):
            engine.export_context("non-existent")
