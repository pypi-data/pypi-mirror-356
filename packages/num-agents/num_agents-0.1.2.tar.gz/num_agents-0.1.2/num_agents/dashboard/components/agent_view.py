"""
Composant de vue des agents pour le tableau de bord.

Ce module fournit des fonctions pour afficher les informations
sur les agents actifs, leur état et leur configuration.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os

def render_agent_view(target_dir: Path, is_system: bool = False):
    """
    Affiche la vue des agents dans le tableau de bord.
    
    Args:
        target_dir: Répertoire de l'agent ou du système à visualiser
        is_system: Indique si la cible est un système multi-agents
    """
    import streamlit as st
    
    st.header("Vue des Agents")
    
    # Chargement des informations sur les agents
    agents_info = load_agents_info(target_dir, is_system)
    
    if not agents_info:
        st.warning("Aucune information d'agent trouvée dans le répertoire spécifié.")
        return
    
    # Affichage de la liste des agents
    st.subheader("Agents actifs")
    
    for agent_name, agent_data in agents_info.items():
        with st.expander(f"Agent: {agent_name}", expanded=True):
            st.write(f"**Description:** {agent_data.get('description', 'Non spécifiée')}")
            
            # Affichage des univers
            if 'univers' in agent_data:
                st.write("**Univers activés:**")
                for univers in agent_data['univers']:
                    st.write(f"- {univers}")
            
            # Affichage de la configuration LLM
            if 'llm' in agent_data:
                st.write("**Configuration LLM:**")
                if isinstance(agent_data['llm'], dict):
                    for key, value in agent_data['llm'].items():
                        st.write(f"- {key}: {value}")
                else:
                    st.write(f"- Modèle: {agent_data['llm']}")
            
            # Affichage des fonctionnalités activées
            features = []
            for feature in ['memory', 'eventbus', 'scheduler', 'metrics', 'tracing']:
                if feature in agent_data and agent_data[feature]:
                    features.append(feature)
            
            if features:
                st.write("**Fonctionnalités activées:**")
                for feature in features:
                    st.write(f"- {feature}")
            
            # Affichage des configurations spécifiques
            if 'reasoning' in agent_data:
                st.write("**Configuration du raisonnement:**")
                for key, value in agent_data['reasoning'].items():
                    st.write(f"- {key}: {value}")
    
    # Affichage de l'état d'exécution si disponible
    if is_system and 'coordination' in list(agents_info.values())[0]:
        st.subheader("Configuration de coordination")
        coordination = list(agents_info.values())[0]['coordination']
        st.write(f"**Type:** {coordination.get('type', 'Non spécifié')}")
        st.write(f"**Mémoire partagée:** {coordination.get('shared_memory', False)}")

def load_agents_info(target_dir: Path, is_system: bool) -> Dict[str, Any]:
    """
    Charge les informations sur les agents à partir des fichiers de configuration.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        is_system: Indique si la cible est un système multi-agents
        
    Returns:
        Dictionnaire contenant les informations sur les agents
    """
    try:
        import yaml
    except ImportError:
        import streamlit as st
        st.error("Le module 'pyyaml' n'est pas installé. Veuillez l'installer avec 'pip install pyyaml'.")
        return {}
    
    agents_info = {}
    
    # Si c'est un système multi-agents, chercher le fichier de configuration du système
    if is_system:
        system_config_path = target_dir / "system.yaml"
        if system_config_path.exists():
            with open(system_config_path, 'r') as f:
                system_config = yaml.safe_load(f)
                
            if 'system' in system_config and 'agents' in system_config['system']:
                for agent_config in system_config['system']['agents']:
                    agent_name = agent_config.get('name', 'Unknown')
                    agents_info[agent_name] = agent_config
                
                # Ajouter la configuration de coordination si elle existe
                if 'coordination' in system_config['system']:
                    for agent_name in agents_info:
                        agents_info[agent_name]['coordination'] = system_config['system']['coordination']
        else:
            # Chercher les fichiers agent.yaml dans les sous-répertoires
            for subdir in target_dir.iterdir():
                if subdir.is_dir():
                    agent_config_path = subdir / "agent.yaml"
                    if agent_config_path.exists():
                        with open(agent_config_path, 'r') as f:
                            agent_config = yaml.safe_load(f)
                            
                        if 'agent' in agent_config:
                            agent_name = agent_config['agent'].get('name', subdir.name)
                            agents_info[agent_name] = agent_config['agent']
    else:
        # Chercher le fichier agent.yaml dans le répertoire cible
        agent_config_path = target_dir / "agent.yaml"
        if agent_config_path.exists():
            with open(agent_config_path, 'r') as f:
                agent_config = yaml.safe_load(f)
                
            if 'agent' in agent_config:
                agent_name = agent_config['agent'].get('name', target_dir.name)
                agents_info[agent_name] = agent_config['agent']
    
    return agents_info
