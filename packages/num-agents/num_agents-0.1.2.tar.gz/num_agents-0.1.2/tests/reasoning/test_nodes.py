"""
Tests for the logical reasoning nodes.
"""

import pytest
from unittest.mock import MagicMock, patch

from num_agents.core import SharedStore
from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.models import (
    Proposition, PropositionType, PropositionStatus, Criterion, CriterionType
)
from num_agents.reasoning.nodes import (
    LogicReasoningNode, PropositionEvaluationNode,
    ConsistencyCheckNode, PropositionImportNode
)


class TestLogicReasoningNode:
    """Tests for the LogicReasoningNode class."""
    
    def test_initialization(self):
        """Test initialization of LogicReasoningNode."""
        engine = LogicEngine()
        node = LogicReasoningNode("test_node", engine=engine)
        
        assert node.name == "test_node"
        assert node.engine == engine
        assert node.context_name == "default"
        assert node.context_description == "Default logical reasoning context"
        assert node.shared_store_key == "logic_context_id"
    
    def test_process_new_context(self):
        """Test processing with a new context."""
        engine = LogicEngine()
        node = LogicReasoningNode("test_node", engine=engine)
        
        # Mock the _process_reasoning method
        node._process_reasoning = MagicMock()
        
        # Create a shared store
        shared_store = SharedStore()
        
        # Process the node
        node.process(shared_store)
        
        # Check that a context was created
        context_id = shared_store.get("logic_context_id")
        assert context_id is not None
        
        # Check that the context exists in the engine
        context = engine.get_context(context_id)
        assert context is not None
        assert context.name == "default"
        
        # Check that _process_reasoning was called with the correct arguments
        node._process_reasoning.assert_called_once_with(context_id, shared_store)
    
    def test_process_existing_context(self):
        """Test processing with an existing context."""
        engine = LogicEngine()
        node = LogicReasoningNode("test_node", engine=engine)
        
        # Mock the _process_reasoning method
        node._process_reasoning = MagicMock()
        
        # Create a shared store with an existing context ID
        shared_store = SharedStore()
        context = engine.create_context("Existing Context", "An existing context")
        shared_store.set("logic_context_id", context.id)
        
        # Process the node
        node.process(shared_store)
        
        # Check that the existing context was used
        retrieved_context_id = shared_store.get("logic_context_id")
        assert retrieved_context_id == context.id
        
        # Check that _process_reasoning was called with the correct arguments
        node._process_reasoning.assert_called_once_with(context.id, shared_store)
    
    def test_process_missing_context(self):
        """Test processing with a missing context ID."""
        engine = LogicEngine()
        node = LogicReasoningNode("test_node", engine=engine)
        
        # Mock the _process_reasoning method
        node._process_reasoning = MagicMock()
        
        # Create a shared store with a non-existent context ID
        shared_store = SharedStore()
        shared_store.set("logic_context_id", "non-existent")
        
        # Process the node
        node.process(shared_store)
        
        # Check that a new context was created
        context_id = shared_store.get("logic_context_id")
        assert context_id != "non-existent"
        
        # Check that the context exists in the engine
        context = engine.get_context(context_id)
        assert context is not None
        
        # Check that _process_reasoning was called with the correct arguments
        node._process_reasoning.assert_called_once_with(context_id, shared_store)


class TestPropositionEvaluationNode:
    """Tests for the PropositionEvaluationNode class."""
    
    def test_initialization(self):
        """Test initialization of PropositionEvaluationNode."""
        engine = LogicEngine()
        node = PropositionEvaluationNode(
            name="test_node",
            proposition_id_key="prop_id",
            criterion_id_key="crit_id",
            evaluation_result_key="eval_result",
            engine=engine
        )
        
        assert node.name == "test_node"
        assert node.engine == engine
        assert node.proposition_id_key == "prop_id"
        assert node.criterion_id_key == "crit_id"
        assert node.evaluation_result_key == "eval_result"
    
    def test_process_reasoning(self):
        """Test _process_reasoning method."""
        engine = LogicEngine()
        node = PropositionEvaluationNode(
            name="test_node",
            proposition_id_key="prop_id",
            criterion_id_key="crit_id",
            evaluation_result_key="eval_result",
            engine=engine
        )
        
        # Create a context with a proposition and criterion
        context = engine.create_context("Test Context", "A test context")
        prop = engine.add_proposition(
            context_id=context.id,
            text="The sky is blue",
            prop_type=PropositionType.STATEMENT
        )
        criterion = engine.add_criterion(
            context_id=context.id,
            criterion_type=CriterionType.CLARITY,
            description="Clarity criterion"
        )
        
        # Mock the _evaluate_proposition method
        node._evaluate_proposition = MagicMock(return_value=(0.8, "This is clear"))
        
        # Create a shared store
        shared_store = SharedStore()
        shared_store.set("logic_context_id", context.id)
        shared_store.set("prop_id", prop.id)
        shared_store.set("crit_id", criterion.id)
        
        # Process the node
        node.process(shared_store)
        
        # Check that _evaluate_proposition was called
        node._evaluate_proposition.assert_called_once()
        
        # Check that the evaluation result was stored
        eval_result = shared_store.get("eval_result")
        assert eval_result is not None
        assert eval_result["proposition_id"] == prop.id
        assert eval_result["criterion_id"] == criterion.id
        assert eval_result["score"] == 0.8
        assert eval_result["justification"] == "This is clear"
    
    def test_process_reasoning_missing_proposition(self):
        """Test _process_reasoning with missing proposition."""
        engine = LogicEngine()
        node = PropositionEvaluationNode(
            name="test_node",
            proposition_id_key="prop_id",
            criterion_id_key="crit_id",
            evaluation_result_key="eval_result",
            engine=engine
        )
        
        # Create a context
        context = engine.create_context("Test Context", "A test context")
        
        # Create a shared store without a proposition ID
        shared_store = SharedStore()
        shared_store.set("logic_context_id", context.id)
        
        # Process the node
        node.process(shared_store)
        
        # Check that no evaluation result was stored
        assert shared_store.get("eval_result") is None
    
    def test_evaluate_proposition(self):
        """Test the default _evaluate_proposition method."""
        engine = LogicEngine()
        node = PropositionEvaluationNode(
            name="test_node",
            proposition_id_key="prop_id",
            criterion_id_key="crit_id",
            evaluation_result_key="eval_result",
            engine=engine
        )
        
        # Create a context with propositions
        context = engine.create_context("Test Context", "A test context")
        
        # Create propositions with different statuses
        verified_prop = Proposition(
            id="verified",
            text="Verified proposition",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        refuted_prop = Proposition(
            id="refuted",
            text="Refuted proposition",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.REFUTED
        )
        
        unverified_prop = Proposition(
            id="unverified",
            text="Unverified proposition",
            type=PropositionType.STATEMENT,
            status=PropositionStatus.UNVERIFIED
        )
        
        # Create a criterion
        criterion = Criterion(
            id="crit1",
            type=CriterionType.CONSISTENCY,
            description="Consistency criterion"
        )
        
        # Evaluate propositions
        score1, justification1 = node._evaluate_proposition(verified_prop, criterion, context)
        score2, justification2 = node._evaluate_proposition(refuted_prop, criterion, context)
        score3, justification3 = node._evaluate_proposition(unverified_prop, criterion, context)
        
        # Check results
        assert score1 > 0.5  # Verified should have a high score
        assert score2 < 0.5  # Refuted should have a low score
        assert score3 == 0.5  # Unverified should have a neutral score


class TestConsistencyCheckNode:
    """Tests for the ConsistencyCheckNode class."""
    
    def test_initialization(self):
        """Test initialization of ConsistencyCheckNode."""
        engine = LogicEngine()
        node = ConsistencyCheckNode(
            name="test_node",
            consistency_result_key="consistency",
            engine=engine
        )
        
        assert node.name == "test_node"
        assert node.engine == engine
        assert node.consistency_result_key == "consistency"
    
    def test_process_reasoning_consistent(self):
        """Test _process_reasoning with a consistent context."""
        engine = LogicEngine()
        node = ConsistencyCheckNode(
            name="test_node",
            consistency_result_key="consistency",
            engine=engine
        )
        
        # Create a context with consistent propositions
        context = engine.create_context("Test Context", "A test context")
        engine.add_proposition(
            context_id=context.id,
            text="A is B",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        engine.add_proposition(
            context_id=context.id,
            text="B is C",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        # Create a shared store
        shared_store = SharedStore()
        shared_store.set("logic_context_id", context.id)
        
        # Process the node
        node.process(shared_store)
        
        # Check that the consistency result was stored
        consistency = shared_store.get("consistency")
        assert consistency is not None
        assert consistency["is_consistent"] is True
        assert len(consistency["inconsistencies"]) == 0
    
    def test_process_reasoning_inconsistent(self):
        """Test _process_reasoning with an inconsistent context."""
        engine = LogicEngine()
        node = ConsistencyCheckNode(
            name="test_node",
            consistency_result_key="consistency",
            engine=engine
        )
        
        # Create a context with inconsistent propositions
        context = engine.create_context("Test Context", "A test context")
        prop1 = engine.add_proposition(
            context_id=context.id,
            text="X is Y",
            prop_type=PropositionType.STATEMENT,
            status=PropositionStatus.VERIFIED
        )
        
        # Update the proposition to be both verified and refuted
        context.propositions[prop1.id].status = PropositionStatus.REFUTED
        
        # Create a shared store
        shared_store = SharedStore()
        shared_store.set("logic_context_id", context.id)
        
        # Process the node
        node.process(shared_store)
        
        # Check that the consistency result was stored
        consistency = shared_store.get("consistency")
        assert consistency is not None
        assert consistency["is_consistent"] is False
        assert len(consistency["inconsistencies"]) > 0


class TestPropositionImportNode:
    """Tests for the PropositionImportNode class."""
    
    def test_initialization(self):
        """Test initialization of PropositionImportNode."""
        engine = LogicEngine()
        node = PropositionImportNode(
            name="test_node",
            propositions_key="props",
            imported_ids_key="imported_ids",
            proposition_type=PropositionType.HYPOTHESIS,
            engine=engine
        )
        
        assert node.name == "test_node"
        assert node.engine == engine
        assert node.propositions_key == "props"
        assert node.imported_ids_key == "imported_ids"
        assert node.proposition_type == PropositionType.HYPOTHESIS
    
    def test_process_reasoning(self):
        """Test _process_reasoning method."""
        engine = LogicEngine()
        node = PropositionImportNode(
            name="test_node",
            propositions_key="props",
            imported_ids_key="imported_ids",
            proposition_type=PropositionType.HYPOTHESIS,
            engine=engine
        )
        
        # Create a context
        context = engine.create_context("Test Context", "A test context")
        
        # Create a shared store with propositions
        shared_store = SharedStore()
        shared_store.set("logic_context_id", context.id)
        shared_store.set("props", [
            "Hypothesis 1",
            "Hypothesis 2",
            "Hypothesis 3"
        ])
        
        # Process the node
        node.process(shared_store)
        
        # Check that propositions were imported
        imported_ids = shared_store.get("imported_ids")
        assert imported_ids is not None
        assert len(imported_ids) == 3
        
        # Check that the propositions exist in the context
        for prop_id in imported_ids:
            prop = context.propositions[prop_id]
            assert prop.type == PropositionType.HYPOTHESIS
            assert prop.text in ["Hypothesis 1", "Hypothesis 2", "Hypothesis 3"]
    
    def test_process_reasoning_missing_propositions(self):
        """Test _process_reasoning with missing propositions."""
        engine = LogicEngine()
        node = PropositionImportNode(
            name="test_node",
            propositions_key="props",
            imported_ids_key="imported_ids",
            engine=engine
        )
        
        # Create a context
        context = engine.create_context("Test Context", "A test context")
        
        # Create a shared store without propositions
        shared_store = SharedStore()
        shared_store.set("logic_context_id", context.id)
        
        # Process the node
        node.process(shared_store)
        
        # Check that no propositions were imported
        assert shared_store.get("imported_ids") is None
    
    def test_process_reasoning_invalid_propositions(self):
        """Test _process_reasoning with invalid propositions."""
        engine = LogicEngine()
        node = PropositionImportNode(
            name="test_node",
            propositions_key="props",
            imported_ids_key="imported_ids",
            engine=engine
        )
        
        # Create a context
        context = engine.create_context("Test Context", "A test context")
        
        # Create a shared store with invalid propositions
        shared_store = SharedStore()
        shared_store.set("logic_context_id", context.id)
        shared_store.set("props", "Not a list")  # Invalid: not a list
        
        # Process the node
        node.process(shared_store)
        
        # Check that no propositions were imported
        assert shared_store.get("imported_ids") is None
