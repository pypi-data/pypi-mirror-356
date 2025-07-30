"""
Specialized nodes for logical reasoning in Nüm Agents SDK.

This module provides nodes that can be used in agent flows
for logical reasoning tasks.
"""

import logging
import uuid
from typing import Dict, List, Optional, Any, Union

from num_agents.core import Node, SharedStore
from num_agents.reasoning.logic_engine import LogicEngine
from num_agents.reasoning.models import (
    Proposition, PropositionType, PropositionStatus, PropositionSource,
    Evidence, EvidenceType, Criterion, CriterionType, LogicalContext
)


class LogicReasoningNode(Node):
    """
    Node for performing logical reasoning operations in a flow.
    
    This node interacts with the LogicEngine to perform operations like
    adding and evaluating propositions, building proofs, checking consistency, etc.
    """
    
    def __init__(
        self, 
        name: str,
        engine: Optional[LogicEngine] = None,
        context_name: str = "default",
        context_description: str = "Default logical reasoning context",
        shared_store_key: str = "logic_context_id",
        *args, 
        **kwargs
    ):
        """
        Initialize the logical reasoning node.
        
        Args:
            name: Name of the node
            engine: Optional logic engine to use
            context_name: Name for the logical context
            context_description: Description for the logical context
            shared_store_key: Key to use in shared store for context ID
            *args: Additional arguments to pass to Node
            **kwargs: Additional keyword arguments to pass to Node
        """
        super().__init__(name, *args, **kwargs)
        self.engine = engine or LogicEngine()
        self.context_name = context_name
        self.context_description = context_description
        self.shared_store_key = shared_store_key
        self.logger = logging.getLogger(__name__)
    
    def process(self, shared_store: SharedStore) -> None:
        """
        Process the node.
        
        This method initializes or retrieves the logical context and
        manages its lifecycle in the shared store.
        
        Args:
            shared_store: The shared store for the agent flow
        """
        # Get or create logical context
        context_id = shared_store.get(self.shared_store_key)
        if context_id is None:
            context = self.engine.create_context(self.context_name, self.context_description)
            shared_store.set(self.shared_store_key, context.id)
            self.logger.info(f"Created logical context '{self.context_name}' with ID {context.id}")
        else:
            context = self.engine.get_context(context_id)
            if context is None:
                context = self.engine.create_context(self.context_name, self.context_description)
                shared_store.set(self.shared_store_key, context.id)
                self.logger.info(f"Re-created logical context '{self.context_name}' with ID {context.id}")
            else:
                self.logger.info(f"Retrieved logical context '{context.name}' with ID {context.id}")
        
        # Process additional node-specific operations
        self._process_reasoning(context.id, shared_store)
    
    def _process_reasoning(self, context_id: str, shared_store: SharedStore) -> None:
        """
        Perform reasoning operations on the context.
        
        This method should be overridden by subclasses to implement
        specific reasoning operations.
        
        Args:
            context_id: ID of the logical context to use
            shared_store: The shared store for the agent flow
        """
        pass


class PropositionEvaluationNode(LogicReasoningNode):
    """
    Node for evaluating propositions in a logical context.
    
    This node evaluates propositions against criteria, potentially
    using external sources or LLMs for evaluation.
    """
    
    def __init__(
        self,
        name: str,
        proposition_id_key: str,
        criterion_id_key: str,
        evaluation_result_key: str,
        *args,
        **kwargs
    ):
        """
        Initialize the proposition evaluation node.
        
        Args:
            name: Name of the node
            proposition_id_key: Key to use in shared store for proposition ID
            criterion_id_key: Key to use in shared store for criterion ID
            evaluation_result_key: Key to use in shared store for evaluation result
            *args: Additional arguments to pass to LogicReasoningNode
            **kwargs: Additional keyword arguments to pass to LogicReasoningNode
        """
        super().__init__(name, *args, **kwargs)
        self.proposition_id_key = proposition_id_key
        self.criterion_id_key = criterion_id_key
        self.evaluation_result_key = evaluation_result_key
    
    def _process_reasoning(self, context_id: str, shared_store: SharedStore) -> None:
        """
        Evaluate a proposition against a criterion.
        
        This method retrieves a proposition and criterion from the shared store,
        evaluates the proposition, and stores the evaluation result.
        
        Args:
            context_id: ID of the logical context to use
            shared_store: The shared store for the agent flow
        """
        # Get proposition and criterion IDs from shared store
        proposition_id = shared_store.get(self.proposition_id_key)
        if proposition_id is None:
            self.logger.error(f"No proposition ID found in shared store key {self.proposition_id_key}")
            return
        
        criterion_id = shared_store.get(self.criterion_id_key)
        if criterion_id is None:
            self.logger.error(f"No criterion ID found in shared store key {self.criterion_id_key}")
            return
        
        # Get context
        context = self.engine.get_context(context_id)
        if context is None:
            self.logger.error(f"Context with ID {context_id} not found")
            return
        
        # Check that proposition and criterion exist
        if proposition_id not in context.propositions:
            self.logger.error(f"Proposition with ID {proposition_id} not found in context {context_id}")
            return
        
        if criterion_id not in context.criteria:
            self.logger.error(f"Criterion with ID {criterion_id} not found in context {context_id}")
            return
        
        # Get proposition and criterion
        proposition = context.propositions[proposition_id]
        criterion = context.criteria[criterion_id]
        
        # Evaluate the proposition (this could use LLM or other evaluation methods)
        score, justification = self._evaluate_proposition(proposition, criterion, context)
        
        # Store the evaluation
        evaluation = self.engine.evaluate_proposition(
            context_id=context_id,
            proposition_id=proposition_id,
            criterion_id=criterion_id,
            score=score,
            justification=justification
        )
        
        # Store evaluation result in shared store
        evaluation_result = {
            "proposition_id": proposition_id,
            "criterion_id": criterion_id,
            "score": score,
            "justification": justification
        }
        shared_store.set(self.evaluation_result_key, evaluation_result)
        
        self.logger.info(f"Evaluated proposition '{proposition.text}' against criterion '{criterion.description}'")
        self.logger.info(f"Score: {score}, Justification: {justification}")
    
    def _evaluate_proposition(
        self, 
        proposition: Proposition, 
        criterion: Criterion,
        context: LogicalContext
    ) -> tuple[float, str]:
        """
        Evaluate a proposition against a criterion.
        
        This method can be overridden to implement custom evaluation logic,
        such as using an LLM or other external services.
        
        Args:
            proposition: The proposition to evaluate
            criterion: The criterion to evaluate against
            context: The logical context
            
        Returns:
            A tuple of (score, justification)
        """
        # Default implementation uses a simple heuristic
        score = 0.5  # Neutral score by default
        justification = f"Default evaluation of proposition '{proposition.text}' against criterion '{criterion.description}'"
        
        # Simple reasoning based on proposition status
        if proposition.status == PropositionStatus.VERIFIED:
            score = 0.8
            justification = f"Proposition is verified, which generally satisfies the {criterion.type} criterion"
        elif proposition.status == PropositionStatus.REFUTED:
            score = 0.2
            justification = f"Proposition is refuted, which generally fails to satisfy the {criterion.type} criterion"
        
        return score, justification


class ConsistencyCheckNode(LogicReasoningNode):
    """
    Node for checking logical consistency in a context.
    
    This node checks the consistency of a logical context and
    reports any inconsistencies found.
    """
    
    def __init__(
        self,
        name: str,
        consistency_result_key: str,
        *args,
        **kwargs
    ):
        """
        Initialize the consistency check node.
        
        Args:
            name: Name of the node
            consistency_result_key: Key to use in shared store for consistency result
            *args: Additional arguments to pass to LogicReasoningNode
            **kwargs: Additional keyword arguments to pass to LogicReasoningNode
        """
        super().__init__(name, *args, **kwargs)
        self.consistency_result_key = consistency_result_key
    
    def _process_reasoning(self, context_id: str, shared_store: SharedStore) -> None:
        """
        Check consistency of the logical context.
        
        This method checks the logical consistency of the context and
        stores the result in the shared store.
        
        Args:
            context_id: ID of the logical context to use
            shared_store: The shared store for the agent flow
        """
        # Check consistency
        is_consistent, inconsistencies = self.engine.check_consistency(context_id)
        
        # Store consistency result in shared store
        consistency_result = {
            "is_consistent": is_consistent,
            "inconsistencies": inconsistencies
        }
        shared_store.set(self.consistency_result_key, consistency_result)
        
        if is_consistent:
            self.logger.info(f"Logical context {context_id} is consistent")
        else:
            self.logger.warning(f"Logical context {context_id} has inconsistencies: {inconsistencies}")


class PropositionImportNode(LogicReasoningNode):
    """
    Node for importing propositions from various sources.
    
    This node imports propositions from the shared store or other sources
    into the logical context.
    """
    
    def __init__(
        self,
        name: str,
        propositions_key: str,
        imported_ids_key: str,
        proposition_type: PropositionType = PropositionType.STATEMENT,
        *args,
        **kwargs
    ):
        """
        Initialize the proposition import node.
        
        Args:
            name: Name of the node
            propositions_key: Key to use in shared store for propositions to import
            imported_ids_key: Key to use in shared store for imported proposition IDs
            proposition_type: Type to assign to imported propositions
            *args: Additional arguments to pass to LogicReasoningNode
            **kwargs: Additional keyword arguments to pass to LogicReasoningNode
        """
        super().__init__(name, *args, **kwargs)
        self.propositions_key = propositions_key
        self.imported_ids_key = imported_ids_key
        self.proposition_type = proposition_type
    
    def _process_reasoning(self, context_id: str, shared_store: SharedStore) -> None:
        """
        Import propositions into the logical context.
        
        This method imports propositions from the shared store into
        the logical context.
        
        Args:
            context_id: ID of the logical context to use
            shared_store: The shared store for the agent flow
        """
        # Get propositions from shared store
        propositions = shared_store.get(self.propositions_key)
        if propositions is None:
            self.logger.warning(f"No propositions found in shared store key {self.propositions_key}")
            return
        
        if not isinstance(propositions, list):
            self.logger.error(f"Expected a list of propositions in shared store key {self.propositions_key}, got {type(propositions)}")
            return
        
        # Import propositions
        imported_ids = []
        for text in propositions:
            source = PropositionSource(type="imported", identifier=self.propositions_key)
            proposition = self.engine.add_proposition(
                context_id=context_id,
                text=text,
                prop_type=self.proposition_type,
                source=source
            )
            imported_ids.append(proposition.id)
            self.logger.info(f"Imported proposition '{text}' with ID {proposition.id}")
        
        # Store imported IDs in shared store
        shared_store.set(self.imported_ids_key, imported_ids)
        self.logger.info(f"Imported {len(imported_ids)} propositions into context {context_id}")
