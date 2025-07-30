"""
Semantic models for the reasoning engine.

This module defines the data models for semantic entities and expertise
that can be used in the reasoning engine.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field, validator


class EntityType(str, Enum):
    """Types of entities in the semantic model."""
    CONCEPT = "concept"
    PROPERTY = "property"
    ACTION = "action"
    EVENT = "event"
    OBJECT = "object"
    PERSON = "person"
    PLACE = "place"
    TIME = "time"
    UNIT = "unit"
    VALUE = "value"
    OTHER = "other"


class EntityProperty(BaseModel):
    """
    A property of a semantic entity.
    
    Properties define attributes that an entity can have,
    such as name, type, value, etc.
    """
    name: str = Field(..., description="Name of the property")
    type: str = Field(..., description="Data type of the property")
    description: Optional[str] = Field(None, description="Description of the property")
    required: bool = Field(default=False, description="Whether the property is required")
    default_value: Optional[Any] = Field(None, description="Default value for the property")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class EntityRelation(BaseModel):
    """
    A relation between semantic entities.
    
    Relations define how entities are connected to each other,
    such as "contains", "belongs_to", "derived_from", etc.
    """
    name: str = Field(..., description="Name of the relation")
    target: str = Field(..., description="Target entity type for the relation")
    description: Optional[str] = Field(None, description="Description of the relation")
    cardinality: Optional[str] = Field(None, description="Cardinality of the relation (e.g., 'one-to-one', 'one-to-many')")
    inverse_relation: Optional[str] = Field(None, description="Name of the inverse relation, if any")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SemanticEntity(BaseModel):
    """
    A semantic entity that can be reasoned about.
    
    Semantic entities represent concepts, objects, or ideas that can be
    referenced in propositions and used in logical reasoning.
    """
    name: str = Field(..., description="Name of the entity type")
    description: Optional[str] = Field(None, description="Description of the entity type")
    properties: List[EntityProperty] = Field(default_factory=list, description="Properties of the entity")
    relations: List[EntityRelation] = Field(default_factory=list, description="Relations to other entities")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ExpertiseDomain(BaseModel):
    """
    A domain of expertise for an agent.
    
    Expertise domains define areas of knowledge that an agent can have,
    such as "data_analysis", "machine_learning", etc.
    """
    name: str = Field(..., description="Name of the expertise domain")
    proficiency: float = Field(..., description="Proficiency level (0.0 to 1.0)")
    description: Optional[str] = Field(None, description="Description of the expertise domain")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('proficiency')
    def validate_proficiency(cls, v):
        """Validate that proficiency is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Proficiency must be between 0.0 and 1.0")
        return v


class ExpertiseSkill(BaseModel):
    """
    A specific skill within an expertise domain.
    
    Skills are more specific abilities within a domain,
    such as "python_programming" within "software_development".
    """
    name: str = Field(..., description="Name of the skill")
    proficiency: float = Field(..., description="Proficiency level (0.0 to 1.0)")
    domain: Optional[str] = Field(None, description="Domain this skill belongs to")
    description: Optional[str] = Field(None, description="Description of the skill")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('proficiency')
    def validate_proficiency(cls, v):
        """Validate that proficiency is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Proficiency must be between 0.0 and 1.0")
        return v


class KnowledgeBase(BaseModel):
    """
    A knowledge base referenced by an agent.
    
    Knowledge bases are sources of information that an agent can use,
    such as "statistics_fundamentals", "visualization_best_practices", etc.
    """
    name: str = Field(..., description="Name of the knowledge base")
    source: str = Field(..., description="Source of the knowledge base ('internal' or 'external')")
    url: Optional[str] = Field(None, description="URL of the knowledge base, if external")
    description: Optional[str] = Field(None, description="Description of the knowledge base")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Entity(BaseModel):
    """
    A semantic entity in the knowledge graph.
    
    Entities represent concepts, objects, or ideas that can be
    referenced in propositions and used in logical reasoning.
    """
    name: str = Field(..., description="Name of the entity")
    type: EntityType = Field(..., description="Type of the entity")
    description: Optional[str] = Field(None, description="Description of the entity")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Relation(BaseModel):
    """
    A relation between entities in the knowledge graph.
    
    Relations define how entities are connected to each other.
    """
    source: Entity = Field(..., description="Source entity of the relation")
    target: Entity = Field(..., description="Target entity of the relation")
    weight: float = Field(default=1.0, description="Weight of the relation (0.0 to 1.0)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('weight')
    def validate_weight(cls, v):
        """Validate that weight is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Weight must be between 0.0 and 1.0")
        return v


class Domain(BaseModel):
    """
    A domain of knowledge in the expertise model.
    
    Domains represent areas of knowledge that an agent can have expertise in.
    """
    name: str = Field(..., description="Name of the domain")
    description: Optional[str] = Field(None, description="Description of the domain")
    proficiency: float = Field(default=0.5, description="Proficiency level (0.0 to 1.0)")
    entities: List[Entity] = Field(default_factory=list, description="Entities in this domain")
    relations: List[Relation] = Field(default_factory=list, description="Relations in this domain")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('proficiency')
    def validate_proficiency(cls, v):
        """Validate that proficiency is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError(f"Proficiency must be between 0.0 and 1.0, got {v}")
        return v


class Expertise(BaseModel):
    """
    The expertise of an agent.
    
    Expertise defines the agent's domains of knowledge, skills, and knowledge bases.
    """
    name: str = Field(..., description="Name of the expertise")
    domains: List[Domain] = Field(default_factory=list, description="Domains of expertise")
    relations: List[Relation] = Field(default_factory=list, description="Relations between entities")
    confidence: float = Field(default=0.5, description="Overall confidence in this expertise (0.0 to 1.0)")
    skills: List[ExpertiseSkill] = Field(default_factory=list, description="Skills within domains")
    knowledge_bases: List[KnowledgeBase] = Field(default_factory=list, description="Knowledge bases")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        """Validate that confidence is between 0.0 and 1.0."""
        if v < 0.0 or v > 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class EntityInstance(BaseModel):
    """
    An instance of a semantic entity.
    
    Entity instances are concrete occurrences of entity types,
    with specific values for properties and relations to other instances.
    """
    id: str = Field(..., description="Unique identifier for the entity instance")
    entity_type: str = Field(..., description="Type of the entity")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Property values")
    relations: Dict[str, List[str]] = Field(default_factory=dict, description="Relations to other entity instances")
    confidence: Optional[float] = Field(None, description="Confidence in the entity instance (0.0 to 1.0)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        """Validate that confidence is between 0.0 and 1.0."""
        if v is not None and (v < 0.0 or v > 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v
