"""
Fournisseur de données pour les traces d'exécution des agents.

Ce module contient les fonctions pour charger et traiter les journaux,
événements et erreurs des agents.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os
import datetime
import re

def get_execution_logs(agent_dir: Path, agent_name: Optional[str] = None, 
                      log_level: Optional[str] = None, 
                      component: Optional[str] = None,
                      limit: int = 100) -> List[Dict[str, Any]]:
    """
    Récupère les journaux d'exécution d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        log_level: Niveau de journal à filtrer (INFO, DEBUG, WARNING, ERROR)
        component: Composant à filtrer
        limit: Nombre maximum de journaux à récupérer
        
    Returns:
        Liste des journaux d'exécution
    """
    # Dans une implémentation réelle, cette fonction chargerait les journaux
    # à partir d'un fichier de journal ou d'une API
    
    logs_path = agent_dir / "logs" / "execution.log"
    logs = []
    
    if logs_path.exists():
        try:
            # Lire le fichier journal
            with open(logs_path, 'r') as f:
                log_lines = f.readlines()
            
            # Analyser chaque ligne de journal
            for line in log_lines[-limit:]:  # Limiter au nombre de lignes spécifié
                # Exemple de format de journal: "2023-06-19 15:30:45 [INFO] [Core] Message"
                match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(\w+)\] \[(\w+)\] (.*)', line)
                if match:
                    timestamp_str, level, comp, message = match.groups()
                    
                    # Filtrer par niveau de journal si spécifié
                    if log_level and level != log_level:
                        continue
                    
                    # Filtrer par composant si spécifié
                    if component and comp != component:
                        continue
                    
                    # Convertir la chaîne de timestamp en objet datetime
                    try:
                        timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        timestamp = datetime.datetime.now()
                    
                    logs.append({
                        "timestamp": timestamp,
                        "level": level,
                        "component": comp,
                        "message": message.strip()
                    })
        except Exception as e:
            print(f"Erreur lors du chargement des journaux d'exécution: {e}")
    
    # Trier les journaux par timestamp (du plus récent au plus ancien)
    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return logs

def get_events(agent_dir: Path, agent_name: Optional[str] = None,
              event_type: Optional[str] = None,
              limit: int = 100) -> List[Dict[str, Any]]:
    """
    Récupère les événements d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        event_type: Type d'événement à filtrer
        limit: Nombre maximum d'événements à récupérer
        
    Returns:
        Liste des événements
    """
    # Dans une implémentation réelle, cette fonction chargerait les événements
    # à partir d'un fichier de sauvegarde ou d'une API
    
    events_path = agent_dir / "logs" / "events.json"
    if events_path.exists():
        try:
            with open(events_path, 'r') as f:
                events = json.load(f)
            
            # Filtrer par type d'événement si spécifié
            if event_type:
                events = [evt for evt in events if evt.get("type") == event_type]
            
            # Trier les événements par timestamp (du plus récent au plus ancien)
            events.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            
            # Limiter le nombre d'événements
            return events[:limit]
        except Exception as e:
            print(f"Erreur lors du chargement des événements: {e}")
    
    # Si aucun fichier d'événements n'est trouvé, retourner une liste vide
    return []

def get_errors(agent_dir: Path, agent_name: Optional[str] = None,
              component: Optional[str] = None,
              include_resolved: bool = True,
              limit: int = 100) -> List[Dict[str, Any]]:
    """
    Récupère les erreurs d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        component: Composant à filtrer
        include_resolved: Inclure les erreurs résolues
        limit: Nombre maximum d'erreurs à récupérer
        
    Returns:
        Liste des erreurs
    """
    # Dans une implémentation réelle, cette fonction chargerait les erreurs
    # à partir d'un fichier de sauvegarde ou d'une API
    
    errors_path = agent_dir / "logs" / "errors.json"
    if errors_path.exists():
        try:
            with open(errors_path, 'r') as f:
                errors = json.load(f)
            
            # Filtrer par composant si spécifié
            if component:
                errors = [err for err in errors if err.get("component") == component]
            
            # Filtrer les erreurs résolues si nécessaire
            if not include_resolved:
                errors = [err for err in errors if not err.get("resolved", False)]
            
            # Trier les erreurs par timestamp (du plus récent au plus ancien)
            errors.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
            
            # Limiter le nombre d'erreurs
            return errors[:limit]
        except Exception as e:
            print(f"Erreur lors du chargement des erreurs: {e}")
    
    # Si aucun fichier d'erreurs n'est trouvé, retourner une liste vide
    return []

def generate_sample_traces(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Génère des traces d'exemple pour un agent.
    Utile pour les démonstrations et les tests.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire contenant les traces générées
    """
    import random
    
    # Créer les répertoires nécessaires
    logs_dir = agent_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    
    # Générer des journaux d'exécution
    now = datetime.datetime.now()
    log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
    log_components = ["Core", "LLM", "Memory", "Reasoning", "EventBus", "Scheduler"]
    
    logs = []
    for i in range(100):  # Générer 100 entrées de journal
        # Générer un timestamp pour les dernières 24 heures
        timestamp = now - datetime.timedelta(minutes=i * 15)
        
        # Générer un niveau de journal aléatoire, avec une probabilité plus élevée pour INFO et DEBUG
        level_weights = [0.6, 0.3, 0.08, 0.02]  # INFO, DEBUG, WARNING, ERROR
        level = random.choices(log_levels, weights=level_weights)[0]
        
        # Générer un composant aléatoire
        component = random.choice(log_components)
        
        # Générer un message de journal
        if level == "INFO":
            message = random.choice([
                "Traitement de la requête utilisateur terminé",
                "Modèle LLM appelé avec succès",
                "Croyance mise à jour dans la mémoire",
                "Événement publié sur le bus d'événements",
                "Tâche planifiée exécutée"
            ])
        elif level == "DEBUG":
            message = random.choice([
                "Entrée LLM: 'Quelle est la capitale de la France?'",
                "Sortie LLM: 'La capitale de la France est Paris.'",
                "Temps de traitement: 1.23s",
                "Contexte logique initialisé",
                "Nœud de raisonnement activé"
            ])
        elif level == "WARNING":
            message = random.choice([
                "Temps de réponse LLM supérieur au seuil",
                "Croyance contradictoire détectée",
                "Tentative de reconnexion au service externe",
                "Mémoire tampon presque pleine",
                "Tâche planifiée retardée"
            ])
        else:  # ERROR
            message = random.choice([
                "Échec de l'appel au modèle LLM",
                "Exception lors du traitement de la requête",
                "Échec de la mise à jour de la mémoire",
                "Erreur de publication d'événement",
                "Tâche planifiée échouée"
            ])
        
        # Formater la ligne de journal
        log_line = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} [{level}] [{component}] {message}\n"
        logs.append(log_line)
    
    # Écrire les journaux dans un fichier
    try:
        with open(logs_dir / "execution.log", 'w') as f:
            f.writelines(logs)
    except Exception as e:
        print(f"Erreur lors de l'écriture des journaux d'exécution: {e}")
    
    # Générer des événements
    events = []
    event_types = [
        "user_input", "llm_request", "llm_response", 
        "memory_update", "belief_revision", "task_scheduled",
        "task_executed", "system_notification"
    ]
    
    for i in range(50):  # Générer 50 événements
        # Générer un timestamp pour les dernières 24 heures
        timestamp = now - datetime.timedelta(minutes=i * 30)
        
        # Générer un type d'événement aléatoire
        event_type = random.choice(event_types)
        
        # Générer un contenu d'événement en fonction du type
        if event_type == "user_input":
            content = {
                "input": random.choice([
                    "Quelle est la capitale de la France?",
                    "Comment fonctionne un moteur à combustion?",
                    "Peux-tu me résumer ce document?",
                    "Quels sont les effets du réchauffement climatique?"
                ])
            }
        elif event_type == "llm_request":
            content = {
                "model": random.choice(["gemini-2.0-pro", "gemini-2.0-flash", "gemini-1.5-flash"]),
                "prompt": "Générer une réponse à la question de l'utilisateur...",
                "max_tokens": random.choice([100, 200, 500, 1000])
            }
        elif event_type == "llm_response":
            content = {
                "model": random.choice(["gemini-2.0-pro", "gemini-2.0-flash", "gemini-1.5-flash"]),
                "tokens_used": random.randint(50, 500),
                "response_time": random.uniform(0.5, 3.0)
            }
        elif event_type == "memory_update":
            content = {
                "key": f"fact_{random.randint(1, 100)}",
                "value": random.choice([
                    "Paris est la capitale de la France",
                    "L'eau bout à 100 degrés Celsius",
                    "La Terre tourne autour du Soleil"
                ])
            }
        elif event_type == "belief_revision":
            content = {
                "proposition_id": f"p{random.randint(1, 10)}",
                "old_confidence": random.uniform(0.5, 0.9),
                "new_confidence": random.uniform(0.5, 0.9),
                "reason": "Nouvelle information reçue"
            }
        elif event_type == "task_scheduled":
            content = {
                "task_id": f"task_{random.randint(1, 100)}",
                "scheduled_time": (timestamp + datetime.timedelta(minutes=random.randint(1, 30))).strftime("%H:%M:%S"),
                "priority": random.choice(["high", "medium", "low"])
            }
        elif event_type == "task_executed":
            content = {
                "task_id": f"task_{random.randint(1, 100)}",
                "execution_time": random.uniform(0.1, 2.0),
                "status": random.choice(["success", "partial_success", "failure"])
            }
        else:  # system_notification
            content = {
                "type": random.choice(["info", "warning", "error"]),
                "message": random.choice([
                    "Service démarré",
                    "Connexion établie",
                    "Mémoire faible",
                    "Erreur de connexion"
                ])
            }
        
        events.append({
            "id": f"evt_{i}",
            "timestamp": timestamp.timestamp(),
            "type": event_type,
            "content": content
        })
    
    # Écrire les événements dans un fichier
    try:
        with open(logs_dir / "events.json", 'w') as f:
            json.dump(events, f, indent=2)
    except Exception as e:
        print(f"Erreur lors de l'écriture des événements: {e}")
    
    # Générer des erreurs
    errors = []
    error_types = ["LLMError", "MemoryError", "EventBusError", "SchedulerError", "NetworkError"]
    
    for i in range(10):  # Générer 10 erreurs
        # Générer un timestamp pour les dernières 24 heures
        timestamp = now - datetime.timedelta(hours=random.randint(1, 24))
        
        # Générer un type d'erreur aléatoire
        error_type = random.choice(error_types)
        
        # Générer un message d'erreur en fonction du type
        if error_type == "LLMError":
            message = random.choice([
                "Échec de la connexion au service LLM",
                "Timeout lors de l'appel au modèle",
                "Réponse invalide du modèle",
                "Quota d'API dépassé"
            ])
            component = "LLM"
        elif error_type == "MemoryError":
            message = random.choice([
                "Échec de l'écriture en mémoire",
                "Incohérence détectée dans la base de croyances",
                "Échec de la récupération du contexte"
            ])
            component = "Memory"
        elif error_type == "EventBusError":
            message = random.choice([
                "Échec de la publication d'événement",
                "Abonnement invalide",
                "Boucle d'événements détectée"
            ])
            component = "EventBus"
        elif error_type == "SchedulerError":
            message = random.choice([
                "Échec de la planification de tâche",
                "Tâche expirée",
                "Conflit de planification détecté"
            ])
            component = "Scheduler"
        else:  # NetworkError
            message = random.choice([
                "Échec de la connexion au service externe",
                "Timeout réseau",
                "Erreur DNS"
            ])
            component = "Network"
        
        # Générer une trace d'erreur
        trace = f"Traceback (most recent call last):\n"
        trace += f"  File \"num_agents/{component.lower()}/core.py\", line {random.randint(10, 500)}, in process_request\n"
        trace += f"    result = self._handle_{component.lower()}_operation(request)\n"
        trace += f"  File \"num_agents/{component.lower()}/operations.py\", line {random.randint(10, 300)}, in _handle_{component.lower()}_operation\n"
        trace += f"    response = self._execute_operation(request)\n"
        trace += f"  File \"num_agents/{component.lower()}/operations.py\", line {random.randint(10, 300)}, in _execute_operation\n"
        trace += f"    return self._client.execute(request)\n"
        trace += f"  File \"num_agents/core/client.py\", line {random.randint(10, 200)}, in execute\n"
        trace += f"    response = self._send_request(request)\n"
        trace += f"{error_type}: {message}"
        
        errors.append({
            "id": f"err_{i}",
            "timestamp": timestamp.timestamp(),
            "type": error_type,
            "message": message,
            "component": component,
            "trace": trace,
            "resolved": random.choice([True, False])
        })
    
    # Écrire les erreurs dans un fichier
    try:
        with open(logs_dir / "errors.json", 'w') as f:
            json.dump(errors, f, indent=2)
    except Exception as e:
        print(f"Erreur lors de l'écriture des erreurs: {e}")
    
    return {
        "logs": logs,
        "events": events,
        "errors": errors
    }
