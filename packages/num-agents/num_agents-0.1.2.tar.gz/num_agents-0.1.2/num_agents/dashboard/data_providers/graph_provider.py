"""
Fournisseur de données pour les graphes logiques.

Ce module contient les fonctions pour charger et traiter les graphes
de flux, de dépendances et d'inférence des agents.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os
import importlib
import inspect

def get_flow_graph(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère le graphe de flux d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire représentant le graphe de flux
    """
    # Dans une implémentation réelle, cette fonction analyserait le code de l'agent
    # pour générer le graphe de flux, ou chargerait un graphe pré-généré
    
    # Vérifier si un graphe pré-généré existe
    graph_path = agent_dir / "flow_graph.json"
    if graph_path.exists():
        try:
            with open(graph_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement du graphe de flux: {e}")
    
    # Si aucun graphe pré-généré n'est trouvé, générer un graphe vide
    return {
        "nodes": [],
        "edges": []
    }

def get_dependency_graph(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère le graphe de dépendances d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire représentant le graphe de dépendances
    """
    # Dans une implémentation réelle, cette fonction analyserait le code de l'agent
    # pour générer le graphe de dépendances, ou chargerait un graphe pré-généré
    
    # Vérifier si un graphe pré-généré existe
    graph_path = agent_dir / "dependency_graph.json"
    if graph_path.exists():
        try:
            with open(graph_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement du graphe de dépendances: {e}")
    
    # Si aucun graphe pré-généré n'est trouvé, générer un graphe vide
    return {
        "nodes": [],
        "edges": []
    }

def get_inference_graph(agent_dir: Path, agent_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Récupère le graphe d'inférence d'un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
        agent_name: Nom de l'agent
        
    Returns:
        Dictionnaire représentant le graphe d'inférence
    """
    # Dans une implémentation réelle, cette fonction analyserait l'état de l'agent
    # pour générer le graphe d'inférence, ou chargerait un graphe pré-généré
    
    # Vérifier si un graphe pré-généré existe
    graph_path = agent_dir / "inference_graph.json"
    if graph_path.exists():
        try:
            with open(graph_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement du graphe d'inférence: {e}")
    
    # Si aucun graphe pré-généré n'est trouvé, générer un graphe vide
    return {
        "nodes": [],
        "edges": []
    }

def analyze_flow_structure(agent_dir: Path) -> Dict[str, Any]:
    """
    Analyse la structure du flux d'un agent en inspectant son code.
    
    Args:
        agent_dir: Répertoire de l'agent
        
    Returns:
        Dictionnaire représentant la structure du flux
    """
    # Cette fonction est un exemple de comment on pourrait analyser
    # la structure du flux d'un agent en inspectant son code
    
    # Dans une implémentation réelle, cette fonction chargerait les modules
    # de l'agent et inspecterait les classes et les méthodes pour identifier
    # les nœuds et les arêtes du graphe de flux
    
    # Exemple simplifié :
    nodes = []
    edges = []
    
    # Chercher les fichiers Python dans le répertoire de l'agent
    python_files = list(agent_dir.glob("**/*.py"))
    
    for py_file in python_files:
        # Ignorer les fichiers de test, les __init__.py, etc.
        if py_file.name.startswith("test_") or py_file.name == "__init__.py":
            continue
        
        # Essayer de charger le module
        try:
            # Convertir le chemin du fichier en nom de module
            module_path = str(py_file.relative_to(agent_dir.parent)).replace("/", ".").replace("\\", ".")
            module_name = module_path[:-3]  # Enlever l'extension .py
            
            # Charger le module
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Inspecter les classes du module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Vérifier si la classe hérite de Node
                    if "Node" in name or hasattr(obj, "process"):
                        # Ajouter le nœud au graphe
                        nodes.append({
                            "id": name,
                            "label": name,
                            "type": "node"
                        })
                        
                        # Chercher les connexions entre les nœuds
                        # (ceci est simplifié et ne fonctionnerait pas dans tous les cas)
                        for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                            if method_name == "process":
                                source_code = inspect.getsource(method)
                                
                                # Chercher les appels à d'autres nœuds
                                for other_node in nodes:
                                    if other_node["id"] in source_code and other_node["id"] != name:
                                        edges.append({
                                            "source": name,
                                            "target": other_node["id"],
                                            "label": "calls"
                                        })
        except Exception as e:
            print(f"Erreur lors de l'analyse du fichier {py_file}: {e}")
    
    return {
        "nodes": nodes,
        "edges": edges
    }

def convert_to_graphviz(graph: Dict[str, Any]) -> str:
    """
    Convertit un graphe en format DOT pour Graphviz.
    
    Args:
        graph: Dictionnaire représentant le graphe
        
    Returns:
        Chaîne de caractères au format DOT
    """
    dot = "digraph G {\n"
    dot += "  rankdir=LR;\n"
    
    # Ajouter les nœuds
    for node in graph.get("nodes", []):
        node_id = node.get("id", "")
        label = node.get("label", node_id)
        node_type = node.get("type", "")
        
        # Définir le style en fonction du type
        if node_type == "input":
            shape = "ellipse"
            color = "blue"
        elif node_type == "output":
            shape = "ellipse"
            color = "green"
        elif node_type == "llm":
            shape = "box"
            color = "purple"
        else:
            shape = "box"
            color = "black"
        
        dot += f'  "{node_id}" [label="{label}", shape={shape}, color={color}];\n'
    
    # Ajouter les arêtes
    for edge in graph.get("edges", []):
        source = edge.get("source", "")
        target = edge.get("target", "")
        label = edge.get("label", "")
        
        if label:
            dot += f'  "{source}" -> "{target}" [label="{label}"];\n'
        else:
            dot += f'  "{source}" -> "{target}";\n'
    
    dot += "}"
    return dot
