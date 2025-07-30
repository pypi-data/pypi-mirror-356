"""
Fonction de rendu des performances des nœuds pour le tableau de bord.

Ce module fournit la fonction render_node_performance pour visualiser les métriques
de performance des nœuds d'un agent avec des visualisations avancées et des fonctionnalités d'exportation.
"""

from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import os
import random
import datetime
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from num_agents.dashboard.utils.visualizations import (
    create_heatmap, create_radar_chart, create_treemap, render_plotly_chart
)
from num_agents.dashboard.utils.export import create_export_section


def render_node_performance(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche les métriques de performance des nœuds d'un agent avec des visualisations avancées.
    
    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    st.subheader("Performance des nœuds")
    
    # Dans une implémentation réelle, ces données seraient chargées à partir de l'état de l'agent
    # Pour l'instant, nous utilisons des données d'exemple
    nodes = [
        "UserInputNode", 
        "DataProcessorNode", 
        "LLMNode", 
        "ExpertiseWeightingNode", 
        "MultiExpertiseAggregationNode",
        "ReasoningNode",
        "MemoryNode",
        "OutputNode"
    ]
    
    # Générer des données d'exemple plus riches pour chaque nœud
    node_data = {}
    now = datetime.datetime.now()
    
    for node in nodes:
        # Simuler des exécutions sur une période de temps
        executions = []
        for i in range(30):  # 30 exécutions par nœud
            timestamp = now - datetime.timedelta(minutes=i * random.randint(5, 15))
            execution_time = random.uniform(0.1, 2.0)
            
            # Simuler différents types de résultats
            success = random.random() > 0.1  # 90% de réussite
            error_type = None if success else random.choice(["timeout", "validation_error", "api_error", "memory_error"])
            
            # Simuler des métriques supplémentaires
            memory_usage = random.uniform(10, 100) if success else None  # en MB
            cpu_usage = random.uniform(1, 30) if success else None  # en %
            
            # Simuler des données d'entrée/sortie
            input_size = random.randint(100, 5000)  # en octets
            output_size = random.randint(50, 3000) if success else 0  # en octets
            
            executions.append({
                "timestamp": timestamp,
                "execution_time": execution_time,
                "success": success,
                "error_type": error_type,
                "memory_usage": memory_usage,
                "cpu_usage": cpu_usage,
                "input_size": input_size,
                "output_size": output_size,
                "execution_id": f"exec_{random.randint(1000, 9999)}"
            })
        
        # Trier par ordre chronologique
        executions.sort(key=lambda x: x["timestamp"])
        
        # Calculer des statistiques agrégées
        successful_execs = [e for e in executions if e["success"]]
        avg_execution_time = sum(e["execution_time"] for e in successful_execs) / len(successful_execs) if successful_execs else 0
        
        node_data[node] = {
            "executions": executions,
            "call_count": len(executions),
            "success_count": len(successful_execs),
            "error_count": len(executions) - len(successful_execs),
            "avg_execution_time": avg_execution_time,
            "total_execution_time": sum(e["execution_time"] for e in executions),
            "peak_memory_usage": max((e["memory_usage"] or 0) for e in executions),
            "avg_memory_usage": sum((e["memory_usage"] or 0) for e in successful_execs) / len(successful_execs) if successful_execs else 0,
            "total_input_size": sum(e["input_size"] for e in executions),
            "total_output_size": sum(e["output_size"] for e in executions)
        }
    
    # Vue d'ensemble de tous les nœuds
    st.write("### Vue d'ensemble des nœuds")
    
    # Créer un DataFrame pour la vue d'ensemble
    overview_data = []
    for node_name, data in node_data.items():
        overview_data.append({
            "Nœud": node_name,
            "Appels": data["call_count"],
            "Réussites": data["success_count"],
            "Erreurs": data["error_count"],
            "Temps moyen (s)": round(data["avg_execution_time"], 3),
            "Temps total (s)": round(data["total_execution_time"], 3),
            "Mémoire moyenne (MB)": round(data["avg_memory_usage"], 2),
            "Taux de réussite (%)": round(data["success_count"] / data["call_count"] * 100, 1) if data["call_count"] > 0 else 0
        })
    
    overview_df = pd.DataFrame(overview_data)
    
    # Afficher le tableau de synthèse avec mise en forme conditionnelle
    st.dataframe(
        overview_df.style.background_gradient(subset=["Temps moyen (s)"], cmap="YlOrRd")
                       .background_gradient(subset=["Taux de réussite (%)"], cmap="RdYlGn")
    )
    
    # Créer des visualisations pour la vue d'ensemble
    col1, col2 = st.columns(2)
    
    with col1:
        # Graphique à barres des temps d'exécution moyens par nœud
        fig = px.bar(
            overview_df,
            x="Nœud",
            y="Temps moyen (s)",
            color="Taux de réussite (%)",
            color_continuous_scale="RdYlGn",
            title="Temps d'exécution moyen par nœud"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Graphique circulaire des appels par nœud
        fig = px.pie(
            overview_df,
            values="Appels",
            names="Nœud",
            title="Répartition des appels par nœud",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Graphique de comparaison des erreurs
    fig = px.bar(
        overview_df,
        x="Nœud",
        y=["Réussites", "Erreurs"],
        title="Réussites vs Erreurs par nœud",
        barmode="stack"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Sélectionner un nœud spécifique à analyser en détail
    st.write("### Analyse détaillée d'un nœud")
    selected_node = st.selectbox("Sélectionner un nœud à analyser", nodes)
    
    if selected_node in node_data:
        data = node_data[selected_node]
        executions = data["executions"]
        
        # Convertir les exécutions en DataFrame pour faciliter l'analyse
        df_execs = pd.DataFrame(executions)
        
        # Afficher les statistiques clés
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Taux de réussite", 
                f"{data['success_count'] / data['call_count'] * 100:.1f}%" if data['call_count'] > 0 else "N/A",
                delta=None
            )
        with col2:
            st.metric(
                "Temps moyen d'exécution", 
                f"{data['avg_execution_time']:.3f}s"
            )
        with col3:
            st.metric(
                "Mémoire moyenne", 
                f"{data['avg_memory_usage']:.2f} MB"
            )
        with col4:
            st.metric(
                "Nombre d'erreurs", 
                data["error_count"],
                delta_color="inverse"
            )
        
        # Créer des onglets pour différentes vues
        tab1, tab2, tab3 = st.tabs(["Performance", "Erreurs", "Ressources"])
        
        with tab1:
            st.write("#### Analyse de performance")
            
            # Graphique des temps d'exécution au fil du temps
            fig = go.Figure()
            
            # Ajouter les temps d'exécution
            fig.add_trace(go.Scatter(
                x=[e["timestamp"] for e in executions],
                y=[e["execution_time"] for e in executions],
                mode="lines+markers",
                name="Temps d'exécution",
                marker=dict(
                    color=["red" if not e["success"] else "blue" for e in executions],
                    size=8
                )
            ))
            
            # Ajouter une ligne pour le temps moyen
            fig.add_trace(go.Scatter(
                x=[executions[0]["timestamp"], executions[-1]["timestamp"]],
                y=[data["avg_execution_time"], data["avg_execution_time"]],
                mode="lines",
                name="Temps moyen",
                line=dict(dash="dash", color="green")
            ))
            
            # Configurer le graphique
            fig.update_layout(
                title=f"Temps d'exécution du nœud {selected_node} au fil du temps",
                xaxis_title="Date et heure",
                yaxis_title="Temps (secondes)",
                height=400
            )
            
            # Afficher le graphique
            st.plotly_chart(fig, use_container_width=True)
            
            # Histogramme des temps d'exécution
            fig = px.histogram(
                df_execs,
                x="execution_time",
                nbins=20,
                title=f"Distribution des temps d'exécution pour {selected_node}",
                labels={"execution_time": "Temps d'exécution (s)"}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Corrélation entre taille d'entrée et temps d'exécution
            fig = px.scatter(
                df_execs,
                x="input_size",
                y="execution_time",
                color="success",
                title="Corrélation entre taille d'entrée et temps d'exécution",
                labels={
                    "input_size": "Taille d'entrée (octets)",
                    "execution_time": "Temps d'exécution (s)",
                    "success": "Succès"
                },
                color_discrete_map={True: "green", False: "red"}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            st.write("#### Analyse des erreurs")
            
            # Filtrer les exécutions avec erreur
            error_execs = [e for e in executions if not e["success"]]
            
            if error_execs:
                # Créer un DataFrame pour les erreurs
                df_errors = pd.DataFrame(error_execs)
                
                # Graphique circulaire des types d'erreurs
                error_counts = df_errors["error_type"].value_counts().reset_index()
                error_counts.columns = ["Type d'erreur", "Nombre"]
                
                fig = px.pie(
                    error_counts,
                    values="Nombre",
                    names="Type d'erreur",
                    title=f"Répartition des types d'erreurs pour {selected_node}",
                    color_discrete_sequence=px.colors.sequential.Reds_r
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Afficher les détails des erreurs
                st.write("#### Détails des erreurs")
                for i, error in enumerate(error_execs):
                    with st.expander(f"Erreur {i+1}: {error['error_type']} ({error['timestamp'].strftime('%Y-%m-%d %H:%M:%S')})"):
                        st.write(f"**ID d'exécution:** {error['execution_id']}")
                        st.write(f"**Timestamp:** {error['timestamp']}")
                        st.write(f"**Type d'erreur:** {error['error_type']}")
                        st.write(f"**Taille d'entrée:** {error['input_size']} octets")
                        st.write(f"**Temps avant échec:** {error['execution_time']:.3f}s")
            else:
                st.success("Aucune erreur détectée pour ce nœud.")
        
        with tab3:
            st.write("#### Utilisation des ressources")
            
            # Graphique de l'utilisation de la mémoire au fil du temps
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Ajouter l'utilisation de la mémoire
            fig.add_trace(
                go.Scatter(
                    x=[e["timestamp"] for e in executions if e["memory_usage"] is not None],
                    y=[e["memory_usage"] for e in executions if e["memory_usage"] is not None],
                    name="Mémoire (MB)",
                    line=dict(color="blue")
                ),
                secondary_y=False
            )
            
            # Ajouter l'utilisation du CPU
            fig.add_trace(
                go.Scatter(
                    x=[e["timestamp"] for e in executions if e["cpu_usage"] is not None],
                    y=[e["cpu_usage"] for e in executions if e["cpu_usage"] is not None],
                    name="CPU (%)",
                    line=dict(color="orange")
                ),
                secondary_y=True
            )
            
            # Configurer les axes
            fig.update_layout(
                title=f"Utilisation des ressources pour {selected_node}",
                xaxis_title="Date et heure"
            )
            fig.update_yaxes(title_text="Mémoire (MB)", secondary_y=False)
            fig.update_yaxes(title_text="CPU (%)", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Graphique de la relation entre taille de sortie et utilisation de la mémoire
            successful_df = df_execs[df_execs["success"]]
            if not successful_df.empty:
                fig = px.scatter(
                    successful_df,
                    x="output_size",
                    y="memory_usage",
                    size="execution_time",
                    color="cpu_usage",
                    title="Relation entre taille de sortie et utilisation des ressources",
                    labels={
                        "output_size": "Taille de sortie (octets)",
                        "memory_usage": "Utilisation de la mémoire (MB)",
                        "execution_time": "Temps d'exécution (s)",
                        "cpu_usage": "Utilisation CPU (%)"
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Section d'exportation des données
        st.write("### Exportation des données")
        
        # Créer un DataFrame pour l'exportation
        export_df = pd.DataFrame(executions)
        
        # Ajouter le nom du nœud pour référence
        export_df["node"] = selected_node
        
        # Créer la section d'exportation
        create_export_section(export_df, f"node_performance_{selected_node}")
        
        st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir des métriques réelles de l'agent.")
