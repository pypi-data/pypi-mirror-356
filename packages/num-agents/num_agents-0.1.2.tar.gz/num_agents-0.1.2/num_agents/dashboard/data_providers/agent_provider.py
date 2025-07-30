"""
Fournisseur de données pour les informations sur les agents.

Ce module contient les fonctions pour charger et traiter les informations
sur les agents à partir des fichiers de configuration et de l'état d'exécution.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml
import json
import os

def load_agent_config(agent_dir: Path) -> Dict[str, Any]:
    """
    Charge la configuration d'un agent à partir de son fichier de configuration.
    
    Args:
        agent_dir: Répertoire de l'agent
        
    Returns:
        Dictionnaire contenant la configuration de l'agent
    """
    config_path = agent_dir / "agent.yaml"
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'agent' in config:
            return config['agent']
        return {}
    except Exception as e:
        print(f"Erreur lors du chargement de la configuration de l'agent: {e}")
        return {}

def load_system_config(system_dir: Path) -> Dict[str, Any]:
    """
    Charge la configuration d'un système multi-agents.
    
    Args:
        system_dir: Répertoire du système
        
    Returns:
        Dictionnaire contenant la configuration du système
    """
    config_path = system_dir / "system.yaml"
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        if 'system' in config:
            return config['system']
        return {}
    except Exception as e:
        print(f"Erreur lors du chargement de la configuration du système: {e}")
        return {}

def get_agent_directories(target_dir: Path) -> List[Path]:
    """
    Récupère les répertoires des agents dans un système multi-agents.
    
    Args:
        target_dir: Répertoire du système
        
    Returns:
        Liste des chemins vers les répertoires des agents
    """
    # Vérifier si c'est un système multi-agents avec un fichier system.yaml
    system_config = load_system_config(target_dir)
    if 'agents' in system_config:
        # Récupérer les noms des agents à partir de la configuration
        agent_names = [agent.get('name') for agent in system_config['agents']]
        
        # Chercher les répertoires correspondants
        agent_dirs = []
        for name in agent_names:
            if name:
                agent_dir = target_dir / name
                if agent_dir.exists() and agent_dir.is_dir():
                    agent_dirs.append(agent_dir)
        
        if agent_dirs:
            return agent_dirs
    
    # Si pas de configuration système ou pas de répertoires d'agents trouvés,
    # chercher les répertoires contenant un fichier agent.yaml
    return [
        d for d in target_dir.iterdir() 
        if d.is_dir() and (d / "agent.yaml").exists()
    ]

def get_agent_status(agent_dir: Path) -> Dict[str, Any]:
    """
    Récupère l'état d'exécution d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        
    Returns:
        Dictionnaire contenant l'état de l'agent
    """
    # Dans une implémentation réelle, cette fonction chargerait l'état
    # à partir d'un fichier de statut ou d'une API
    status_path = agent_dir / "status.json"
    if status_path.exists():
        try:
            with open(status_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de l'état de l'agent: {e}")
    
    # État par défaut si aucun fichier de statut n'est trouvé
    return {
        "status": "unknown",
        "last_active": None,
        "memory_usage": None,
        "active_flows": []
    }

def get_agent_info(agent_dir: Path) -> Dict[str, Any]:
    """
    Récupère toutes les informations sur un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        
    Returns:
        Dictionnaire contenant les informations sur l'agent
    """
    config = load_agent_config(agent_dir)
    status = get_agent_status(agent_dir)
    
    # Fusionner la configuration et l'état
    info = {**config, **status}
    
    # Ajouter le chemin du répertoire
    info["directory"] = str(agent_dir)
    
    return info

def get_all_agents_info(target_dir: Path, is_system: bool = False) -> Dict[str, Dict[str, Any]]:
    """
    Récupère les informations sur tous les agents.
    
    Args:
        target_dir: Répertoire cible
        is_system: Indique si la cible est un système multi-agents
        
    Returns:
        Dictionnaire contenant les informations sur tous les agents
    """
    if is_system:
        agent_dirs = get_agent_directories(target_dir)
    else:
        # Si ce n'est pas un système, considérer le répertoire cible comme un agent
        agent_dirs = [target_dir]
    
    agents_info = {}
    for agent_dir in agent_dirs:
        agent_info = get_agent_info(agent_dir)
        agent_name = agent_info.get('name', agent_dir.name)
        agents_info[agent_name] = agent_info
    
    return agents_info
