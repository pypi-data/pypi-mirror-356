"""
Composant de vue des métriques pour le tableau de bord.

Ce module fournit des fonctions pour visualiser les métriques de performance des agents,
l'utilisation des modèles et les temps de réponse avec des visualisations avancées
et des fonctionnalités d'exportation.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os
import random
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from num_agents.dashboard.utils.visualizations import (
    create_heatmap, create_radar_chart, create_treemap, render_plotly_chart
)
from num_agents.dashboard.utils.export import create_export_section
from num_agents.dashboard.components.render_node_performance import render_node_performance

def render_metrics_view(target_dir: Path, is_system: bool = False):
    """
    Affiche la vue des métriques dans le tableau de bord.
    
    Args:
        target_dir: Répertoire de l'agent ou du système à visualiser
        is_system: Indique si la cible est un système multi-agents
    """
    import streamlit as st
    
    st.header("Vue des Métriques")
    
    # Si c'est un système multi-agents, permettre de sélectionner l'agent
    selected_agent = None
    if is_system:
        agents = get_available_agents(target_dir)
        if agents:
            selected_agent = st.selectbox("Sélectionner un agent", agents)
        else:
            st.warning("Aucun agent trouvé dans le système.")
            return
    
    # Sélection du type de métriques à visualiser
    metrics_type = st.selectbox(
        "Type de métriques",
        ["Performance des nœuds", "Utilisation des modèles", "Temps de réponse"]
    )
    
    # Affichage du type de métriques sélectionné
    if metrics_type == "Performance des nœuds":
        render_node_performance(target_dir, selected_agent)
    elif metrics_type == "Utilisation des modèles":
        render_model_usage(target_dir, selected_agent)
    elif metrics_type == "Temps de réponse":
        render_response_times(target_dir, selected_agent)

# La fonction render_node_performance est maintenant importée depuis le module dédié

def render_model_usage(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche les métriques d'utilisation des modèles LLM d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Utilisation des modèles")
    
    # Dans une implémentation réelle, ces données seraient chargées à partir de l'état de l'agent
    # Pour l'instant, nous utilisons des données d'exemple
    models = {
        "gemini-2.0-flash": {
            "call_count": 45,
            "token_count": 12500,
            "avg_response_time": 0.8,
            "cost_estimate": 0.25
        },
        "gemini-2.0-pro": {
            "call_count": 15,
            "token_count": 8000,
            "avg_response_time": 1.2,
            "cost_estimate": 0.40
        },
        "gemini-1.5-flash": {
            "call_count": 5,
            "token_count": 1500,
            "avg_response_time": 0.7,
            "cost_estimate": 0.05
        }
    }
    
    # Afficher un résumé de l'utilisation des modèles
    try:
        import plotly.graph_objects as go
        import pandas as pd
        
        # Créer un DataFrame pour le graphique
        models_df = pd.DataFrame({
            "Modèle": list(models.keys()),
            "Appels": [models[m]["call_count"] for m in models],
            "Tokens": [models[m]["token_count"] for m in models],
            "Temps moyen (s)": [models[m]["avg_response_time"] for m in models],
            "Coût estimé ($)": [models[m]["cost_estimate"] for m in models]
        })
        
        # Afficher le tableau des données
        st.dataframe(models_df)
        
        # Créer des graphiques
        tab1, tab2, tab3 = st.tabs(["Appels", "Tokens", "Coût"])
        
        with tab1:
            # Graphique des appels
            fig1 = go.Figure(data=[
                go.Bar(
                    x=models_df["Modèle"],
                    y=models_df["Appels"],
                    marker_color=["#1f77b4", "#ff7f0e", "#2ca02c"]
                )
            ])
            fig1.update_layout(
                title="Nombre d'appels par modèle",
                xaxis_title="Modèle",
                yaxis_title="Nombre d'appels",
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with tab2:
            # Graphique des tokens
            fig2 = go.Figure(data=[
                go.Bar(
                    x=models_df["Modèle"],
                    y=models_df["Tokens"],
                    marker_color=["#1f77b4", "#ff7f0e", "#2ca02c"]
                )
            ])
            fig2.update_layout(
                title="Nombre de tokens par modèle",
                xaxis_title="Modèle",
                yaxis_title="Nombre de tokens",
                height=400
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            # Graphique des coûts
            fig3 = go.Figure(data=[
                go.Bar(
                    x=models_df["Modèle"],
                    y=models_df["Coût estimé ($)"],
                    marker_color=["#1f77b4", "#ff7f0e", "#2ca02c"]
                )
            ])
            fig3.update_layout(
                title="Coût estimé par modèle ($)",
                xaxis_title="Modèle",
                yaxis_title="Coût ($)",
                height=400
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    except ImportError:
        st.error("Les modules 'plotly' et 'pandas' sont nécessaires pour afficher les graphiques. Veuillez les installer avec 'pip install plotly pandas'.")
        
        # Afficher les données brutes
        for model, data in models.items():
            st.write(f"**{model}**")
            st.write(f"- Appels: {data['call_count']}")
            st.write(f"- Tokens: {data['token_count']}")
            st.write(f"- Temps moyen: {data['avg_response_time']}s")
            st.write(f"- Coût estimé: ${data['cost_estimate']}")
    
    st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir de l'état de l'agent.")

def render_response_times(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche les métriques de temps de réponse d'un agent.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    import streamlit as st
    
    st.subheader("Temps de réponse")
    
    # Dans une implémentation réelle, ces données seraient chargées à partir de l'état de l'agent
    # Pour l'instant, nous utilisons des données d'exemple
    
    # Générer des données d'exemple pour les temps de réponse
    now = datetime.datetime.now()
    response_times = []
    
    for i in range(20):
        # Générer un timestamp pour les 20 dernières heures
        timestamp = now - datetime.timedelta(hours=i)
        
        # Générer un temps de réponse aléatoire entre 0.5 et 3 secondes
        response_time = random.uniform(0.5, 3.0)
        
        response_times.append({
            "timestamp": timestamp,
            "response_time": response_time,
            "request_type": random.choice(["user_query", "system_event", "scheduled_task"])
        })
    
    # Trier les données par timestamp
    response_times.sort(key=lambda x: x["timestamp"])
    
    # Afficher un graphique des temps de réponse
    try:
        import plotly.graph_objects as go
        import pandas as pd
        
        # Créer un DataFrame pour le graphique
        df = pd.DataFrame(response_times)
        
        # Créer le graphique
        fig = go.Figure()
        
        # Ajouter une trace pour chaque type de requête
        for req_type in ["user_query", "system_event", "scheduled_task"]:
            df_filtered = df[df["request_type"] == req_type]
            
            if not df_filtered.empty:
                fig.add_trace(go.Scatter(
                    x=df_filtered["timestamp"],
                    y=df_filtered["response_time"],
                    mode="lines+markers",
                    name=req_type
                ))
        
        # Configurer le graphique
        fig.update_layout(
            title="Temps de réponse au fil du temps",
            xaxis_title="Heure",
            yaxis_title="Temps de réponse (secondes)",
            height=400
        )
        
        # Afficher le graphique
        st.plotly_chart(fig, use_container_width=True)
        
        # Afficher des statistiques
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_time = sum(item["response_time"] for item in response_times) / len(response_times)
            st.metric("Temps moyen de réponse", f"{avg_time:.2f}s")
        
        with col2:
            max_time = max(item["response_time"] for item in response_times)
            st.metric("Temps de réponse max", f"{max_time:.2f}s")
        
        with col3:
            min_time = min(item["response_time"] for item in response_times)
            st.metric("Temps de réponse min", f"{min_time:.2f}s")
        
        # Afficher un histogramme des temps de réponse
        fig2 = go.Figure(data=[
            go.Histogram(x=[item["response_time"] for item in response_times], nbinsx=10)
        ])
        fig2.update_layout(
            title="Distribution des temps de réponse",
            xaxis_title="Temps de réponse (secondes)",
            yaxis_title="Fréquence",
            height=300
        )
        
        st.plotly_chart(fig2, use_container_width=True)
        
    except ImportError:
        st.error("Les modules 'plotly' et 'pandas' sont nécessaires pour afficher les graphiques. Veuillez les installer avec 'pip install plotly pandas'.")
        
        # Afficher les données brutes
        st.write("Temps de réponse (secondes):")
        for item in response_times:
            st.write(f"{item['timestamp']}: {item['response_time']:.2f}s ({item['request_type']})")
    
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
