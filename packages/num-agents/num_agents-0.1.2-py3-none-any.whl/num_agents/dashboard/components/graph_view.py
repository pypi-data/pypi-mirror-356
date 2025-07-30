"""
Composant de vue des graphes logiques pour le tableau de bord.

Ce module fournit des fonctions pour visualiser les graphes de flux,
de dépendances et d'inférence des agents.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os

def render_graph_view(target_dir: Path, is_system: bool = False):
    """
    Affiche la vue des graphes logiques dans le tableau de bord.
    
    Args:
        target_dir: Répertoire de l'agent ou du système à visualiser
        is_system: Indique si la cible est un système multi-agents
    """
    import streamlit as st
    
    st.header("Vue des Graphes Logiques")
    
    # Sélection du type de graphe
    graph_type = st.selectbox(
        "Type de graphe",
        ["Graphe de flux", "Graphe de dépendances", "Graphe d'inférence"]
    )
    
    # Si c'est un système multi-agents, permettre de sélectionner l'agent
    selected_agent = None
    if is_system:
        agents = get_available_agents(target_dir)
        if agents:
            selected_agent = st.selectbox("Sélectionner un agent", agents)
        else:
            st.warning("Aucun agent trouvé dans le système.")
            return
    
    # Affichage du graphe sélectionné
    if graph_type == "Graphe de flux":
        render_flow_graph(target_dir, selected_agent)
    elif graph_type == "Graphe de dépendances":
        render_dependency_graph(target_dir, selected_agent)
    elif graph_type == "Graphe d'inférence":
        render_inference_graph(target_dir, selected_agent)

def render_flow_graph(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche le graphe de flux d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Graphe de flux")
    
    # Vérifier si graphviz est installé
    try:
        import graphviz
    except ImportError:
        st.error("Le module 'graphviz' n'est pas installé. Veuillez l'installer avec 'pip install graphviz'.")
        st.info("Note: Vous devez également installer le logiciel Graphviz sur votre système.")
        return
    
    # Créer un graphe de flux d'exemple
    # Dans une implémentation réelle, ce graphe serait généré à partir de l'analyse du code de l'agent
    graph = graphviz.Digraph()
    graph.attr(rankdir='LR')
    
    # Ajouter des nœuds et des arêtes d'exemple
    graph.node('input', 'Entrée Utilisateur', shape='ellipse')
    graph.node('process', 'Traitement', shape='box')
    graph.node('llm', 'LLM', shape='box')
    graph.node('output', 'Sortie', shape='ellipse')
    
    graph.edge('input', 'process')
    graph.edge('process', 'llm')
    graph.edge('llm', 'output')
    
    # Afficher le graphe
    st.graphviz_chart(graph)
    
    st.info("Note: Ce graphe est un exemple. Dans une implémentation complète, il serait généré dynamiquement à partir de l'analyse du code de l'agent.")

def render_dependency_graph(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche le graphe de dépendances d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Graphe de dépendances")
    
    # Vérifier si graphviz est installé
    try:
        import graphviz
    except ImportError:
        st.error("Le module 'graphviz' n'est pas installé. Veuillez l'installer avec 'pip install graphviz'.")
        return
    
    # Créer un graphe de dépendances d'exemple
    graph = graphviz.Digraph()
    graph.attr(rankdir='TB')
    
    # Ajouter des nœuds et des arêtes d'exemple
    graph.node('core', 'Core')
    graph.node('memory', 'Memory')
    graph.node('llm', 'LLM')
    graph.node('reasoning', 'Reasoning')
    graph.node('eventbus', 'EventBus')
    
    graph.edge('reasoning', 'core')
    graph.edge('reasoning', 'llm')
    graph.edge('memory', 'core')
    graph.edge('eventbus', 'core')
    
    # Afficher le graphe
    st.graphviz_chart(graph)
    
    st.info("Note: Ce graphe est un exemple. Dans une implémentation complète, il serait généré dynamiquement à partir de l'analyse des dépendances de l'agent.")

def render_inference_graph(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche le graphe d'inférence d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Graphe d'inférence")
    
    # Vérifier si graphviz est installé
    try:
        import graphviz
    except ImportError:
        st.error("Le module 'graphviz' n'est pas installé. Veuillez l'installer avec 'pip install graphviz'.")
        return
    
    # Créer un graphe d'inférence d'exemple
    graph = graphviz.Digraph()
    graph.attr(rankdir='TB')
    
    # Ajouter des nœuds et des arêtes d'exemple pour un graphe d'inférence logique
    graph.node('p1', 'Le ciel est bleu', shape='box')
    graph.node('p2', 'S\'il pleut, le ciel est gris', shape='box')
    graph.node('p3', 'Il pleut', shape='box')
    graph.node('c1', 'Le ciel est gris', shape='ellipse')
    graph.node('c2', 'Contradiction!', shape='diamond', color='red')
    
    graph.edge('p2', 'c1', label='Modus Ponens')
    graph.edge('p3', 'c1', label='Modus Ponens')
    graph.edge('p1', 'c2')
    graph.edge('c1', 'c2')
    
    # Afficher le graphe
    st.graphviz_chart(graph)
    
    st.info("Note: Ce graphe est un exemple. Dans une implémentation complète, il serait généré dynamiquement à partir de l'analyse du moteur d'inférence de l'agent.")

def get_available_agents(target_dir: Path) -> List[str]:
    """
    Récupère la liste des agents disponibles dans un système multi-agents.
    
    Args:
        target_dir: Répertoire du système multi-agents
        
    Returns:
        Liste des noms d'agents disponibles
    """
    agents = []
    
    # Chercher le fichier de configuration du système
    system_config_path = target_dir / "system.yaml"
    if system_config_path.exists():
        try:
            import yaml
            with open(system_config_path, 'r') as f:
                system_config = yaml.safe_load(f)
                
            if 'system' in system_config and 'agents' in system_config['system']:
                for agent_config in system_config['system']['agents']:
                    agent_name = agent_config.get('name', 'Unknown')
                    agents.append(agent_name)
        except Exception as e:
            import streamlit as st
            st.error(f"Erreur lors de la lecture du fichier de configuration: {e}")
    else:
        # Chercher les répertoires d'agents
        for subdir in target_dir.iterdir():
            if subdir.is_dir() and (subdir / "agent.yaml").exists():
                agents.append(subdir.name)
    
    return agents
