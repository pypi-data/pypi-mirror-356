"""
Logic engine for Nüm Agents SDK.

This module provides the core logic reasoning engine that operates on
propositions, evidence, and proofs to evaluate logical validity.
It includes advanced capabilities such as rule-based inference,
complex query capabilities, and belief revision.
"""

import logging
import uuid
from typing import Dict, List, Optional, Set, Tuple, Any, Union, Callable
import json
import copy
from collections import defaultdict

from num_agents.reasoning.models import (
    Proposition, PropositionType, PropositionStatus, PropositionSource,
    Evidence, EvidenceType,
    Proof, ProofStep,
    Criterion, CriterionType, CriterionEvaluation,
    LogicalContext
)
from num_agents.reasoning.rules import STANDARD_RULES, LogicalRule
from num_agents.reasoning.semantic_models import (
    SemanticEntity, EntityInstance, Expertise, ExpertiseDomain, ExpertiseSkill
)
from num_agents.memory.entity_knowledge_base import EntityKnowledgeBase
from num_agents.utils.file_io import AgentSpecLoader


class LogicEngine:
    """
    Engine for logical reasoning operations.
    
    The LogicEngine is responsible for managing logical contexts,
    evaluating propositions, checking logical consistency, and
    building proofs.
    
    It can also integrate with expertise domains and semantic entities
    to enhance reasoning capabilities with domain-specific knowledge.
    """
    
    def __init__(self, agent_spec_loader: Optional[AgentSpecLoader] = None):
        """
        Initialize the logic engine.
        
        Args:
            agent_spec_loader: Optional AgentSpecLoader to load expertise and semantic entities
        """
        self.contexts: Dict[str, LogicalContext] = {}
        self.logger = logging.getLogger(__name__)
        self.rules: Dict[str, LogicalRule] = {}
        
        # Initialize expertise and semantic entities
        self.expertise: Optional[Expertise] = None
        self.entity_knowledge_base: EntityKnowledgeBase = EntityKnowledgeBase()
        
        # Load expertise and semantic entities if agent_spec_loader is provided
        if agent_spec_loader:
            self.load_from_agent_spec(agent_spec_loader)
        
        self._register_standard_rules()
    
    def _register_standard_rules(self):
        """Register the standard set of logical rules."""
        for name, rule in STANDARD_RULES.items():
            self.register_rule(name, rule)
            
    def register_rule(self, name: str, rule: LogicalRule):
        """Register a new logical rule for inference."""
        if name in self.rules:
            self.logger.warning(f"Rule '{name}' is already registered. Overwriting.")
        self.rules[name] = rule
        self.logger.info(f"Registered rule: {name}")
        
    def load_from_agent_spec(self, agent_spec_loader: AgentSpecLoader) -> None:
        """
        Load expertise and semantic entities from an agent specification.
        
        Args:
            agent_spec_loader: The AgentSpecLoader containing expertise and semantic entity definitions
        """
        self.logger.info("Loading expertise and semantic entities from agent specification")
        
        # Load expertise
        expertise_data = agent_spec_loader.get_expertise()
        
        # Create domains
        domains = []
        for domain_data in expertise_data.get("domains", []):
            domain = ExpertiseDomain(
                name=domain_data["name"],
                proficiency=domain_data["proficiency"],
                description=domain_data.get("description")
            )
            domains.append(domain)
            
        # Create skills
        skills = []
        for skill_data in expertise_data.get("skills", []):
            skill = ExpertiseSkill(
                name=skill_data["name"],
                proficiency=skill_data["proficiency"],
                domain=skill_data.get("domain"),
                description=skill_data.get("description")
            )
            skills.append(skill)
            
        # Create knowledge bases
        knowledge_bases = []
        for kb_data in expertise_data.get("knowledge_bases", []):
            kb = KnowledgeBase(
                name=kb_data["name"],
                source=kb_data["source"],
                url=kb_data.get("url"),
                description=kb_data.get("description")
            )
            knowledge_bases.append(kb)
            
        # Create expertise object
        self.expertise = Expertise(
            domains=domains,
            skills=skills,
            knowledge_bases=knowledge_bases
        )
        
        # Load semantic entities into knowledge base
        self.entity_knowledge_base.load_from_agent_spec(agent_spec_loader)
        
        self.logger.info(f"Loaded {len(domains)} domains, {len(skills)} skills, {len(knowledge_bases)} knowledge bases, "
                       f"and {len(agent_spec_loader.get_semantic_entities())} semantic entity types")
        
    def get_expertise(self) -> Optional[Expertise]:
        """
        Get the expertise object.
        
        Returns:
            The expertise object, or None if not loaded
        """
        return self.expertise
        
    def get_entity_knowledge_base(self) -> EntityKnowledgeBase:
        """
        Get the entity knowledge base.
        
        Returns:
            The entity knowledge base
        """
        return self.entity_knowledge_base
    
    def create_context(self, name: str, description: str) -> LogicalContext:
        """
        Create a new logical context.
        
        Args:
            name: Name of the context
            description: Description of the context
            
        Returns:
            The created logical context
        """
        context_id = str(uuid.uuid4())
        context = LogicalContext(
            id=context_id,
            name=name,
            description=description
        )
        self.contexts[context_id] = context
        self.logger.info(f"Created logical context '{name}' with ID {context_id}")
        return context
    
    def get_context(self, context_id: str) -> Optional[LogicalContext]:
        """
        Get a logical context by ID.
        
        Args:
            context_id: ID of the context to get
            
        Returns:
            The logical context, or None if not found
        """
        return self.contexts.get(context_id)
    
    def add_proposition(
        self, 
        context_id: str, 
        text: str, 
        prop_type: PropositionType,
        source: Optional[PropositionSource] = None,
        status: PropositionStatus = PropositionStatus.UNVERIFIED,
        confidence: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
        entity_references: Optional[List[str]] = None,
        entity_relations: Optional[List[Dict[str, str]]] = None,
        domain_relevance: Optional[Dict[str, float]] = None
    ) -> Proposition:
        """
        Add a proposition to a logical context.
        
        Args:
            context_id: ID of the context to add the proposition to
            text: Textual representation of the proposition
            prop_type: Type of the proposition
            source: Source of the proposition (optional)
            status: Initial status of the proposition (default: UNVERIFIED)
            confidence: Initial confidence level (optional)
            metadata: Additional metadata (optional)
            entity_references: IDs of referenced entity instances (optional)
            entity_relations: Relations between referenced entities (optional)
            domain_relevance: Relevance scores for expertise domains (optional)
            
        Returns:
            The created proposition
            
        Raises:
            ValueError: If the context does not exist
        """
        context = self.get_context(context_id)
        if not context:
            raise ValueError(f"Context with ID '{context_id}' does not exist")
            
        prop_id = str(uuid.uuid4())
        prop = Proposition(
            id=prop_id,
            type=prop_type,
            text=text,
            status=status,
            confidence=confidence,
            source=source,
            metadata=metadata or {},
            entity_references=entity_references or [],
            entity_relations=entity_relations or [],
            domain_relevance=domain_relevance or {}
        )
        
        # If we have expertise and no domain_relevance was provided, try to infer it
        if self.expertise and not domain_relevance:
            self._infer_domain_relevance(prop)
        
        context.propositions[prop_id] = prop
        self.logger.info(f"Added proposition '{text}' to context {context_id}")
        return prop
    
    def update_proposition_domain_relevance(self, proposition_id: str, domain_relevance: dict) -> None:
        """
        Update the domain_relevance field of a proposition by its ID in all contexts.
        """
        for context in self.contexts.values():
            if proposition_id in context.propositions:
                context.propositions[proposition_id].domain_relevance = domain_relevance
                
    def update_proposition_confidence(self, proposition_id: str, confidence: float) -> None:
        """
        Update the confidence field of a proposition by its ID in all contexts.
        
        Args:
            proposition_id: The ID of the proposition to update
            confidence: The new confidence value (between 0.0 and 1.0)
        """
        for context in self.contexts.values():
            if proposition_id in context.propositions:
                context.propositions[proposition_id].confidence = confidence
                self.logger.info(f"Updated domain_relevance for proposition {proposition_id}.")
                return
        self.logger.warning(f"Proposition with ID {proposition_id} not found in any context.")

    def add_evidence(
        self,
        context_id: str,
        text: str,
        evidence_type: EvidenceType,
        strength: float,
        related_propositions: List[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Evidence:
        """
        Add evidence to a logical context.
        
        Args:
            context_id: ID of the context to add the evidence to
            text: Text of the evidence
            evidence_type: Type of the evidence
            strength: Strength of the evidence (0.0 to 1.0)
            related_propositions: IDs of related propositions
            metadata: Additional metadata
            
        Returns:
            The created evidence
            
        Raises:
            ValueError: If the context does not exist
        """
        context = self.get_context(context_id)
        if context is None:
            raise ValueError(f"Context with ID {context_id} not found")
        
        # Validate that related propositions exist
        if related_propositions:
            for prop_id in related_propositions:
                if prop_id not in context.propositions:
                    raise ValueError(f"Proposition with ID {prop_id} not found in context {context_id}")
        
        evidence_id = str(uuid.uuid4())
        evidence = Evidence(
            id=evidence_id,
            type=evidence_type,
            text=text,
            strength=strength,
            related_propositions=related_propositions or [],
            metadata=metadata or {}
        )
        
        context.evidence[evidence_id] = evidence
        self.logger.info(f"Added evidence '{text}' to context {context_id}")
        return evidence
    
    def create_proof(
        self,
        context_id: str,
        premise_ids: List[str],
        conclusion_ids: List[str],
        steps: List[ProofStep],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Proof:
        """
        Create a proof in a logical context.
        
        Args:
            context_id: ID of the context to create the proof in
            premise_ids: IDs of premise propositions
            conclusion_ids: IDs of conclusion propositions
            steps: Steps in the proof
            metadata: Additional metadata
            
        Returns:
            The created proof
            
        Raises:
            ValueError: If the context does not exist or if propositions do not exist
        """
        context = self.get_context(context_id)
        if context is None:
            raise ValueError(f"Context with ID {context_id} not found")
        
        # Validate that propositions exist
        for prop_id in premise_ids + conclusion_ids:
            if prop_id not in context.propositions:
                raise ValueError(f"Proposition with ID {prop_id} not found in context {context_id}")
        
        # Validate proof steps
        for step in steps:
            for prop_id in step.from_propositions + step.to_propositions:
                if prop_id not in context.propositions:
                    raise ValueError(f"Proposition with ID {prop_id} not found in context {context_id}")
        
        proof_id = str(uuid.uuid4())
        proof = Proof(
            id=proof_id,
            premise_ids=premise_ids,
            conclusion_ids=conclusion_ids,
            steps=steps,
            metadata=metadata or {}
        )
        
        context.proofs[proof_id] = proof
        self.logger.info(f"Created proof with ID {proof_id} in context {context_id}")
        
        # Update proposition statuses
        for conclusion_id in conclusion_ids:
            proposition = context.propositions[conclusion_id]
            proposition.status = PropositionStatus.VERIFIED
            context.propositions[conclusion_id] = proposition
        
        return proof
    
    def add_criterion(
        self,
        context_id: str,
        criterion_type: CriterionType,
        description: str,
        weight: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Criterion:
        """
        Add an evaluation criterion to a logical context.
        
        Args:
            context_id: ID of the context to add the criterion to
            criterion_type: Type of the criterion
            description: Description of the criterion
            weight: Relative weight of the criterion (0.0 to 1.0)
            metadata: Additional metadata
            
        Returns:
            The created criterion
            
        Raises:
            ValueError: If the context does not exist
        """
        context = self.get_context(context_id)
        if context is None:
            raise ValueError(f"Context with ID {context_id} not found")
        
        criterion_id = str(uuid.uuid4())
        criterion = Criterion(
            id=criterion_id,
            type=criterion_type,
            description=description,
            weight=weight,
            metadata=metadata or {}
        )
        
        context.criteria[criterion_id] = criterion
        self.logger.info(f"Added criterion '{description}' to context {context_id}")
        return criterion
    
    def evaluate_proposition(
        self,
        context_id: str,
        proposition_id: str,
        criterion_id: str,
        score: float,
        justification: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CriterionEvaluation:
        """
        Evaluate a proposition against a criterion.
        
        Args:
            context_id: ID of the context containing the proposition
            proposition_id: ID of the proposition to evaluate
            criterion_id: ID of the criterion to evaluate against
            score: Evaluation score (0.0 to 1.0)
            justification: Justification for the evaluation
            metadata: Additional metadata
            
        Returns:
            The created evaluation
            
        Raises:
            ValueError: If the context, proposition, or criterion does not exist
        """
        context = self.get_context(context_id)
        if context is None:
            raise ValueError(f"Context with ID {context_id} not found")
        
        if proposition_id not in context.propositions:
            raise ValueError(f"Proposition with ID {proposition_id} not found in context {context_id}")
        
        if criterion_id not in context.criteria:
            raise ValueError(f"Criterion with ID {criterion_id} not found in context {context_id}")
        
        evaluation = CriterionEvaluation(
            criterion_id=criterion_id,
            target_id=proposition_id,
            target_type="proposition",
            score=score,
            justification=justification,
            metadata=metadata or {}
        )
        
        context.evaluations.append(evaluation)
        self.logger.info(f"Evaluated proposition {proposition_id} against criterion {criterion_id} in context {context_id}")
        return evaluation
    
    def check_consistency(self, context_id: str) -> Tuple[bool, List[str]]:
        """
        Check logical consistency of a context.
        
        Args:
            context_id: ID of the context to check
            
        Returns:
            A tuple of (is_consistent, inconsistency_details)
            
        Raises:
            ValueError: If the context does not exist
        """
        context = self.get_context(context_id)
        if context is None:
            raise ValueError(f"Context with ID {context_id} not found")
        
        # Map of proposition IDs to their statuses
        proposition_statuses = {
            prop_id: prop.status for prop_id, prop in context.propositions.items()
        }
        
        # Check for direct contradictions
        inconsistencies = []
        verified_props = {
            prop_id for prop_id, status in proposition_statuses.items() 
            if status == PropositionStatus.VERIFIED
        }
        refuted_props = {
            prop_id for prop_id, status in proposition_statuses.items() 
            if status == PropositionStatus.REFUTED
        }
        
        # Check if any proposition is both verified and refuted
        for prop_id in verified_props.intersection(refuted_props):
            prop = context.propositions[prop_id]
            inconsistencies.append(
                f"Proposition '{prop.text}' (ID: {prop_id}) is both verified and refuted."
            )
        
        # Check for contradictions through proofs
        for proof_id, proof in context.proofs.items():
            for conclusion_id in proof.conclusion_ids:
                if conclusion_id in refuted_props:
                    premises = [context.propositions[pid].text for pid in proof.premise_ids]
                    conclusion = context.propositions[conclusion_id].text
                    inconsistencies.append(
                        f"Proof {proof_id} derives a refuted conclusion '{conclusion}' from premises: {', '.join(premises)}"
                    )
        
        is_consistent = len(inconsistencies) == 0
        return is_consistent, inconsistencies
    
    def get_verification_path(
        self, 
        context_id: str, 
        proposition_id: str
    ) -> Optional[List[ProofStep]]:
        """
        Get the chain of reasoning that verifies a proposition.
        
        Args:
            context_id: ID of the context containing the proposition
            proposition_id: ID of the proposition to find a verification path for
            
        Returns:
            A list of proof steps that verify the proposition, or None if not verified
            
        Raises:
            ValueError: If the context or proposition does not exist
        """
        context = self.get_context(context_id)
        if context is None:
            raise ValueError(f"Context with ID {context_id} not found")
        
        if proposition_id not in context.propositions:
            raise ValueError(f"Proposition with ID {proposition_id} not found in context {context_id}")
        
        # Find proofs that verify this proposition
        verification_paths = []
        for proof_id, proof in context.proofs.items():
            if proposition_id in proof.conclusion_ids:
                verification_paths.extend(proof.steps)
        
        return verification_paths if verification_paths else None

    def _infer_domain_relevance(self, proposition: Proposition) -> None:
        """
        Infer domain relevance scores for a proposition based on its content.
        
        This method analyzes the proposition text and any referenced entities
        to determine its relevance to different expertise domains.
        
        Args:
            proposition: The proposition to analyze
        """
        if not self.expertise or not self.expertise.domains:
            return
            
        # Simple keyword-based relevance scoring for now
        # In a real implementation, this could use more sophisticated NLP techniques
        for domain in self.expertise.domains:
            score = 0.0
            
            # Check if domain name or related keywords appear in the proposition text
            if domain.name.lower() in proposition.text.lower():
                score += 0.7
                
            # Check description keywords if available
            if domain.description:
                keywords = domain.description.lower().split()
                for keyword in keywords:
                    if len(keyword) > 3 and keyword in proposition.text.lower():
                        score += 0.3
                        break
                        
            # Check if any referenced entities are related to this domain
            for entity_id in proposition.entity_references:
                entity = self.entity_knowledge_base.get_entity(entity_id)
                if entity and domain.name.lower() in entity.metadata.get("domains", []):
                    score += 0.5
                    
            # Normalize score to 0.0-1.0 range and set if significant
            score = min(1.0, score)
            if score > 0.2:  # Only set if there's some meaningful relevance
                proposition.set_domain_relevance(domain.name, score)
                
    def _calculate_expertise_confidence(self, proposition: Proposition) -> float:
        """
        Calculate a confidence modifier based on agent expertise.
        
        This method evaluates how the agent's expertise in relevant domains
        should affect the confidence in a proposition.
        
        Args:
            proposition: The proposition to evaluate
            
        Returns:
            A confidence modifier (0.0 to 1.0) based on expertise
        """
        if not self.expertise or not proposition.domain_relevance:
            return 1.0  # No expertise data or domain relevance, so no modification
            
        total_relevance = sum(proposition.domain_relevance.values())
        if total_relevance == 0:
            return 1.0  # No relevant domains
            
        weighted_expertise = 0.0
        
        # Calculate weighted expertise based on domain relevance and proficiency
        for domain_name, relevance in proposition.domain_relevance.items():
            # Find the domain in expertise
            domain_expertise = 0.5  # Default medium expertise if domain not found
            for domain in self.expertise.domains:
                if domain.name == domain_name:
                    domain_expertise = domain.proficiency
                    break
                    
            # Weight the domain expertise by its relevance to the proposition
            weighted_expertise += (domain_expertise * relevance)
            
        # Normalize by total relevance
        expertise_factor = weighted_expertise / total_relevance
        
        # Scale the confidence modifier: low expertise reduces confidence,
        # high expertise increases it slightly
        if expertise_factor < 0.3:
            return 0.7  # Low expertise significantly reduces confidence
        elif expertise_factor < 0.7:
            return 0.9  # Medium expertise slightly reduces confidence
        else:
            return 1.1  # High expertise slightly increases confidence (capped at 1.0 later)
            
    def apply_inference(self, context_id: str) -> List[Proposition]:
        """
        Apply all registered inference rules to the context once.

        Args:
            context_id: ID of the context to apply inference to

        Returns:
            A list of newly derived propositions
        """
        context = self.get_context(context_id)
        if not context:
            raise ValueError(f"Context with ID {context_id} not found")

        newly_derived_propositions = []
        existing_texts = {p.text for p in context.propositions.values()}

        for rule_name, rule in self.rules.items():
            try:
                # Pass the current list of all propositions to the rule
                current_propositions = list(context.propositions.values())
                result = rule.apply(context, current_propositions)
                
                if result:
                    new_propositions, proof_step = result
                    for new_prop in new_propositions:
                        # Prevent adding propositions that are textual duplicates
                        # Rules are now responsible for setting the correct status (typically VERIFIED)
                        if new_prop.text not in existing_texts:
                            # Ensure the rule has set a status, default to UNVERIFIED if not (though rules should set it)
                            if new_prop.status is None:
                                self.logger.warning(f"Rule {rule_name} derived proposition {new_prop.text} without an explicit status. Defaulting to UNVERIFIED.")
                                new_prop.status = PropositionStatus.UNVERIFIED
                            
                            # Infer domain relevance if not already set and we have expertise data
                            if not new_prop.domain_relevance and self.expertise:
                                self._infer_domain_relevance(new_prop)
                            
                            # Adjust confidence based on expertise if confidence is set
                            if new_prop.confidence is not None and self.expertise:
                                expertise_factor = self._calculate_expertise_confidence(new_prop)
                                new_prop.confidence = min(1.0, new_prop.confidence * expertise_factor)
                                self.logger.debug(f"Adjusted confidence for proposition '{new_prop.text}' by factor {expertise_factor} based on expertise")
                            
                            context.propositions[new_prop.id] = new_prop
                            existing_texts.add(new_prop.text)
                            newly_derived_propositions.append(new_prop)
                            self.logger.info(f"Derived new proposition via {rule_name}: {new_prop.text} with status {new_prop.status} and confidence {new_prop.confidence}")
                            
                            # Create a new proof for this inference
                            self.create_proof(
                                context_id=context_id,
                                premise_ids=proof_step.from_propositions,
                                conclusion_ids=proof_step.to_propositions,
                                steps=[proof_step]
                            )

            except Exception as e:
                self.logger.error(f"Error applying rule {rule_name}: {e}", exc_info=True)
        
        return newly_derived_propositions

    def run_inference_engine(self, context_id: str, max_iterations: int = 10) -> int:
        """
        Run the inference engine until no new propositions are derived.

        Args:
            context_id: ID of the context to run inference on
            max_iterations: Maximum number of iterations to prevent infinite loops

        Returns:
            The total number of newly derived propositions
        """
        total_new_propositions = 0
        for i in range(max_iterations):
            self.logger.info(f"Inference iteration {i+1}")
            newly_derived = self.apply_inference(context_id)
            if not newly_derived:
                self.logger.info("Inference stabilized. No new propositions derived.")
                break
            total_new_propositions += len(newly_derived)
        else:
            self.logger.warning("Inference engine reached max iterations.")
        
        return total_new_propositions

    def query_context(
        self, 
        context_id: str, 
        text_contains: Optional[str] = None,
        prop_type: Optional[PropositionType] = None,
        status: Optional[PropositionStatus] = None,
        min_confidence: Optional[float] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Proposition]:
        """
        Query for propositions in a context based on multiple criteria.

        Args:
            context_id: ID of the context to query
            text_contains: Substring to search for in proposition text (case-insensitive)
            prop_type: Type of proposition to filter by
            status: Status of proposition to filter by
            min_confidence: Minimum confidence level
            metadata_filter: Dictionary to filter metadata by

        Returns:
            A list of propositions matching the criteria
        """
        context = self.get_context(context_id)
        if not context:
            raise ValueError(f"Context with ID {context_id} not found")
        
        results = []
        for prop in context.propositions.values():
            if text_contains and text_contains.lower() not in prop.text.lower():
                continue
            if prop_type and prop.type != prop_type:
                continue
            if status and prop.status != status:
                continue
            if min_confidence and (prop.confidence is None or prop.confidence < min_confidence):
                continue
            if metadata_filter:
                match = all(
                    prop.metadata.get(k) == v for k, v in metadata_filter.items()
                )
                if not match:
                    continue
            results.append(prop)
            
        return results

    def revise_belief(
        self, 
        context_id: str, 
        proposition_id: str, 
        new_status: PropositionStatus,
        justification: str
    ) -> List[str]:
        """
        Revise the status of a proposition and propagate the consequences.

        Args:
            context_id: ID of the context
            proposition_id: ID of the proposition to revise
            new_status: The new status for the proposition
            justification: Justification for the revision

        Returns:
            A list of IDs of other propositions whose status was changed as a result.
        """
        context = self.get_context(context_id)
        if not context:
            raise ValueError(f"Context with ID {context_id} not found")
        
        if proposition_id not in context.propositions:
            raise ValueError(f"Proposition with ID {proposition_id} not found")

        proposition = context.propositions[proposition_id]
        if proposition.status == new_status:
            return []

        self.logger.info(f"Revising belief for proposition {proposition_id}: {proposition.status} -> {new_status}")
        proposition.status = new_status
        proposition.metadata['revision_justification'] = justification

        # This is a simplified propagation mechanism.
        # A more robust implementation would use a proper Truth Maintenance System (TMS).
        affected_propositions = []

        # If a proposition is refuted, all conclusions derived from it may become unverified
        if new_status == PropositionStatus.REFUTED:
            for proof in context.proofs.values():
                if proposition_id in proof.premise_ids:
                    for conclusion_id in proof.conclusion_ids:
                        conclusion = context.propositions[conclusion_id]
                        if conclusion.status == PropositionStatus.VERIFIED:
                            conclusion.status = PropositionStatus.UNVERIFIED
                            conclusion.metadata['revision_justification'] = (
                                f"A premise ('{proposition.text}') was refuted."
                            )
                            affected_propositions.append(conclusion_id)
                            self.logger.info(f"Proposition {conclusion_id} status changed to UNVERIFIED due to refutation of premise.")

        # Re-run inference to see if new conclusions can be drawn
        self.run_inference_engine(context_id)

        return affected_propositions
    
    def export_context(self, context_id: str) -> Dict[str, Any]:
        """
        Export a logical context as a dictionary.
        
        Args:
            context_id: ID of the context to export
            
        Returns:
            Dictionary representation of the context
            
        Raises:
            ValueError: If the context does not exist
        """
        context = self.get_context(context_id)
        if context is None:
            raise ValueError(f"Context with ID {context_id} not found")
        
        return json.loads(context.json())
    
    def import_context(self, context_data: Dict[str, Any]) -> LogicalContext:
        """
        Import a logical context from a dictionary.
        
        Args:
            context_data: Dictionary representation of the context
            
        Returns:
            The imported logical context
        """
        context = LogicalContext(**context_data)
        self.contexts[context.id] = context
        self.logger.info(f"Imported logical context '{context.name}' with ID {context.id}")
        return context
