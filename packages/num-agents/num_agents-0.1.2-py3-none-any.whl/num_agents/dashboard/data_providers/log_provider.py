"""
Fournisseur de données de journaux pour le tableau de bord.

Ce module fournit des fonctions pour récupérer et traiter les journaux
d'exécution d'un agent, y compris le filtrage et l'analyse des entrées de journal.
"""

from pathlib import Path
import os
import re
import json
from typing import Dict, List, Any, Optional, Union, Tuple
import datetime
import pandas as pd


class LogEntry:
    """
    Représente une entrée de journal structurée.
    """
    
    def __init__(
        self,
        timestamp: datetime.datetime,
        level: str,
        message: str,
        source: str = "",
        node: Optional[str] = None,
        execution_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialise une entrée de journal.
        
        Args:
            timestamp: Horodatage de l'entrée
            level: Niveau de journal (INFO, WARNING, ERROR, etc.)
            message: Message de journal
            source: Source du journal (nom du module)
            node: Nœud associé à l'entrée (si applicable)
            execution_id: ID d'exécution associé (si applicable)
            metadata: Métadonnées supplémentaires
        """
        self.timestamp = timestamp
        self.level = level
        self.message = message
        self.source = source
        self.node = node
        self.execution_id = execution_id
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convertit l'entrée en dictionnaire.
        
        Returns:
            Représentation dictionnaire de l'entrée
        """
        return {
            "timestamp": self.timestamp.isoformat(),
            "level": self.level,
            "message": self.message,
            "source": self.source,
            "node": self.node,
            "execution_id": self.execution_id,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LogEntry':
        """
        Crée une entrée de journal à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données de l'entrée
            
        Returns:
            Instance de LogEntry
        """
        try:
            timestamp = datetime.datetime.fromisoformat(data["timestamp"])
        except (ValueError, KeyError):
            timestamp = datetime.datetime.now()
        
        return cls(
            timestamp=timestamp,
            level=data.get("level", "INFO"),
            message=data.get("message", ""),
            source=data.get("source", ""),
            node=data.get("node"),
            execution_id=data.get("execution_id"),
            metadata=data.get("metadata", {})
        )
    
    @classmethod
    def from_line(cls, line: str) -> Optional['LogEntry']:
        """
        Analyse une ligne de journal texte et crée une entrée structurée.
        
        Args:
            line: Ligne de journal à analyser
            
        Returns:
            Instance de LogEntry ou None si la ligne n'est pas valide
        """
        # Format standard: YYYY-MM-DD HH:MM:SS,mmm LEVEL [SOURCE] MESSAGE
        pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}) ([A-Z]+) \[([^\]]+)\] (.+)'
        match = re.match(pattern, line)
        
        if match:
            try:
                timestamp_str, level, source, message = match.groups()
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                
                # Extraire le nœud et l'ID d'exécution s'ils sont présents dans le message
                node_match = re.search(r'node=([^\s,]+)', message)
                exec_id_match = re.search(r'execution_id=([^\s,]+)', message)
                
                node = node_match.group(1) if node_match else None
                execution_id = exec_id_match.group(1) if exec_id_match else None
                
                return cls(
                    timestamp=timestamp,
                    level=level,
                    message=message,
                    source=source,
                    node=node,
                    execution_id=execution_id
                )
            except Exception:
                pass
        
        # Format JSON
        try:
            data = json.loads(line)
            return cls.from_dict(data)
        except json.JSONDecodeError:
            pass
        
        # Format simple
        if line.strip():
            return cls(
                timestamp=datetime.datetime.now(),
                level="INFO",
                message=line.strip(),
                source="unknown"
            )
        
        return None


class LogProvider:
    """
    Classe pour récupérer et traiter les journaux d'un agent.
    """
    
    def __init__(self, agent_dir: Path):
        """
        Initialise le fournisseur de journaux.
        
        Args:
            agent_dir: Répertoire de l'agent
        """
        self.agent_dir = agent_dir
        self.logs_dir = agent_dir / "logs"
        self.cache = {}  # Cache pour éviter de relire les mêmes fichiers
    
    def get_log_files(self) -> List[Path]:
        """
        Récupère la liste des fichiers de journal disponibles.
        
        Returns:
            Liste des chemins vers les fichiers de journal
        """
        if not self.logs_dir.exists() or not self.logs_dir.is_dir():
            return []
        
        return sorted(
            self.logs_dir.glob("*.log"),
            key=lambda p: os.path.getmtime(p),
            reverse=True
        )
    
    def read_log_file(self, log_file: Path, use_cache: bool = True) -> List[LogEntry]:
        """
        Lit un fichier de journal et retourne les entrées structurées.
        
        Args:
            log_file: Chemin vers le fichier de journal
            use_cache: Utiliser le cache si disponible
            
        Returns:
            Liste d'entrées de journal
        """
        if not log_file.exists():
            return []
        
        # Vérifier le cache
        file_mtime = os.path.getmtime(log_file)
        cache_key = str(log_file)
        
        if use_cache and cache_key in self.cache:
            cached_mtime, entries = self.cache[cache_key]
            if cached_mtime == file_mtime:
                return entries
        
        # Lire le fichier
        entries = []
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                current_entry_lines = []
                
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Vérifier si c'est une nouvelle entrée
                    if re.match(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', line) or line.startswith('{'):
                        # Traiter l'entrée précédente s'il y en a une
                        if current_entry_lines:
                            entry_text = '\n'.join(current_entry_lines)
                            entry = LogEntry.from_line(entry_text)
                            if entry:
                                entries.append(entry)
                            current_entry_lines = []
                        
                        # Commencer une nouvelle entrée
                        current_entry_lines.append(line)
                    else:
                        # Continuer l'entrée actuelle
                        current_entry_lines.append(line)
                
                # Traiter la dernière entrée
                if current_entry_lines:
                    entry_text = '\n'.join(current_entry_lines)
                    entry = LogEntry.from_line(entry_text)
                    if entry:
                        entries.append(entry)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier de journal {log_file}: {e}")
        
        # Mettre à jour le cache
        self.cache[cache_key] = (file_mtime, entries)
        
        return entries
    
    def get_logs(
        self,
        max_entries: int = 1000,
        level_filter: Optional[List[str]] = None,
        source_filter: Optional[List[str]] = None,
        node_filter: Optional[List[str]] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
        search_text: Optional[str] = None
    ) -> List[LogEntry]:
        """
        Récupère les entrées de journal filtrées.
        
        Args:
            max_entries: Nombre maximum d'entrées à retourner
            level_filter: Filtrer par niveaux de journal
            source_filter: Filtrer par sources
            node_filter: Filtrer par nœuds
            start_time: Heure de début pour le filtrage
            end_time: Heure de fin pour le filtrage
            search_text: Texte à rechercher dans les messages
            
        Returns:
            Liste d'entrées de journal filtrées
        """
        log_files = self.get_log_files()
        all_entries = []
        
        for log_file in log_files:
            entries = self.read_log_file(log_file)
            all_entries.extend(entries)
            
            # Arrêter si on a assez d'entrées
            if len(all_entries) >= max_entries * 2:  # Facteur de sécurité pour le filtrage
                break
        
        # Appliquer les filtres
        filtered_entries = all_entries
        
        if level_filter:
            filtered_entries = [e for e in filtered_entries if e.level in level_filter]
        
        if source_filter:
            filtered_entries = [e for e in filtered_entries if e.source in source_filter]
        
        if node_filter:
            filtered_entries = [e for e in filtered_entries if e.node in node_filter]
        
        if start_time:
            filtered_entries = [e for e in filtered_entries if e.timestamp >= start_time]
        
        if end_time:
            filtered_entries = [e for e in filtered_entries if e.timestamp <= end_time]
        
        if search_text:
            search_text = search_text.lower()
            filtered_entries = [
                e for e in filtered_entries 
                if search_text in e.message.lower() or 
                   search_text in e.source.lower() or
                   (e.node and search_text in e.node.lower())
            ]
        
        # Trier par horodatage décroissant et limiter le nombre d'entrées
        filtered_entries.sort(key=lambda e: e.timestamp, reverse=True)
        return filtered_entries[:max_entries]
    
    def get_logs_dataframe(self, **kwargs) -> pd.DataFrame:
        """
        Récupère les entrées de journal sous forme de DataFrame pandas.
        
        Args:
            **kwargs: Arguments à passer à get_logs()
            
        Returns:
            DataFrame pandas contenant les entrées de journal
        """
        entries = self.get_logs(**kwargs)
        
        data = []
        for entry in entries:
            row = {
                "timestamp": entry.timestamp,
                "level": entry.level,
                "source": entry.source,
                "message": entry.message,
                "node": entry.node,
                "execution_id": entry.execution_id
            }
            data.append(row)
        
        return pd.DataFrame(data)
    
    def get_log_statistics(self) -> Dict[str, Any]:
        """
        Calcule des statistiques sur les journaux.
        
        Returns:
            Dictionnaire contenant diverses statistiques
        """
        log_files = self.get_log_files()
        
        if not log_files:
            return {
                "total_entries": 0,
                "first_entry": None,
                "last_entry": None,
                "level_counts": {},
                "source_counts": {},
                "node_counts": {}
            }
        
        # Lire tous les journaux
        all_entries = []
        for log_file in log_files:
            entries = self.read_log_file(log_file)
            all_entries.extend(entries)
        
        if not all_entries:
            return {
                "total_entries": 0,
                "first_entry": None,
                "last_entry": None,
                "level_counts": {},
                "source_counts": {},
                "node_counts": {}
            }
        
        # Trier par horodatage
        all_entries.sort(key=lambda e: e.timestamp)
        
        # Calculer les statistiques
        level_counts = {}
        source_counts = {}
        node_counts = {}
        
        for entry in all_entries:
            # Compter par niveau
            level_counts[entry.level] = level_counts.get(entry.level, 0) + 1
            
            # Compter par source
            source_counts[entry.source] = source_counts.get(entry.source, 0) + 1
            
            # Compter par nœud
            if entry.node:
                node_counts[entry.node] = node_counts.get(entry.node, 0) + 1
        
        return {
            "total_entries": len(all_entries),
            "first_entry": all_entries[0].timestamp if all_entries else None,
            "last_entry": all_entries[-1].timestamp if all_entries else None,
            "level_counts": level_counts,
            "source_counts": source_counts,
            "node_counts": node_counts
        }
    
    def export_logs(
        self,
        output_format: str = "csv",
        output_path: Optional[Path] = None,
        **filter_kwargs
    ) -> Union[str, Path]:
        """
        Exporte les journaux filtrés dans un format spécifié.
        
        Args:
            output_format: Format de sortie (csv, json, excel)
            output_path: Chemin de sortie (optionnel)
            **filter_kwargs: Arguments de filtrage à passer à get_logs()
            
        Returns:
            Chemin du fichier exporté ou contenu sous forme de chaîne
        """
        df = self.get_logs_dataframe(**filter_kwargs)
        
        # Convertir les horodatages en chaînes pour la sérialisation
        df['timestamp'] = df['timestamp'].apply(lambda x: x.isoformat() if x else None)
        
        if output_path is None:
            # Générer un nom de fichier par défaut
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"agent_logs_{timestamp}.{output_format}"
            output_path = self.agent_dir / "exports" / filename
            
            # Créer le répertoire d'exportation s'il n'existe pas
            output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Exporter dans le format demandé
        if output_format.lower() == "csv":
            df.to_csv(output_path, index=False, encoding='utf-8')
        elif output_format.lower() == "json":
            df.to_json(output_path, orient="records", date_format="iso")
        elif output_format.lower() == "excel":
            df.to_excel(output_path, index=False)
        else:
            # Format non supporté, retourner CSV comme chaîne
            return df.to_csv(index=False, encoding='utf-8')
        
        return output_path
