"""
Composant de vue des traces pour le tableau de bord.

Ce module fournit des fonctions pour visualiser les journaux d'exécution,
les événements et les erreurs des agents avec des visualisations avancées
et des fonctionnalités d'exportation.
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
from num_agents.dashboard.components.render_events import render_events
from num_agents.dashboard.components.render_errors import render_errors

def get_available_agents(target_dir: Path) -> List[str]:
    """
    Récupère la liste des agents disponibles dans le répertoire.
    (Implémentation factice pour l'exemple)
    """
    # À remplacer par une lecture réelle du dossier
    return [p.name for p in target_dir.iterdir() if p.is_dir()]

def render_execution_logs(target_dir: Path, agent_name: Optional[str] = None):
    """
    Affiche les journaux d'exécution d'un agent avec des visualisations avancées.

    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    st.subheader("Journaux d'exécution")

    now = datetime.datetime.now()
    log_levels = ["INFO", "DEBUG", "WARNING", "ERROR"]
    log_components = ["Core", "LLM", "Memory", "Reasoning", "EventBus", "Scheduler"]

    # Générer des données d'exemple plus riches
    logs = []
    for i in range(50):  # Augmenter le nombre d'entrées pour de meilleures visualisations
        timestamp = now - datetime.timedelta(minutes=i * random.randint(1, 5))
        level = random.choices(log_levels, weights=[0.6, 0.3, 0.08, 0.02])[0]
        component = random.choice(log_components)
        duration = random.uniform(0.1, 5.0) if random.random() > 0.7 else None

        if level == "INFO":
            msg_list = [
                "Traitement de la requête utilisateur terminé",
                "Modèle LLM appelé avec succès",
                "Croyance mise à jour dans la mémoire",
                "Événement publié sur le bus d'événements",
                "Tâche planifiée exécutée"
            ]
        elif level == "DEBUG":
            msg_list = [
                "Entrée LLM: 'Quelle est la capitale de la France?'",
                "Sortie LLM: 'La capitale de la France est Paris.'",
                "Temps de traitement: 1.23s",
                "Contexte logique initialisé",
                "Nœud de raisonnement activé"
            ]
        elif level == "WARNING":
            msg_list = [
                "Temps de réponse LLM supérieur au seuil",
                "Croyance contradictoire détectée",
                "Tentative de reconnexion au service externe",
                "Mémoire tampon presque pleine",
                "Tâche planifiée retardée"
            ]
        else:  # ERROR
            msg_list = [
                "Échec de l'appel au modèle LLM",
                "Exception lors du traitement de la requête",
                "Échec de la mise à jour de la mémoire",
                "Erreur de publication d'événement",
                "Tâche planifiée échouée"
            ]

        logs.append({
            "timestamp": timestamp,
            "level": level,
            "component": component,
            "message": random.choice(msg_list),
            "duration": duration,
            "agent": agent_name or "main_agent"
        })

    logs.sort(key=lambda x: x["timestamp"], reverse=True)
    
    # Convertir en DataFrame pour faciliter la manipulation
    df_logs = pd.DataFrame(logs)
    
    # Créer des onglets pour différentes vues
    tab1, tab2, tab3, tab4 = st.tabs(["Liste", "Chronologie", "Statistiques", "Exportation"])
    
    with tab1:
        # Filtres interactifs
        col1, col2 = st.columns(2)
        with col1:
            selected_levels = st.multiselect("Filtrer par niveau", log_levels, default=log_levels)
        with col2:
            selected_components = st.multiselect("Filtrer par composant", log_components, default=log_components)

        # Appliquer les filtres
        filtered = df_logs[
            df_logs["level"].isin(selected_levels) & 
            df_logs["component"].isin(selected_components)
        ]

        # Afficher le nombre d'entrées filtrées
        st.info(f"{len(filtered)} journaux affichés sur {len(df_logs)} au total")

        if not filtered.empty:
            # Affichage amélioré avec des couleurs et des icônes
            for _, log in filtered.iterrows():
                color = {
                    "ERROR": "red",
                    "WARNING": "orange",
                    "INFO": "blue",
                    "DEBUG": "gray"
                }[log["level"]]
                
                icon = {
                    "ERROR": "❌",
                    "WARNING": "⚠️",
                    "INFO": "ℹ️",
                    "DEBUG": "🔍"
                }[log["level"]]

                st.markdown(
                    f"<div style='padding:8px; margin-bottom:8px; border-left:3px solid {color}; background-color:rgba(0,0,0,0.03); border-radius:4px;'>"
                    f"<span style='color:{color}; font-weight:bold;'>{icon} [{log['level']}]</span> "
                    f"<span style='color:gray;'>{log['timestamp'].strftime('%H:%M:%S')}</span> "
                    f"<span style='color:purple;'>[{log['component']}]</span> "
                    f"{log['message']}</div>",
                    unsafe_allow_html=True
                )
        else:
            st.warning("Aucun journal ne correspond aux filtres sélectionnés.")
    
    with tab2:
        st.subheader("Chronologie des journaux")
        
        # Préparer les données pour la chronologie
        timeline_events = []
        for _, log in df_logs.iterrows():
            event = {
                'timestamp': log['timestamp'],
                'event_type': log['level'],
                'description': f"[{log['component']}] {log['message']}"
            }
            timeline_events.append(event)
        
        # Créer et afficher la chronologie
        timeline_fig = create_timeline(timeline_events, "Chronologie des journaux d'exécution")
        render_plotly_chart(timeline_fig)
        
        # Créer un diagramme de Gantt pour les opérations avec durée
        st.subheader("Durée des opérations")
        
        # Filtrer les logs avec durée
        duration_logs = df_logs.dropna(subset=['duration'])
        
        if not duration_logs.empty:
            # Préparer les données pour le diagramme de Gantt
            gantt_tasks = []
            
            for _, log in duration_logs.iterrows():
                # Calculer l'heure de fin en ajoutant la durée
                start_time = log['timestamp']
                end_time = start_time + datetime.timedelta(seconds=log['duration'])
                
                task = {
                    'task': f"{log['component']}: {log['message'][:30]}{'...' if len(log['message']) > 30 else ''}",
                    'start': start_time,
                    'finish': end_time,
                    'resource': log['level']
                }
                gantt_tasks.append(task)
            
            # Créer et afficher le diagramme de Gantt
            gantt_fig = create_gantt_chart(gantt_tasks, "Durée des opérations")
            render_plotly_chart(gantt_fig)
        else:
            st.info("Aucune opération avec durée disponible.")
    
    with tab3:
        st.subheader("Statistiques des journaux")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution par niveau
            level_counts = df_logs['level'].value_counts().reset_index()
            level_counts.columns = ['Niveau', 'Nombre']
            
            st.write("Distribution par niveau de journal")
            fig = px.pie(level_counts, values='Nombre', names='Niveau', hole=.3,
                        color='Niveau',
                        color_discrete_map={
                            'INFO': 'blue',
                            'DEBUG': 'gray',
                            'WARNING': 'orange',
                            'ERROR': 'red'
                        })
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Distribution par composant
            component_counts = df_logs['component'].value_counts().reset_index()
            component_counts.columns = ['Composant', 'Nombre']
            
            st.write("Distribution par composant")
            st.bar_chart(component_counts.set_index('Composant'))
        
        # Distribution temporelle
        st.write("Distribution temporelle des journaux")
        try:
            # Grouper par intervalle de 5 minutes
            df_logs['time_group'] = df_logs['timestamp'].dt.floor('5min')
            time_counts = df_logs.groupby(['time_group', 'level']).size().reset_index()
            time_counts.columns = ['Temps', 'Niveau', 'Nombre']
            
            # Créer un graphique temporel avec couleurs par niveau
            fig = px.line(time_counts, x='Temps', y='Nombre', color='Niveau',
                        color_discrete_map={
                            'INFO': 'blue',
                            'DEBUG': 'gray',
                            'WARNING': 'orange',
                            'ERROR': 'red'
                        })
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.warning(f"Impossible de créer la distribution temporelle: {str(e)}")
    
    with tab4:
        st.subheader("Exportation des journaux")
        
        # Ajouter des options d'exportation
        create_export_section(df_logs, "logs_export")
        
        # Option pour télécharger uniquement les erreurs
        st.subheader("Exporter uniquement les erreurs")
        errors_df = df_logs[df_logs['level'] == 'ERROR']
        if not errors_df.empty:
            create_export_section(errors_df, "errors_export")
        else:
            st.success("Aucune erreur à exporter.")
    
    st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir des journaux de l'agent.")


def render_trace_view(target_dir: Path, is_system: bool = False):
    """
    Affiche la vue des traces dans le tableau de bord.

    Args:
        target_dir: Répertoire de l'agent ou du système à visualiser
        is_system: Indique si la cible est un système multi-agents
    """
    st.header("Vue des Traces")

    selected_agent = None
    if is_system:
        agents = get_available_agents(target_dir)
        if agents:
            selected_agent = st.selectbox("Sélectionner un agent", agents)
        else:
            st.warning("Aucun agent trouvé dans le système.")
            return

    trace_type = st.selectbox("Type de traces", ["Journaux d'exécution", "Événements", "Erreurs"])

    if trace_type == "Journaux d'exécution":
        render_execution_logs(target_dir, selected_agent)
    elif trace_type == "Événements":
        render_events(target_dir, selected_agent)
    elif trace_type == "Erreurs":
        render_errors(target_dir, selected_agent)
