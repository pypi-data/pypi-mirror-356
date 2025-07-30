"""
Entity Knowledge Base for managing semantic entities.

This module provides a knowledge base for storing and querying
semantic entities and their relationships.
"""

from typing import Any, Dict, List, Optional, Set, Union
import uuid

from num_agents.reasoning.semantic_models import (
    EntityInstance, EntityProperty, EntityRelation, SemanticEntity
)


class EntityKnowledgeBase:
    """
    A knowledge base for storing and querying semantic entities.
    
    The EntityKnowledgeBase manages entity definitions (types) and
    entity instances, allowing for storage, retrieval, and querying
    of entities and their relationships.
    """
    
    def __init__(self):
        """Initialize an empty entity knowledge base."""
        self._entity_types: Dict[str, SemanticEntity] = {}
        self._entity_instances: Dict[str, EntityInstance] = {}
        
    def add_entity_type(self, entity_type: SemanticEntity) -> None:
        """
        Add an entity type to the knowledge base.
        
        Args:
            entity_type: The entity type to add
        """
        self._entity_types[entity_type.name] = entity_type
        
    def get_entity_type(self, name: str) -> Optional[SemanticEntity]:
        """
        Get an entity type by name.
        
        Args:
            name: Name of the entity type to retrieve
            
        Returns:
            The entity type, or None if not found
        """
        return self._entity_types.get(name)
        
    def add_entity_instance(self, instance: EntityInstance) -> None:
        """
        Add an entity instance to the knowledge base.
        
        Args:
            instance: The entity instance to add
        """
        self._entity_instances[instance.id] = instance
        
    def create_entity_instance(self, entity_type: str, properties: Dict[str, Any] = None) -> EntityInstance:
        """
        Create and add a new entity instance.
        
        Args:
            entity_type: Type of the entity to create
            properties: Property values for the entity
            
        Returns:
            The created entity instance
            
        Raises:
            ValueError: If the entity type does not exist
        """
        if entity_type not in self._entity_types:
            raise ValueError(f"Entity type '{entity_type}' does not exist")
            
        instance_id = str(uuid.uuid4())
        instance = EntityInstance(
            id=instance_id,
            entity_type=entity_type,
            properties=properties or {}
        )
        
        self.add_entity_instance(instance)
        return instance
        
    def get_entity(self, entity_id: str) -> Optional[EntityInstance]:
        """
        Get an entity instance by ID.
        
        Args:
            entity_id: ID of the entity instance to retrieve
            
        Returns:
            The entity instance, or None if not found
        """
        return self._entity_instances.get(entity_id)
        
    def query_entities(self, entity_type: Optional[str] = None, 
                      properties: Optional[Dict[str, Any]] = None) -> List[EntityInstance]:
        """
        Query entity instances by type and properties.
        
        Args:
            entity_type: Type of entities to retrieve (optional)
            properties: Property values to match (optional)
            
        Returns:
            A list of matching entity instances
        """
        results = []
        
        for instance in self._entity_instances.values():
            # Filter by entity type if specified
            if entity_type and instance.entity_type != entity_type:
                continue
                
            # Filter by properties if specified
            if properties:
                match = True
                for key, value in properties.items():
                    if key not in instance.properties or instance.properties[key] != value:
                        match = False
                        break
                        
                if not match:
                    continue
                    
            results.append(instance)
            
        return results
        
    def add_relation(self, source_id: str, relation: str, target_id: str) -> None:
        """
        Add a relation between entity instances.
        
        Args:
            source_id: ID of the source entity instance
            relation: Name of the relation
            target_id: ID of the target entity instance
            
        Raises:
            ValueError: If either entity instance does not exist
        """
        source = self.get_entity(source_id)
        target = self.get_entity(target_id)
        
        if not source:
            raise ValueError(f"Source entity '{source_id}' does not exist")
        if not target:
            raise ValueError(f"Target entity '{target_id}' does not exist")
            
        if relation not in source.relations:
            source.relations[relation] = []
            
        if target_id not in source.relations[relation]:
            source.relations[relation].append(target_id)
            
    def query_related_entities(self, entity_id: str, relation: Optional[str] = None) -> Dict[str, List[EntityInstance]]:
        """
        Query entities related to a given entity.
        
        Args:
            entity_id: ID of the entity instance
            relation: Name of the relation to filter by (optional)
            
        Returns:
            A dictionary mapping relation names to lists of related entity instances
            
        Raises:
            ValueError: If the entity instance does not exist
        """
        entity = self.get_entity(entity_id)
        if not entity:
            raise ValueError(f"Entity '{entity_id}' does not exist")
            
        result = {}
        
        for rel_name, target_ids in entity.relations.items():
            if relation and rel_name != relation:
                continue
                
            result[rel_name] = [self.get_entity(target_id) for target_id in target_ids if self.get_entity(target_id)]
            
        return result
        
    def load_from_agent_spec(self, agent_spec_loader) -> None:
        """
        Load entity types from an agent specification.
        
        Args:
            agent_spec_loader: The AgentSpecLoader containing entity definitions
        """
        semantic_entities = agent_spec_loader.get_semantic_entities()
        
        for entity_def in semantic_entities:
            properties = []
            for prop in entity_def.get("properties", []):
                properties.append(EntityProperty(
                    name=prop["name"],
                    type=prop["type"],
                    description=prop.get("description"),
                    required=prop.get("required", False),
                    default_value=prop.get("default_value")
                ))
                
            relations = []
            for rel in entity_def.get("relations", []):
                relations.append(EntityRelation(
                    name=rel["name"],
                    target=rel["target"],
                    description=rel.get("description"),
                    cardinality=rel.get("cardinality"),
                    inverse_relation=rel.get("inverse_relation")
                ))
                
            entity_type = SemanticEntity(
                name=entity_def["name"],
                description=entity_def.get("description"),
                properties=properties,
                relations=relations
            )
            
            self.add_entity_type(entity_type)
