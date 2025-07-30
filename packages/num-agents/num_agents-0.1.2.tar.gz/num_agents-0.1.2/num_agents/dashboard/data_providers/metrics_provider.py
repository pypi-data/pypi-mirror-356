"""
Fournisseur de données pour les métriques des agents.

Ce module contient les fonctions pour charger et traiter les métriques
de performance et d'utilisation des agents.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os
import datetime
import time

def get_performance_metrics(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère les métriques de performance d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire contenant les métriques de performance
    """
    # Dans une implémentation réelle, cette fonction chargerait les métriques
    # à partir d'un fichier de sauvegarde ou d'une API
    
    metrics_path = agent_dir / "metrics" / "performance.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des métriques de performance: {e}")
    
    # Si aucun fichier de métriques n'est trouvé, retourner un dictionnaire vide
    return {}

def get_usage_metrics(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère les métriques d'utilisation d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire contenant les métriques d'utilisation
    """
    # Dans une implémentation réelle, cette fonction chargerait les métriques
    # à partir d'un fichier de sauvegarde ou d'une API
    
    metrics_path = agent_dir / "metrics" / "usage.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des métriques d'utilisation: {e}")
    
    # Si aucun fichier de métriques n'est trouvé, retourner un dictionnaire vide
    return {}

def get_llm_metrics(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère les métriques d'utilisation des modèles LLM d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire contenant les métriques d'utilisation des modèles LLM
    """
    # Dans une implémentation réelle, cette fonction chargerait les métriques
    # à partir d'un fichier de sauvegarde ou d'une API
    
    metrics_path = agent_dir / "metrics" / "llm.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des métriques LLM: {e}")
    
    # Si aucun fichier de métriques n'est trouvé, retourner un dictionnaire vide
    return {}

def get_metrics_history(agent_dir: Path, metric_type: str, timeframe: str = "day", agent_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Récupère l'historique des métriques d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        metric_type: Type de métrique (performance, usage, llm)
        timeframe: Période de temps (hour, day, week, month)
        agent_name: Nom de l'agent
        
    Returns:
        Liste des métriques historiques
    """
    # Dans une implémentation réelle, cette fonction chargerait l'historique
    # à partir d'un fichier de sauvegarde ou d'une API
    
    history_path = agent_dir / "metrics" / f"{metric_type}_history.json"
    if history_path.exists():
        try:
            with open(history_path, 'r') as f:
                history = json.load(f)
            
            # Filtrer l'historique en fonction de la période de temps
            now = time.time()
            if timeframe == "hour":
                cutoff = now - 3600  # 1 heure
            elif timeframe == "day":
                cutoff = now - 86400  # 1 jour
            elif timeframe == "week":
                cutoff = now - 604800  # 1 semaine
            elif timeframe == "month":
                cutoff = now - 2592000  # 30 jours
            else:
                cutoff = 0
            
            return [
                entry for entry in history
                if "timestamp" in entry and entry["timestamp"] >= cutoff
            ]
        except Exception as e:
            print(f"Erreur lors du chargement de l'historique des métriques: {e}")
    
    # Si aucun fichier d'historique n'est trouvé, retourner une liste vide
    return []

def get_system_metrics(system_dir: Path) -> Dict[str, Any]:
    """
    Récupère les métriques d'un système multi-agents.
    
    Args:
        system_dir: Répertoire du système
        
    Returns:
        Dictionnaire contenant les métriques du système
    """
    # Dans une implémentation réelle, cette fonction chargerait les métriques
    # à partir d'un fichier de sauvegarde ou d'une API
    
    metrics_path = system_dir / "metrics" / "system.json"
    if metrics_path.exists():
        try:
            with open(metrics_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des métriques du système: {e}")
    
    # Si aucun fichier de métriques n'est trouvé, retourner un dictionnaire vide
    return {}

def generate_sample_metrics(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Génère des métriques d'exemple pour un agent.
    Utile pour les démonstrations et les tests.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire contenant les métriques générées
    """
    import random
    
    # Générer des métriques de performance
    performance = {
        "response_time": {
            "avg": random.uniform(0.5, 2.0),
            "min": random.uniform(0.1, 0.5),
            "max": random.uniform(2.0, 5.0),
            "p90": random.uniform(1.5, 3.0),
            "p99": random.uniform(3.0, 4.5)
        },
        "success_rate": random.uniform(0.9, 1.0),
        "error_rate": random.uniform(0.0, 0.1),
        "throughput": random.randint(10, 100)
    }
    
    # Générer des métriques d'utilisation
    usage = {
        "requests": {
            "total": random.randint(100, 1000),
            "per_hour": random.randint(5, 50)
        },
        "memory_usage": {
            "current_mb": random.uniform(50, 200),
            "peak_mb": random.uniform(100, 300)
        },
        "cpu_usage": {
            "current_percent": random.uniform(5, 30),
            "peak_percent": random.uniform(20, 80)
        }
    }
    
    # Générer des métriques LLM
    llm = {
        "tokens": {
            "input": random.randint(1000, 10000),
            "output": random.randint(500, 5000),
            "total": random.randint(1500, 15000)
        },
        "cost": {
            "total": random.uniform(0.1, 5.0),
            "per_request": random.uniform(0.01, 0.1)
        },
        "models": {
            "gemini-2.0-pro": {
                "usage": random.uniform(0.6, 0.8),
                "tokens": random.randint(1000, 8000)
            },
            "gemini-2.0-flash": {
                "usage": random.uniform(0.1, 0.3),
                "tokens": random.randint(500, 4000)
            },
            "gemini-1.5-flash": {
                "usage": random.uniform(0.05, 0.15),
                "tokens": random.randint(200, 2000)
            }
        }
    }
    
    # Générer l'historique des métriques
    now = time.time()
    performance_history = []
    usage_history = []
    llm_history = []
    
    # Générer des données pour les dernières 24 heures
    for i in range(24):
        timestamp = now - i * 3600  # Chaque heure
        
        # Métriques de performance pour cette heure
        perf_entry = {
            "timestamp": timestamp,
            "response_time_avg": random.uniform(0.5, 2.0),
            "success_rate": random.uniform(0.9, 1.0),
            "error_rate": random.uniform(0.0, 0.1),
            "throughput": random.randint(10, 100)
        }
        performance_history.append(perf_entry)
        
        # Métriques d'utilisation pour cette heure
        usage_entry = {
            "timestamp": timestamp,
            "requests": random.randint(5, 50),
            "memory_usage_mb": random.uniform(50, 200),
            "cpu_usage_percent": random.uniform(5, 30)
        }
        usage_history.append(usage_entry)
        
        # Métriques LLM pour cette heure
        llm_entry = {
            "timestamp": timestamp,
            "input_tokens": random.randint(100, 1000),
            "output_tokens": random.randint(50, 500),
            "cost": random.uniform(0.01, 0.5)
        }
        llm_history.append(llm_entry)
    
    # Créer les répertoires nécessaires
    metrics_dir = agent_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    
    # Enregistrer les métriques générées
    try:
        with open(metrics_dir / "performance.json", 'w') as f:
            json.dump(performance, f, indent=2)
        
        with open(metrics_dir / "usage.json", 'w') as f:
            json.dump(usage, f, indent=2)
        
        with open(metrics_dir / "llm.json", 'w') as f:
            json.dump(llm, f, indent=2)
        
        with open(metrics_dir / "performance_history.json", 'w') as f:
            json.dump(performance_history, f, indent=2)
        
        with open(metrics_dir / "usage_history.json", 'w') as f:
            json.dump(usage_history, f, indent=2)
        
        with open(metrics_dir / "llm_history.json", 'w') as f:
            json.dump(llm_history, f, indent=2)
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des métriques générées: {e}")
    
    return {
        "performance": performance,
        "usage": usage,
        "llm": llm,
        "performance_history": performance_history,
        "usage_history": usage_history,
        "llm_history": llm_history
    }
