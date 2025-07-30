"""
File I/O utilities for the Nüm Agents SDK.

This module provides functions for reading and writing files,
particularly YAML configuration files.
"""

import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml


def read_yaml(file_path: str) -> Dict[str, Any]:
    """
    Read a YAML file and return its contents as a dictionary.
    
    Args:
        file_path: Path to the YAML file
        
    Returns:
        The parsed YAML content as a dictionary
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        yaml.YAMLError: If the file is not valid YAML
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def write_yaml(file_path: str, data: Dict[str, Any]) -> None:
    """
    Write a dictionary to a YAML file.
    
    Args:
        file_path: Path to the YAML file
        data: The data to write
        
    Raises:
        IOError: If the file can't be written
    """
    # Create directory if it doesn't exist
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    with open(file_path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


class AgentSpecLoader:
    """
    Loader for agent specifications.
    
    This class is responsible for loading and parsing agent specification YAML files,
    which define the configuration for an agent.
    
    The agent specification can include the following sections:
    - Basic configuration (name, description, univers, protocol, llm, etc.)
    - Working memory (goals, context, constraints, preferences)
    - Expertise (domains, skills, knowledge_bases)
    - Semantic entities (entities that the agent can manipulate)
    """
    
    def __init__(self, spec_path: str) -> None:
        """
        Initialize the agent specification loader.
        
        Args:
            spec_path: Path to the agent specification YAML file
        """
        self.spec_path = spec_path
        self._spec: Dict[str, Any] = {}
    
    def load(self) -> Dict[str, Any]:
        """
        Load the agent specification from the YAML file.
        
        Returns:
            The parsed agent specification as a dictionary
            
        Raises:
            FileNotFoundError: If the specification file doesn't exist
            yaml.YAMLError: If the specification file is not valid YAML
            ValueError: If the specification doesn't have the expected structure
        """
        self._spec = read_yaml(self.spec_path)
        
        # Validate the specification structure
        if "agent" not in self._spec:
            raise ValueError("Invalid agent specification: missing 'agent' key")
        
        agent_spec = self._spec["agent"]
        required_keys = ["name", "univers"]
        for key in required_keys:
            if key not in agent_spec:
                raise ValueError(f"Invalid agent specification: missing required key '{key}'")
        
        return self._spec
    
    def get_agent_name(self) -> str:
        """
        Get the name of the agent.
        
        Returns:
            The name of the agent
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"]["name"]
    
    def get_agent_description(self) -> Optional[str]:
        """
        Get the description of the agent.
        
        Returns:
            The description of the agent, or None if not specified
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"].get("description")
    
    def get_agent_universes(self) -> list:
        """
        Get the list of universes for the agent.
        
        Returns:
            The list of universes for the agent
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"]["univers"]
    
    def get_agent_protocol(self) -> Optional[str]:
        """
        Get the protocol for the agent.
        
        Returns:
            The protocol for the agent, or None if not specified
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"].get("protocol")
    
    def get_agent_llm(self) -> Optional[str]:
        """
        Get the LLM for the agent.
        
        Returns:
            The LLM for the agent, or None if not specified
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"].get("llm")
    
    def get_agent_config(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value for the agent.
        
        Args:
            key: The configuration key
            default: The default value to return if the key is not found
            
        Returns:
            The configuration value for the key, or the default if not found
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"].get(key, default)
    
    def get_working_memory(self) -> Dict[str, Any]:
        """
        Get the working memory configuration for the agent.
        
        Working memory contains goals, context, constraints, and preferences
        that define the agent's operational parameters.
        
        Returns:
            The working memory configuration as a dictionary, or an empty dictionary if not specified
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"].get("working_memory", {})
    
    def get_goals(self) -> List[str]:
        """
        Get the goals from the agent's working memory.
        
        Returns:
            The list of goals, or an empty list if not specified
        """
        working_memory = self.get_working_memory()
        return working_memory.get("goals", [])
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get the context from the agent's working memory.
        
        Context includes domain, project_type, user_expertise, etc.
        
        Returns:
            The context as a dictionary, or an empty dictionary if not specified
        """
        working_memory = self.get_working_memory()
        return working_memory.get("context", {})
    
    def get_constraints(self) -> List[str]:
        """
        Get the constraints from the agent's working memory.
        
        Returns:
            The list of constraints, or an empty list if not specified
        """
        working_memory = self.get_working_memory()
        return working_memory.get("constraints", [])
    
    def get_preferences(self) -> Dict[str, Any]:
        """
        Get the preferences from the agent's working memory.
        
        Returns:
            The preferences as a dictionary, or an empty dictionary if not specified
        """
        working_memory = self.get_working_memory()
        return working_memory.get("preferences", {})
    
    def get_expertise(self) -> Dict[str, Any]:
        """
        Get the expertise configuration for the agent.
        
        Expertise defines the agent's domains of knowledge, skills, and knowledge bases.
        
        Returns:
            The expertise configuration as a dictionary, or an empty dictionary if not specified
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"].get("expertise", {})
    
    def get_domains(self) -> List[Dict[str, Any]]:
        """
        Get the domains from the agent's expertise.
        
        Returns:
            The list of domains, or an empty list if not specified
        """
        expertise = self.get_expertise()
        return expertise.get("domains", [])
    
    def get_skills(self) -> List[Dict[str, Any]]:
        """
        Get the skills from the agent's expertise.
        
        Returns:
            The list of skills, or an empty list if not specified
        """
        expertise = self.get_expertise()
        return expertise.get("skills", [])
    
    def get_knowledge_bases(self) -> List[Dict[str, Any]]:
        """
        Get the knowledge bases from the agent's expertise.
        
        Returns:
            The list of knowledge bases, or an empty list if not specified
        """
        expertise = self.get_expertise()
        return expertise.get("knowledge_bases", [])
    
    def get_semantic_entities(self) -> List[Dict[str, Any]]:
        """
        Get the semantic entities configuration for the agent.
        
        Semantic entities define the entities that the agent can manipulate,
        including their properties and relations.
        
        Returns:
            The list of semantic entities, or an empty list if not specified
        """
        if not self._spec:
            self.load()
        
        return self._spec["agent"].get("semantic_entities", [])
