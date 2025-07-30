"""
Fournisseur de données pour la mémoire des agents.

Ce module contient les fonctions pour charger et traiter les données
de mémoire des agents, y compris les croyances, les faits et les contextes.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os
import datetime

def get_beliefs(agent_dir: Path, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Récupère les croyances d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Liste des croyances de l'agent
    """
    # Dans une implémentation réelle, cette fonction chargerait les croyances
    # à partir d'un fichier de sauvegarde ou d'une API
    
    beliefs_path = agent_dir / "memory" / "beliefs.json"
    if beliefs_path.exists():
        try:
            with open(beliefs_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des croyances: {e}")
    
    # Si aucun fichier de croyances n'est trouvé, retourner une liste vide
    return []

def get_facts(agent_dir: Path, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Récupère les faits d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Liste des faits de l'agent
    """
    # Dans une implémentation réelle, cette fonction chargerait les faits
    # à partir d'un fichier de sauvegarde ou d'une API
    
    facts_path = agent_dir / "memory" / "facts.json"
    if facts_path.exists():
        try:
            with open(facts_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des faits: {e}")
    
    # Si aucun fichier de faits n'est trouvé, retourner une liste vide
    return []

def get_contexts(agent_dir: Path, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Récupère les contextes logiques d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Liste des contextes de l'agent
    """
    # Dans une implémentation réelle, cette fonction chargerait les contextes
    # à partir d'un fichier de sauvegarde ou d'une API
    
    contexts_path = agent_dir / "memory" / "contexts.json"
    if contexts_path.exists():
        try:
            with open(contexts_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des contextes: {e}")
    
    # Si aucun fichier de contextes n'est trouvé, retourner une liste vide
    return []

def get_memory_stats(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère les statistiques de mémoire d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire contenant les statistiques de mémoire
    """
    # Récupérer les croyances, faits et contextes
    beliefs = get_beliefs(agent_dir, agent_name)
    facts = get_facts(agent_dir, agent_name)
    contexts = get_contexts(agent_dir, agent_name)
    
    # Calculer les statistiques
    stats = {
        "belief_count": len(beliefs),
        "fact_count": len(facts),
        "context_count": len(contexts),
        "total_memory_items": len(beliefs) + len(facts) + len(contexts)
    }
    
    # Calculer les statistiques de confiance pour les croyances
    if beliefs:
        confidence_values = [b.get("confidence", 0) for b in beliefs if "confidence" in b]
        if confidence_values:
            stats["avg_belief_confidence"] = sum(confidence_values) / len(confidence_values)
            stats["max_belief_confidence"] = max(confidence_values)
            stats["min_belief_confidence"] = min(confidence_values)
    
    return stats

def get_memory_history(agent_dir: Path, agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Récupère l'historique des modifications de la mémoire d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Liste des modifications de la mémoire
    """
    # Dans une implémentation réelle, cette fonction chargerait l'historique
    # à partir d'un fichier de sauvegarde ou d'une API
    
    history_path = agent_dir / "memory" / "history.json"
    if history_path.exists():
        try:
            with open(history_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de l'historique: {e}")
    
    # Si aucun fichier d'historique n'est trouvé, retourner une liste vide
    return []

def get_memory_usage(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère l'utilisation de la mémoire d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire contenant l'utilisation de la mémoire
    """
    # Dans une implémentation réelle, cette fonction calculerait l'utilisation
    # de la mémoire à partir des fichiers de sauvegarde ou d'une API
    
    # Récupérer les statistiques de mémoire
    stats = get_memory_stats(agent_dir, agent_name)
    
    # Calculer l'utilisation de la mémoire
    usage = {
        "total_items": stats.get("total_memory_items", 0),
        "last_updated": datetime.datetime.now().isoformat(),
        "memory_size_bytes": 0
    }
    
    # Calculer la taille des fichiers de mémoire
    memory_dir = agent_dir / "memory"
    if memory_dir.exists() and memory_dir.is_dir():
        total_size = 0
        for file_path in memory_dir.glob("**/*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        
        usage["memory_size_bytes"] = total_size
    
    return usage
