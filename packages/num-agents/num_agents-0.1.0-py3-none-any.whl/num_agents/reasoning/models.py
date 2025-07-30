"""
Logic reasoning models for Nüm Agents SDK.

This module defines Pydantic models for logical reasoning components,
including propositions, proofs, and criteria.
"""

from enum import Enum
from typing import Dict, List, Optional, Union, Any, Set
from pydantic import BaseModel, Field, validator
from num_agents.reasoning.semantic_models import EntityInstance


class PropositionType(str, Enum):
    """Types of logical propositions."""
    STATEMENT = "statement"
    QUESTION = "question"
    HYPOTHESIS = "hypothesis"
    CONCLUSION = "conclusion"
    AXIOM = "axiom"
    LEMMA = "lemma"
    THEOREM = "theorem"


class PropositionStatus(str, Enum):
    """Status of a proposition's evaluation."""
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    REFUTED = "refuted"
    UNDECIDABLE = "undecidable"
    PENDING = "pending"


class PropositionSource(BaseModel):
    """Source information for a proposition."""
    type: str = Field(..., description="Type of source (e.g., 'user', 'system', 'inference')")
    identifier: Optional[str] = Field(None, description="Identifier for the source")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata about the source")


class Proposition(BaseModel):
    """
    A logical proposition that can be reasoned about.
    
    Propositions are statements that can be evaluated as true or false,
    or questions that can be answered through logical reasoning.
    
    Propositions can be linked to semantic entities, allowing for
    reasoning about entities and their relationships.
    """
    id: str = Field(..., description="Unique identifier for the proposition")
    type: PropositionType = Field(..., description="Type of the proposition")
    text: str = Field(..., description="The textual representation of the proposition")
    status: PropositionStatus = Field(default=PropositionStatus.UNVERIFIED, description="Current evaluation status")
    confidence: Optional[float] = Field(None, description="Confidence level (0.0 to 1.0)")
    source: Optional[PropositionSource] = Field(None, description="Source of the proposition")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # New fields for semantic entity integration
    entity_references: List[str] = Field(default_factory=list, description="IDs of referenced entity instances")
    entity_relations: List[Dict[str, str]] = Field(default_factory=list, 
                                                 description="Relations between referenced entities in this proposition")
    domain_relevance: Dict[str, float] = Field(default_factory=dict, 
                                             description="Relevance scores for expertise domains (0.0 to 1.0)")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        """Validate that confidence is between 0.0 and 1.0."""
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v
        
    @validator('domain_relevance')
    def validate_domain_relevance(cls, v):
        """Validate that domain relevance scores are between 0.0 and 1.0."""
        for domain, score in v.items():
            if score < 0.0 or score > 1.0:
                raise ValueError(f"Domain relevance score for {domain} must be between 0.0 and 1.0")
        return v
        
    def get_entity_instances(self, entity_knowledge_base) -> List[EntityInstance]:
        """
        Get the entity instances referenced by this proposition.
        
        Args:
            entity_knowledge_base: The knowledge base containing entity instances
            
        Returns:
            A list of entity instances referenced by this proposition
        """
        return [entity_knowledge_base.get_entity(entity_id) for entity_id in self.entity_references]
        
    def add_entity_reference(self, entity_id: str) -> None:
        """
        Add a reference to an entity instance.
        
        Args:
            entity_id: ID of the entity instance to reference
        """
        if entity_id not in self.entity_references:
            self.entity_references.append(entity_id)
            
    def add_entity_relation(self, source_id: str, relation: str, target_id: str) -> None:
        """
        Add a relation between referenced entities.
        
        Args:
            source_id: ID of the source entity instance
            relation: Name of the relation
            target_id: ID of the target entity instance
        """
        relation_dict = {"source": source_id, "relation": relation, "target": target_id}
        if relation_dict not in self.entity_relations:
            self.entity_relations.append(relation_dict)
            
    def set_domain_relevance(self, domain: str, score: float) -> None:
        """
        Set the relevance score for an expertise domain.
        
        Args:
            domain: Name of the expertise domain
            score: Relevance score (0.0 to 1.0)
        """
        if score < 0.0 or score > 1.0:
            raise ValueError(f"Domain relevance score must be between 0.0 and 1.0")
        self.domain_relevance[domain] = score


class EvidenceType(str, Enum):
    """Types of evidence in logical reasoning."""
    DIRECT = "direct"
    INDIRECT = "indirect"
    COUNTER = "counter"
    SUPPORTING = "supporting"
    EXAMPLE = "example"
    COUNTER_EXAMPLE = "counter_example"


class Evidence(BaseModel):
    """
    Evidence used to support or refute a proposition.
    
    Evidence can be direct (explicitly showing the proposition is true),
    indirect (supporting the proposition), or counter (refuting the proposition).
    """
    id: str = Field(..., description="Unique identifier for the evidence")
    type: EvidenceType = Field(..., description="Type of evidence")
    text: str = Field(..., description="Textual representation of the evidence")
    strength: float = Field(..., description="Strength of the evidence (0.0 to 1.0)")
    related_propositions: List[str] = Field(default_factory=list, description="IDs of related propositions")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('strength')
    def validate_strength(cls, v):
        """Validate that strength is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Strength must be between 0.0 and 1.0")
        return v


class ProofStep(BaseModel):
    """
    A step in a logical proof.
    
    Proof steps connect propositions through logical rules to build
    a chain of reasoning leading to a conclusion.
    """
    id: str = Field(..., description="Unique identifier for the proof step")
    from_propositions: List[str] = Field(..., description="IDs of premises/source propositions")
    to_propositions: List[str] = Field(..., description="IDs of conclusions/derived propositions")
    rule: str = Field(..., description="Logical rule applied (e.g., 'modus_ponens', 'syllogism')")
    justification: str = Field(..., description="Textual justification for the step")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Proof(BaseModel):
    """
    A logical proof connecting premises to a conclusion.
    
    Proofs consist of a sequence of proof steps that together
    demonstrate how a conclusion follows from given premises.
    """
    id: str = Field(..., description="Unique identifier for the proof")
    premise_ids: List[str] = Field(..., description="IDs of premise propositions")
    conclusion_ids: List[str] = Field(..., description="IDs of conclusion propositions")
    steps: List[ProofStep] = Field(..., description="Steps in the proof")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class CriterionType(str, Enum):
    """Types of evaluation criteria for logical reasoning."""
    CONSISTENCY = "consistency"
    COMPLETENESS = "completeness"
    SOUNDNESS = "soundness"
    RELEVANCE = "relevance"
    CLARITY = "clarity"
    PARSIMONY = "parsimony"


class Criterion(BaseModel):
    """
    A criterion for evaluating logical reasoning.
    
    Criteria are used to assess the quality of propositions, evidence,
    and proofs in terms of factors like consistency, completeness, etc.
    """
    id: str = Field(..., description="Unique identifier for the criterion")
    type: CriterionType = Field(..., description="Type of criterion")
    description: str = Field(..., description="Description of the criterion")
    weight: float = Field(default=1.0, description="Relative weight of the criterion (0.0 to 1.0)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('weight')
    def validate_weight(cls, v):
        """Validate that weight is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Weight must be between 0.0 and 1.0")
        return v


class CriterionEvaluation(BaseModel):
    """
    Evaluation of a logical element against a criterion.
    
    CriterionEvaluations assess how well a proposition, evidence, or proof
    meets a specific criterion, resulting in a score and justification.
    """
    criterion_id: str = Field(..., description="ID of the criterion")
    target_id: str = Field(..., description="ID of the evaluated element (proposition, evidence, or proof)")
    target_type: str = Field(..., description="Type of evaluated element ('proposition', 'evidence', 'proof')")
    score: float = Field(..., description="Evaluation score (0.0 to 1.0)")
    justification: str = Field(..., description="Justification for the evaluation")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('score')
    def validate_score(cls, v):
        """Validate that score is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Score must be between 0.0 and 1.0")
        return v


class LogicalContext(BaseModel):
    """
    Context for logical reasoning operations.
    
    LogicalContext contains all the logical elements (propositions, evidence, proofs)
    and their evaluations that are relevant for reasoning about a particular topic.
    """
    id: str = Field(..., description="Unique identifier for the context")
    name: str = Field(..., description="Name of the logical context")
    description: str = Field(..., description="Description of the context")
    propositions: Dict[str, Proposition] = Field(default_factory=dict, description="Propositions in the context")
    evidence: Dict[str, Evidence] = Field(default_factory=dict, description="Evidence in the context")
    proofs: Dict[str, Proof] = Field(default_factory=dict, description="Proofs in the context")
    criteria: Dict[str, Criterion] = Field(default_factory=dict, description="Evaluation criteria")
    evaluations: List[CriterionEvaluation] = Field(default_factory=list, description="Criterion evaluations")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    def add_proposition(self, proposition: Proposition) -> None:
        """Add a proposition to the context."""
        self.propositions[proposition.id] = proposition

    def get_proposition(self, proposition_id: str) -> Optional[Proposition]:
        """Get a proposition by ID."""
        return self.propositions.get(proposition_id)


# Alias for backward compatibility
Context = LogicalContext
