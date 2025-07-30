"""
Module de lancement d'agents pour le SDK Nüm Agents.

Ce module fournit des classes et fonctions pour exécuter des agents
et visualiser leur graphe logique en temps réel.
"""

import os
import sys
import json
import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import importlib.util

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

console = Console()


class AgentRunner:
    """
    Classe pour exécuter des agents et visualiser leur graphe logique en temps réel.
    
    Cette classe charge et exécute un agent à partir de son répertoire,
    avec des options pour la visualisation en temps réel du graphe logique
    et l'exportation des résultats.
    """
    
    def __init__(self, agent_dir: Path, verbose: bool = False):
        """
        Initialise le runner d'agent.
        
        Args:
            agent_dir: Répertoire de l'agent
            verbose: Afficher les informations détaillées pendant l'exécution
        """
        self.agent_dir = agent_dir
        self.verbose = verbose
        self.live_graph = False
        self.live_graph_thread = None
        self.stop_live_graph = False
        
        # Vérifier que le répertoire de l'agent existe
        if not agent_dir.exists() or not agent_dir.is_dir():
            raise ValueError(f"Le répertoire de l'agent n'existe pas : {agent_dir}")
            
        # Vérifier que le fichier main.py existe
        self.main_file = agent_dir / "main.py"
        if not self.main_file.exists():
            raise ValueError(f"Le fichier main.py n'existe pas dans {agent_dir}")
            
        # Vérifier que le fichier agent.yaml existe
        self.agent_spec_file = agent_dir / "agent.yaml"
        if not self.agent_spec_file.exists():
            raise ValueError(f"Le fichier agent.yaml n'existe pas dans {agent_dir}")
            
        # Charger les métadonnées de l'agent
        self._load_agent_metadata()
        
    def _load_agent_metadata(self):
        """
        Charge les métadonnées de l'agent à partir du fichier agent.yaml.
        """
        import yaml
        
        try:
            with open(self.agent_spec_file, "r") as f:
                self.agent_spec = yaml.safe_load(f)
                
            self.agent_name = self.agent_spec.get("agent", {}).get("name", "UnknownAgent")
            self.agent_description = self.agent_spec.get("agent", {}).get("description", "")
            
            if self.verbose:
                console.print(f"[bold blue]Agent:[/] {self.agent_name}")
                console.print(f"[bold blue]Description:[/] {self.agent_description}")
        except Exception as e:
            console.print(f"[bold red]Erreur lors du chargement des métadonnées de l'agent:[/] {str(e)}")
            raise
            
    def enable_live_graph(self):
        """
        Active la visualisation en temps réel du graphe logique.
        """
        self.live_graph = True
        
    def _start_live_graph_visualizer(self):
        """
        Démarre la visualisation en temps réel du graphe logique dans un thread séparé.
        """
        if not self.live_graph:
            return
            
        try:
            # Importer les modules nécessaires
            import matplotlib.pyplot as plt
            import networkx as nx
            from num_agents.graph.logical_graph import generate_logical_graph
            
            # Fonction pour mettre à jour le graphe en temps réel
            def update_graph():
                plt.ion()  # Mode interactif
                fig, ax = plt.subplots(figsize=(12, 8))
                plt.title(f"Graphe logique en temps réel - {self.agent_name}")
                
                while not self.stop_live_graph:
                    try:
                        # Générer le graphe logique
                        graph_data = generate_logical_graph(self.agent_dir, return_data=True)
                        G = nx.DiGraph()
                        
                        # Ajouter les nœuds
                        for node in graph_data.get("nodes", []):
                            G.add_node(node["id"], label=node.get("label", node["id"]), type=node.get("type", "unknown"))
                            
                        # Ajouter les arêtes
                        for edge in graph_data.get("edges", []):
                            G.add_edge(edge["source"], edge["target"], label=edge.get("label", ""))
                            
                        # Dessiner le graphe
                        ax.clear()
                        pos = nx.spring_layout(G)
                        nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, ax=ax)
                        
                        # Ajouter les étiquettes des arêtes
                        edge_labels = {(u, v): d["label"] for u, v, d in G.edges(data=True) if "label" in d}
                        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
                        
                        plt.draw()
                        plt.pause(2)  # Mettre à jour toutes les 2 secondes
                    except Exception as e:
                        if self.verbose:
                            console.print(f"[bold yellow]Erreur lors de la mise à jour du graphe:[/] {str(e)}")
                        time.sleep(2)
                        
                plt.close()
                
            # Démarrer le thread de visualisation
            self.stop_live_graph = False
            self.live_graph_thread = threading.Thread(target=update_graph)
            self.live_graph_thread.daemon = True
            self.live_graph_thread.start()
            
            console.print("[bold green]Visualisation du graphe logique en temps réel démarrée[/]")
        except ImportError:
            console.print("[bold yellow]Attention:[/] matplotlib ou networkx n'est pas installé. La visualisation en temps réel n'est pas disponible.")
            self.live_graph = False
        except Exception as e:
            console.print(f"[bold yellow]Erreur lors du démarrage de la visualisation:[/] {str(e)}")
            self.live_graph = False
            
    def _stop_live_graph_visualizer(self):
        """
        Arrête la visualisation en temps réel du graphe logique.
        """
        if self.live_graph_thread:
            self.stop_live_graph = True
            self.live_graph_thread.join(timeout=1)
            console.print("[bold green]Visualisation du graphe logique arrêtée[/]")
            
    def _load_input_data(self, input_file: Optional[str]) -> Dict[str, Any]:
        """
        Charge les données d'entrée à partir d'un fichier.
        
        Args:
            input_file: Chemin vers le fichier d'entrée
            
        Returns:
            Dictionnaire contenant les données d'entrée
        """
        if not input_file:
            return {}
            
        try:
            with open(input_file, "r") as f:
                if input_file.endswith(".json"):
                    return json.load(f)
                else:
                    return {"input_text": f.read()}
        except Exception as e:
            console.print(f"[bold red]Erreur lors du chargement des données d'entrée:[/] {str(e)}")
            return {}
            
    def _save_output_data(self, output_data: Any, output_file: Optional[str]):
        """
        Sauvegarde les données de sortie dans un fichier.
        
        Args:
            output_data: Données à sauvegarder
            output_file: Chemin vers le fichier de sortie
        """
        if not output_file:
            return
            
        try:
            with open(output_file, "w") as f:
                if output_file.endswith(".json"):
                    json.dump(output_data, f, indent=2)
                else:
                    f.write(str(output_data))
                    
            console.print(f"[bold green]Résultats sauvegardés dans[/] {output_file}")
        except Exception as e:
            console.print(f"[bold red]Erreur lors de la sauvegarde des résultats:[/] {str(e)}")
            
    def run(self, input_file: Optional[str] = None, output_file: Optional[str] = None) -> Any:
        """
        Exécute l'agent.
        
        Args:
            input_file: Chemin vers le fichier d'entrée
            output_file: Chemin vers le fichier de sortie
            
        Returns:
            Résultat de l'exécution de l'agent
        """
        # Charger les données d'entrée
        input_data = self._load_input_data(input_file)
        
        # Démarrer la visualisation en temps réel si activée
        if self.live_graph:
            self._start_live_graph_visualizer()
            
        try:
            # Ajouter le répertoire de l'agent au chemin de recherche Python
            sys.path.insert(0, str(self.agent_dir))
            
            # Charger dynamiquement le module main.py
            spec = importlib.util.spec_from_file_location("main", self.main_file)
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            
            # Vérifier si le module a une fonction run
            if hasattr(main_module, "run"):
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]Exécution de l'agent en cours...[/]"),
                    TimeElapsedColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task("Exécution", total=None)
                    
                    # Exécuter l'agent
                    result = main_module.run(input_data)
                    
                    progress.update(task, completed=True)
                    
                # Sauvegarder les résultats si nécessaire
                if output_file:
                    self._save_output_data(result, output_file)
                    
                return result
            else:
                console.print("[bold red]Erreur:[/] Le module main.py ne contient pas de fonction run()")
                return None
        except Exception as e:
            console.print(f"[bold red]Erreur lors de l'exécution de l'agent:[/] {str(e)}")
            return None
        finally:
            # Arrêter la visualisation en temps réel
            if self.live_graph:
                self._stop_live_graph_visualizer()
                
            # Restaurer le chemin de recherche Python
            if str(self.agent_dir) in sys.path:
                sys.path.remove(str(self.agent_dir))


def run_agent(agent_dir: Union[str, Path], **kwargs) -> Any:
    """
    Fonction utilitaire pour exécuter un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        **kwargs: Arguments supplémentaires pour le runner
        
    Returns:
        Résultat de l'exécution de l'agent
    """
    runner = AgentRunner(Path(agent_dir), **kwargs)
    return runner.run()
