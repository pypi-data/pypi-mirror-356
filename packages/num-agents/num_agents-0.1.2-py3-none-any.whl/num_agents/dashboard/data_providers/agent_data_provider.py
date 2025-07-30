"""
Fournisseur de données d'agent pour le tableau de bord.

Ce module fournit des fonctions pour récupérer et traiter les données
générales d'un agent, y compris sa configuration, son état et ses métadonnées.
"""

from pathlib import Path
import os
import json
import yaml
from typing import Dict, List, Any, Optional, Tuple
import datetime

class AgentDataProvider:
    """
    Classe pour récupérer et traiter les données d'un agent.
    """
    
    def __init__(self, agent_dir: Path):
        """
        Initialise le fournisseur de données d'agent.
        
        Args:
            agent_dir: Répertoire de l'agent
        """
        self.agent_dir = agent_dir
        self.agent_config = None
        self.agent_state = None
        self._load_agent_data()
    
    def _load_agent_data(self) -> None:
        """
        Charge les données de configuration et d'état de l'agent.
        """
        # Charger la configuration de l'agent (agent.yaml)
        config_path = self.agent_dir / "agent.yaml"
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.agent_config = yaml.safe_load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de la configuration de l'agent: {e}")
        
        # Charger l'état de l'agent (state.json s'il existe)
        state_path = self.agent_dir / "state.json"
        if state_path.exists():
            try:
                with open(state_path, 'r', encoding='utf-8') as f:
                    self.agent_state = json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de l'état de l'agent: {e}")
    
    def get_agent_name(self) -> str:
        """
        Récupère le nom de l'agent.
        
        Returns:
            Nom de l'agent ou nom du répertoire si non disponible
        """
        if self.agent_config and 'agent' in self.agent_config and 'name' in self.agent_config['agent']:
            return self.agent_config['agent']['name']
        return self.agent_dir.name
    
    def get_agent_description(self) -> str:
        """
        Récupère la description de l'agent.
        
        Returns:
            Description de l'agent ou chaîne vide si non disponible
        """
        if self.agent_config and 'agent' in self.agent_config and 'description' in self.agent_config['agent']:
            return self.agent_config['agent']['description']
        return ""
    
    def get_agent_univers(self) -> List[str]:
        """
        Récupère la liste des univers utilisés par l'agent.
        
        Returns:
            Liste des univers ou liste vide si non disponible
        """
        if self.agent_config and 'agent' in self.agent_config and 'univers' in self.agent_config['agent']:
            return self.agent_config['agent']['univers']
        return []
    
    def get_agent_llm(self) -> str:
        """
        Récupère le modèle LLM utilisé par l'agent.
        
        Returns:
            Nom du modèle LLM ou chaîne vide si non disponible
        """
        if self.agent_config and 'agent' in self.agent_config and 'llm' in self.agent_config['agent']:
            return self.agent_config['agent']['llm']
        return ""
    
    def get_agent_features(self) -> Dict[str, bool]:
        """
        Récupère les fonctionnalités activées pour l'agent.
        
        Returns:
            Dictionnaire des fonctionnalités et leur état
        """
        features = {}
        if self.agent_config and 'agent' in self.agent_config:
            for feature in ['memory', 'eventbus', 'scheduler', 'metrics', 'tracing']:
                features[feature] = self.agent_config['agent'].get(feature, False)
        return features
    
    def get_agent_nodes(self) -> List[str]:
        """
        Récupère la liste des nœuds de l'agent.
        
        Returns:
            Liste des noms de nœuds ou liste vide si non disponible
        """
        nodes_dir = self.agent_dir / "nodes"
        if not nodes_dir.exists() or not nodes_dir.is_dir():
            return []
        
        nodes = []
        for file in nodes_dir.glob("*.py"):
            if file.name != "__init__.py":
                nodes.append(file.stem)
        return nodes
    
    def get_agent_creation_time(self) -> Optional[datetime.datetime]:
        """
        Récupère la date de création de l'agent.
        
        Returns:
            Date de création ou None si non disponible
        """
        try:
            # Utiliser la date de création du répertoire de l'agent comme approximation
            creation_time = os.path.getctime(self.agent_dir)
            return datetime.datetime.fromtimestamp(creation_time)
        except Exception:
            return None
    
    def get_agent_last_run_time(self) -> Optional[datetime.datetime]:
        """
        Récupère la date de dernière exécution de l'agent.
        
        Returns:
            Date de dernière exécution ou None si non disponible
        """
        if self.agent_state and 'last_run' in self.agent_state:
            try:
                return datetime.datetime.fromisoformat(self.agent_state['last_run'])
            except (ValueError, TypeError):
                pass
        
        # Fallback: vérifier les fichiers de log
        logs_dir = self.agent_dir / "logs"
        if logs_dir.exists() and logs_dir.is_dir():
            log_files = list(logs_dir.glob("*.log"))
            if log_files:
                latest_log = max(log_files, key=os.path.getmtime)
                return datetime.datetime.fromtimestamp(os.path.getmtime(latest_log))
        
        return None
    
    def get_agent_status(self) -> str:
        """
        Récupère l'état actuel de l'agent.
        
        Returns:
            État de l'agent (actif, inactif, erreur)
        """
        if self.agent_state and 'status' in self.agent_state:
            return self.agent_state['status']
        
        # Vérifier les processus actifs (implémentation simplifiée)
        pid_file = self.agent_dir / "agent.pid"
        if pid_file.exists():
            return "actif"
        
        return "inactif"
    
    def get_agent_summary(self) -> Dict[str, Any]:
        """
        Récupère un résumé des informations de l'agent.
        
        Returns:
            Dictionnaire contenant les informations résumées de l'agent
        """
        return {
            "name": self.get_agent_name(),
            "description": self.get_agent_description(),
            "univers": self.get_agent_univers(),
            "llm": self.get_agent_llm(),
            "features": self.get_agent_features(),
            "nodes": self.get_agent_nodes(),
            "creation_time": self.get_agent_creation_time(),
            "last_run": self.get_agent_last_run_time(),
            "status": self.get_agent_status()
        }
    
    def update_agent_config(self, updated_config: Dict[str, Any]) -> bool:
        """
        Met à jour la configuration de l'agent.
        
        Args:
            updated_config: Nouvelle configuration
            
        Returns:
            True si la mise à jour a réussi, False sinon
        """
        config_path = self.agent_dir / "agent.yaml"
        try:
            # Sauvegarder une copie de la configuration actuelle
            if config_path.exists():
                backup_path = self.agent_dir / f"agent.yaml.bak.{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                with open(config_path, 'r', encoding='utf-8') as src, open(backup_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            # Écrire la nouvelle configuration
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(updated_config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            
            # Recharger la configuration
            self._load_agent_data()
            return True
        except Exception as e:
            print(f"Erreur lors de la mise à jour de la configuration: {e}")
            return False


def get_available_agents(base_dir: Path) -> List[Tuple[str, Path]]:
    """
    Récupère la liste des agents disponibles dans un répertoire.
    
    Args:
        base_dir: Répertoire de base à scanner
        
    Returns:
        Liste de tuples (nom_agent, chemin_agent)
    """
    agents = []
    
    # Vérifier si le répertoire est un agent
    if (base_dir / "agent.yaml").exists():
        try:
            provider = AgentDataProvider(base_dir)
            agents.append((provider.get_agent_name(), base_dir))
        except Exception:
            # Si erreur, utiliser le nom du répertoire
            agents.append((base_dir.name, base_dir))
    
    # Scanner les sous-répertoires pour d'autres agents
    for subdir in base_dir.iterdir():
        if subdir.is_dir() and (subdir / "agent.yaml").exists():
            try:
                provider = AgentDataProvider(subdir)
                agents.append((provider.get_agent_name(), subdir))
            except Exception:
                # Si erreur, utiliser le nom du répertoire
                agents.append((subdir.name, subdir))
    
    return agents
