"""
Fournisseur de données pour les événements des agents.

Ce module contient les fonctions pour charger et traiter les événements
générés par les agents pendant leur exécution.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import json
import os
import datetime
import time
from collections import defaultdict

class EventProvider:
    """
    Fournisseur de données pour les événements des agents.
    
    Cette classe fournit des méthodes pour charger, filtrer et traiter
    les événements générés par les agents.
    """
    
    def __init__(self, agent_dir: Path):
        """
        Initialise le fournisseur d'événements.
        
        Args:
            agent_dir: Répertoire de l'agent
        """
        self.agent_dir = agent_dir
        self.events_dir = agent_dir / "events"
        self.cache = {}
        self.last_refresh = 0
        
    def get_events(self, 
                  start_time: Optional[Union[str, datetime.datetime]] = None,
                  end_time: Optional[Union[str, datetime.datetime]] = None,
                  event_types: Optional[List[str]] = None,
                  source_nodes: Optional[List[str]] = None,
                  limit: int = 1000,
                  refresh_cache: bool = False) -> List[Dict[str, Any]]:
        """
        Récupère les événements d'un agent avec filtrage.
        
        Args:
            start_time: Heure de début pour le filtrage (format ISO ou objet datetime)
            end_time: Heure de fin pour le filtrage (format ISO ou objet datetime)
            event_types: Liste des types d'événements à inclure
            source_nodes: Liste des nœuds sources à inclure
            limit: Nombre maximum d'événements à retourner
            refresh_cache: Force le rafraîchissement du cache
            
        Returns:
            Liste des événements filtrés
        """
        # Convertir les chaînes de date en objets datetime si nécessaire
        if isinstance(start_time, str):
            start_time = datetime.datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.datetime.fromisoformat(end_time)
            
        # Vérifier si nous devons rafraîchir le cache
        current_time = time.time()
        if refresh_cache or (current_time - self.last_refresh) > 5:  # Rafraîchir après 5 secondes
            self._load_events()
            self.last_refresh = current_time
            
        # Filtrer les événements
        filtered_events = self.cache.get("events", [])
        
        if start_time:
            filtered_events = [e for e in filtered_events if datetime.datetime.fromisoformat(e.get("timestamp", "")) >= start_time]
        if end_time:
            filtered_events = [e for e in filtered_events if datetime.datetime.fromisoformat(e.get("timestamp", "")) <= end_time]
        if event_types:
            filtered_events = [e for e in filtered_events if e.get("type") in event_types]
        if source_nodes:
            filtered_events = [e for e in filtered_events if e.get("source_node") in source_nodes]
            
        # Limiter le nombre d'événements
        return filtered_events[:limit]
    
    def get_event_types(self) -> List[str]:
        """
        Récupère la liste des types d'événements disponibles.
        
        Returns:
            Liste des types d'événements
        """
        events = self.get_events()
        return sorted(list(set(e.get("type") for e in events if "type" in e)))
    
    def get_source_nodes(self) -> List[str]:
        """
        Récupère la liste des nœuds sources disponibles.
        
        Returns:
            Liste des nœuds sources
        """
        events = self.get_events()
        return sorted(list(set(e.get("source_node") for e in events if "source_node" in e)))
    
    def get_event_timeline(self, 
                         interval: str = "minute",
                         event_types: Optional[List[str]] = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Génère une chronologie des événements regroupés par intervalle.
        
        Args:
            interval: Intervalle de regroupement ('second', 'minute', 'hour', 'day')
            event_types: Types d'événements à inclure
            
        Returns:
            Dictionnaire avec les intervalles de temps comme clés et les listes d'événements comme valeurs
        """
        events = self.get_events(event_types=event_types)
        timeline = defaultdict(list)
        
        for event in events:
            if "timestamp" not in event:
                continue
                
            dt = datetime.datetime.fromisoformat(event["timestamp"])
            
            if interval == "second":
                key = dt.strftime("%Y-%m-%d %H:%M:%S")
            elif interval == "minute":
                key = dt.strftime("%Y-%m-%d %H:%M:00")
            elif interval == "hour":
                key = dt.strftime("%Y-%m-%d %H:00:00")
            elif interval == "day":
                key = dt.strftime("%Y-%m-%d 00:00:00")
            else:
                key = dt.strftime("%Y-%m-%d %H:%M:%S")
                
            timeline[key].append(event)
            
        return dict(timeline)
    
    def get_event_stats(self) -> Dict[str, Any]:
        """
        Calcule des statistiques sur les événements.
        
        Returns:
            Dictionnaire contenant des statistiques sur les événements
        """
        events = self.get_events()
        
        if not events:
            return {
                "total_count": 0,
                "type_distribution": {},
                "source_distribution": {},
                "hourly_distribution": {},
                "first_event_time": None,
                "last_event_time": None
            }
        
        # Distributions
        type_dist = defaultdict(int)
        source_dist = defaultdict(int)
        hourly_dist = defaultdict(int)
        
        # Temps
        timestamps = []
        
        for event in events:
            # Type d'événement
            event_type = event.get("type", "unknown")
            type_dist[event_type] += 1
            
            # Source
            source = event.get("source_node", "unknown")
            source_dist[source] += 1
            
            # Timestamp
            if "timestamp" in event:
                dt = datetime.datetime.fromisoformat(event["timestamp"])
                timestamps.append(dt)
                hour = dt.hour
                hourly_dist[hour] += 1
        
        # Trier les timestamps
        timestamps.sort()
        
        return {
            "total_count": len(events),
            "type_distribution": dict(type_dist),
            "source_distribution": dict(source_dist),
            "hourly_distribution": dict(hourly_dist),
            "first_event_time": timestamps[0].isoformat() if timestamps else None,
            "last_event_time": timestamps[-1].isoformat() if timestamps else None
        }
    
    def export_events(self, 
                    output_format: str = "json",
                    output_path: Optional[Path] = None,
                    **filters) -> Path:
        """
        Exporte les événements dans un fichier.
        
        Args:
            output_format: Format de sortie ('json', 'csv')
            output_path: Chemin du fichier de sortie
            **filters: Filtres à appliquer aux événements
            
        Returns:
            Chemin du fichier exporté
        """
        events = self.get_events(**filters)
        
        if output_path is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.agent_dir / f"events_export_{timestamp}.{output_format}"
            
        if output_format == "json":
            with open(output_path, "w") as f:
                json.dump(events, f, indent=2)
        elif output_format == "csv":
            import csv
            
            # Déterminer les en-têtes
            headers = set()
            for event in events:
                headers.update(event.keys())
            headers = sorted(list(headers))
            
            with open(output_path, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=headers)
                writer.writeheader()
                for event in events:
                    writer.writerow(event)
        else:
            raise ValueError(f"Format de sortie non pris en charge : {output_format}")
            
        return output_path
    
    def _load_events(self) -> None:
        """
        Charge les événements à partir des fichiers.
        """
        events = []
        
        if not self.events_dir.exists():
            self.cache["events"] = []
            return
            
        # Charger tous les fichiers d'événements
        for file_path in self.events_dir.glob("*.json"):
            try:
                with open(file_path, "r") as f:
                    file_events = json.load(f)
                    
                # Si c'est une liste, étendre events
                if isinstance(file_events, list):
                    events.extend(file_events)
                # Si c'est un dictionnaire avec une clé 'events', étendre events
                elif isinstance(file_events, dict) and "events" in file_events:
                    events.extend(file_events["events"])
                # Si c'est un dictionnaire simple, l'ajouter comme un événement
                elif isinstance(file_events, dict):
                    events.append(file_events)
            except Exception as e:
                print(f"Erreur lors du chargement du fichier d'événements {file_path}: {e}")
                
        # Trier les événements par timestamp
        events.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
        
        self.cache["events"] = events
        
    def generate_sample_events(self, count: int = 100) -> None:
        """
        Génère des événements d'exemple pour la démonstration.
        
        Args:
            count: Nombre d'événements à générer
        """
        if not self.events_dir.exists():
            os.makedirs(self.events_dir)
            
        # Types d'événements
        event_types = [
            "node_start", "node_end", "message_sent", "message_received",
            "memory_access", "llm_call", "error", "warning", "info"
        ]
        
        # Nœuds sources
        source_nodes = [
            "ManagerGoalNode", "ToolAdapterNode", "MemoryNode", "LLMNode",
            "OutputFormatterNode", "InputParserNode", "ReasoningNode"
        ]
        
        # Générer des événements
        events = []
        now = datetime.datetime.now()
        
        for i in range(count):
            # Timestamp aléatoire dans les dernières 24 heures
            random_seconds = int(86400 * (i / count))
            timestamp = (now - datetime.timedelta(seconds=random_seconds)).isoformat()
            
            # Type d'événement aléatoire
            event_type = event_types[i % len(event_types)]
            
            # Nœud source aléatoire
            source_node = source_nodes[i % len(source_nodes)]
            
            # Données spécifiques au type d'événement
            data = {}
            if event_type == "llm_call":
                data = {
                    "model": "gemini-2.0-pro" if i % 3 == 0 else "gpt-4o",
                    "tokens_in": int(100 + (i * 10) % 500),
                    "tokens_out": int(50 + (i * 5) % 300),
                    "duration_ms": int(200 + (i * 20) % 2000)
                }
            elif event_type in ["error", "warning", "info"]:
                messages = [
                    "Traitement terminé avec succès",
                    "Erreur de connexion au service externe",
                    "Délai d'attente dépassé pour la requête",
                    "Format de données invalide",
                    "Réponse reçue du modèle LLM"
                ]
                data = {
                    "message": messages[i % len(messages)],
                    "code": i % 5 if event_type == "error" else None
                }
            elif event_type in ["node_start", "node_end"]:
                data = {
                    "node_id": f"node_{i % 10}",
                    "duration_ms": int(50 + (i * 5) % 500) if event_type == "node_end" else None
                }
                
            # Créer l'événement
            event = {
                "id": f"evt_{i}",
                "timestamp": timestamp,
                "type": event_type,
                "source_node": source_node,
                "data": data
            }
            
            events.append(event)
            
        # Sauvegarder les événements
        output_path = self.events_dir / "sample_events.json"
        with open(output_path, "w") as f:
            json.dump(events, f, indent=2)
            
        print(f"Événements d'exemple générés et sauvegardés dans {output_path}")
        
        # Mettre à jour le cache
        self._load_events()


def get_events(agent_dir: Path, **kwargs) -> List[Dict[str, Any]]:
    """
    Fonction utilitaire pour récupérer les événements d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        **kwargs: Arguments de filtrage
        
    Returns:
        Liste des événements filtrés
    """
    provider = EventProvider(agent_dir)
    return provider.get_events(**kwargs)


def generate_sample_events(agent_dir: Path, count: int = 100) -> None:
    """
    Fonction utilitaire pour générer des événements d'exemple.
    
    Args:
        agent_dir: Répertoire de l'agent
        count: Nombre d'événements à générer
    """
    provider = EventProvider(agent_dir)
    provider.generate_sample_events(count)
