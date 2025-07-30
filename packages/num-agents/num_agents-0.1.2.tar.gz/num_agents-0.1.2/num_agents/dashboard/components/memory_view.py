"""
Composant de vue de la mémoire pour le tableau de bord.

Ce module fournit des fonctions pour visualiser l'état de la mémoire des agents,
les croyances actuelles et l'historique des révisions.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os

def render_memory_view(target_dir: Path, is_system: bool = False):
    """
    Affiche la vue de la mémoire dans le tableau de bord.
    
    Args:
        target_dir: Répertoire de l'agent ou du système à visualiser
        is_system: Indique si la cible est un système multi-agents
    """
    import streamlit as st
    
    st.header("Vue de la Mémoire")
    
    # Si c'est un système multi-agents, permettre de sélectionner l'agent
    selected_agent = None
    if is_system:
        agents = get_available_agents(target_dir)
        if agents:
            selected_agent = st.selectbox("Sélectionner un agent", agents)
        else:
            st.warning("Aucun agent trouvé dans le système.")
            return
    
    # Sélection du type de mémoire à visualiser
    memory_type = st.selectbox(
        "Type de mémoire",
        ["Croyances actuelles", "Contextes logiques", "Historique des révisions"]
    )
    
    # Affichage du type de mémoire sélectionné
    if memory_type == "Croyances actuelles":
        render_current_beliefs(target_dir, selected_agent)
    elif memory_type == "Contextes logiques":
        render_logical_contexts(target_dir, selected_agent)
    elif memory_type == "Historique des révisions":
        render_revision_history(target_dir, selected_agent)

def render_current_beliefs(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche les croyances actuelles d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Croyances actuelles")
    
    # Dans une implémentation réelle, ces données seraient chargées à partir de l'état de l'agent
    # Pour l'instant, nous utilisons des données d'exemple
    beliefs = [
        {"id": "p1", "text": "Le ciel est bleu", "confidence": 0.9, "status": "VERIFIED"},
        {"id": "p2", "text": "S'il pleut, le ciel est gris", "confidence": 0.95, "status": "VERIFIED"},
        {"id": "p3", "text": "Il pleut", "confidence": 0.7, "status": "UNVERIFIED"},
        {"id": "c1", "text": "Le ciel est gris", "confidence": 0.7, "status": "DERIVED", "derived_from": ["p2", "p3"]},
    ]
    
    # Filtrer par statut
    status_filter = st.multiselect(
        "Filtrer par statut",
        ["VERIFIED", "UNVERIFIED", "DERIVED", "REJECTED"],
        default=["VERIFIED", "UNVERIFIED", "DERIVED"]
    )
    
    filtered_beliefs = [b for b in beliefs if b["status"] in status_filter]
    
    # Afficher les croyances
    if filtered_beliefs:
        # Créer un tableau pour afficher les croyances
        table_data = {
            "ID": [b["id"] for b in filtered_beliefs],
            "Proposition": [b["text"] for b in filtered_beliefs],
            "Confiance": [f"{b['confidence']:.2f}" for b in filtered_beliefs],
            "Statut": [b["status"] for b in filtered_beliefs],
        }
        
        st.dataframe(table_data)
        
        # Afficher les détails de chaque croyance
        for belief in filtered_beliefs:
            with st.expander(f"{belief['id']}: {belief['text']}"):
                st.write(f"**Confiance:** {belief['confidence']:.2f}")
                st.write(f"**Statut:** {belief['status']}")
                
                if "derived_from" in belief:
                    st.write("**Dérivé de:**")
                    for parent_id in belief["derived_from"]:
                        parent = next((b for b in beliefs if b["id"] == parent_id), None)
                        if parent:
                            st.write(f"- {parent_id}: {parent['text']}")
    else:
        st.info("Aucune croyance ne correspond aux filtres sélectionnés.")
    
    st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir de l'état de l'agent.")

def render_logical_contexts(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche les contextes logiques d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Contextes logiques")
    
    # Dans une implémentation réelle, ces données seraient chargées à partir de l'état de l'agent
    # Pour l'instant, nous utilisons des données d'exemple
    contexts = [
        {
            "id": "ctx1",
            "name": "Météo",
            "description": "Contexte pour les raisonnements liés à la météo",
            "propositions": ["p1", "p2", "p3", "c1"]
        },
        {
            "id": "ctx2",
            "name": "Planification",
            "description": "Contexte pour les raisonnements liés à la planification",
            "propositions": ["p4", "p5", "c2"]
        }
    ]
    
    # Sélectionner un contexte
    context_names = [ctx["name"] for ctx in contexts]
    selected_context = st.selectbox("Sélectionner un contexte", context_names)
    
    # Afficher le contexte sélectionné
    context = next((ctx for ctx in contexts if ctx["name"] == selected_context), None)
    if context:
        st.write(f"**ID:** {context['id']}")
        st.write(f"**Description:** {context['description']}")
        
        st.write("**Propositions dans ce contexte:**")
        for prop_id in context["propositions"]:
            st.write(f"- {prop_id}")
    
    st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir de l'état de l'agent.")

def render_revision_history(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche l'historique des révisions de croyances d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Historique des révisions")
    
    # Dans une implémentation réelle, ces données seraient chargées à partir de l'état de l'agent
    # Pour l'instant, nous utilisons des données d'exemple
    revisions = [
        {
            "timestamp": "2025-06-19T14:30:00",
            "proposition_id": "p3",
            "old_value": {"text": "Il ne pleut pas", "confidence": 0.8, "status": "VERIFIED"},
            "new_value": {"text": "Il pleut", "confidence": 0.7, "status": "UNVERIFIED"},
            "reason": "Nouvelle observation"
        },
        {
            "timestamp": "2025-06-19T14:25:00",
            "proposition_id": "c1",
            "old_value": {"text": "Le ciel est gris", "confidence": 0.7, "status": "DERIVED"},
            "new_value": {"text": "Le ciel est gris", "confidence": 0.7, "status": "REJECTED"},
            "reason": "Révision de la croyance parent"
        }
    ]
    
    # Afficher l'historique des révisions
    if revisions:
        for revision in revisions:
            with st.expander(f"{revision['timestamp']} - Révision de {revision['proposition_id']}"):
                st.write(f"**Raison:** {revision['reason']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Ancienne valeur:**")
                    st.write(f"Texte: {revision['old_value']['text']}")
                    st.write(f"Confiance: {revision['old_value']['confidence']:.2f}")
                    st.write(f"Statut: {revision['old_value']['status']}")
                
                with col2:
                    st.write("**Nouvelle valeur:**")
                    st.write(f"Texte: {revision['new_value']['text']}")
                    st.write(f"Confiance: {revision['new_value']['confidence']:.2f}")
                    st.write(f"Statut: {revision['new_value']['status']}")
    else:
        st.info("Aucune révision trouvée.")
    
    st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir de l'état de l'agent.")

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
