"""
Fonction de rendu des événements pour le tableau de bord.

Ce module fournit la fonction render_events pour visualiser les événements
des agents avec des visualisations avancées et des fonctionnalités d'exportation.
"""

from pathlib import Path
from typing import Optional, List, Dict, Any
import datetime
import random
import pandas as pd
import streamlit as st
import plotly.express as px

from num_agents.dashboard.utils.visualizations import (
    create_timeline, create_gantt_chart, render_plotly_chart
)
from num_agents.dashboard.utils.export import create_export_section


def render_events(target_dir: Path, agent_name: Optional[str] = None) -> None:
    """
    Affiche les événements d'un agent avec des visualisations avancées.

    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    st.subheader("Événements de l'agent")

    # Générer des données d'exemple pour les événements
    now = datetime.datetime.now()
    event_types = ["TASK_STARTED", "TASK_COMPLETED", "MESSAGE_RECEIVED", "MESSAGE_SENT", "STATE_UPDATED"]
    event_sources = ["User", "Agent", "System", "Scheduler", "API"]
    event_statuses = ["SUCCESS", "PENDING", "FAILED", "RETRYING"]

    events = []
    for i in range(30):  # Générer 30 événements d'exemple
        timestamp = now - datetime.timedelta(minutes=i * random.randint(1, 10))
        event_type = random.choice(event_types)
        source = random.choice(event_sources)
        status = random.choice(event_statuses)
        
        # Générer un message d'événement en fonction du type
        if event_type == "TASK_STARTED":
            task_id = f"task_{random.randint(1000, 9999)}"
            message = f"Tâche {task_id} démarrée par {source}"
        elif event_type == "TASK_COMPLETED":
            task_id = f"task_{random.randint(1000, 9999)}"
            duration = random.uniform(0.5, 10.0)
            message = f"Tâche {task_id} terminée en {duration:.2f}s (Statut: {status})"
        elif event_type == "MESSAGE_RECEIVED":
            msg_id = f"msg_{random.randint(1000, 9999)}"
            message = f"Message {msg_id} reçu de {source}"
        elif event_type == "MESSAGE_SENT":
            msg_id = f"msg_{random.randint(1000, 9999)}"
            message = f"Message {msg_id} envoyé à {random.choice(['utilisateur', 'agent', 'système'])}"
        else:  # STATE_UPDATED
            state_key = random.choice(["user_preferences", "conversation_context", "agent_knowledge"])
            message = f"État mis à jour: {state_key} (Source: {source})"
        
        events.append({
            "timestamp": timestamp,
            "type": event_type,
            "source": source,
            "status": status,
            "message": message,
            "duration": random.uniform(0.1, 5.0) if random.random() > 0.7 else None,
            "agent": agent_name or "main_agent"
        })
    
    # Trier les événements par ordre chronologique inverse
    events.sort(key=lambda x: x["timestamp"], reverse=True)
    df_events = pd.DataFrame(events)
    
    # Créer des onglets pour différentes vues
    tab1, tab2, tab3 = st.tabs(["Liste", "Chronologie", "Statistiques"])
    
    with tab1:
        # Filtres interactifs
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_types = st.multiselect("Filtrer par type", event_types, default=event_types)
        with col2:
            selected_sources = st.multiselect("Filtrer par source", event_sources, default=event_sources)
        with col3:
            selected_statuses = st.multiselect("Filtrer par statut", event_statuses, default=event_statuses)
        
        # Appliquer les filtres
        filtered = df_events[
            (df_events["type"].isin(selected_types)) &
            (df_events["source"].isin(selected_sources)) &
            (df_events["status"].isin(selected_statuses))
        ]
        
        # Afficher le nombre d'événements filtrés
        st.info(f"{len(filtered)} événements affichés sur {len(df_events)} au total")
        
        if not filtered.empty:
            # Afficher les événements avec mise en forme
            for _, event in filtered.iterrows():
                # Définir la couleur en fonction du type d'événement
                color = {
                    "TASK_STARTED": "#4e79a7",
                    "TASK_COMPLETED": "#59a14f",
                    "MESSAGE_RECEIVED": "#edc949",
                    "MESSAGE_SENT": "#f28e2c",
                    "STATE_UPDATED": "#e15759"
                }.get(event["type"], "gray")
                
                # Définir l'icône en fonction du type d'événement
                icon = {
                    "TASK_STARTED": "▶️",
                    "TASK_COMPLETED": "✅",
                    "MESSAGE_RECEIVED": "📥",
                    "MESSAGE_SENT": "📤",
                    "STATE_UPDATED": "🔄"
                }.get(event["type"], "ℹ️")
                
                # Afficher l'événement avec mise en forme
                st.markdown(
                    f"<div style='padding:10px; margin-bottom:10px; border-left:4px solid {color}; background-color:rgba(0,0,0,0.03); border-radius:4px;'>"
                    f"<div style='display:flex; justify-content:space-between;'>"
                    f"<span style='color:{color}; font-weight:bold;'>{icon} {event['type']}</span>"
                    f"<span style='color:gray;'>{event['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</span>"
                    f"</div>"
                    f"<div style='margin-top:5px;'>{event['message']}</div>"
                    f"<div style='margin-top:5px; font-size:0.9em; color:#666;'>"
                    f"Source: <span style='font-weight:bold;'>{event['source']}</span> • "
                    f"Statut: <span style='font-weight:bold;'>{event['status']}</span>"
                    f"</div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.warning("Aucun événement ne correspond aux filtres sélectionnés.")
    
    with tab2:
        st.subheader("Chronologie des événements")
        
        # Préparer les données pour la chronologie
        timeline_events = []
        for _, event in df_events.iterrows():
            timeline_events.append({
                'timestamp': event['timestamp'],
                'event_type': event['type'],
                'description': f"[{event['source']}] {event['message']}",
                'status': event['status']
            })
        
        # Créer et afficher la chronologie
        if timeline_events:
            timeline_fig = create_timeline(timeline_events, "Chronologie des événements")
            render_plotly_chart(timeline_fig)
        else:
            st.info("Aucun événement à afficher dans la chronologie.")
    
    with tab3:
        st.subheader("Statistiques des événements")
        
        if not df_events.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution par type d'événement
                st.write("Distribution par type d'événement")
                type_counts = df_events['type'].value_counts().reset_index()
                type_counts.columns = ['Type', 'Nombre']
                
                fig = px.pie(type_counts, values='Nombre', names='Type', 
                            title='Répartition des types d\'événements',
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Distribution par source
                st.write("Distribution par source")
                source_counts = df_events['source'].value_counts().reset_index()
                source_counts.columns = ['Source', 'Nombre']
                
                fig = px.bar(source_counts, x='Source', y='Nombre', 
                           title='Nombre d\'événements par source',
                           color='Source',
                           color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
            
            # Distribution temporelle
            st.write("Distribution temporelle des événements")
            try:
                # Grouper par intervalle de temps
                df_events['time_group'] = df_events['timestamp'].dt.floor('10min')
                time_counts = df_events.groupby(['time_group', 'type']).size().reset_index()
                time_counts.columns = ['Temps', 'Type', 'Nombre']
                
                # Créer un graphique temporel avec couleurs par type
                fig = px.line(time_counts, x='Temps', y='Nombre', color='Type',
                            title='Évolution des événements dans le temps',
                            color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.warning(f"Impossible de créer la distribution temporelle: {str(e)}")
    
    # Section d'exportation
    st.subheader("Exportation des événements")
    create_export_section(df_events, "events_export")
    
    st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir des journaux de l'agent.")
