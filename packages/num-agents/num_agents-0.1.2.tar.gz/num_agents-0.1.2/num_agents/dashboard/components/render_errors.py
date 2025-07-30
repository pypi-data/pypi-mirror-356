"""
Fonction de rendu des erreurs pour le tableau de bord.

Ce module fournit la fonction render_errors pour visualiser les erreurs
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


def render_errors(target_dir: Path, agent_name: Optional[str] = None) -> None:
    """
    Affiche les erreurs d'un agent avec des visualisations avancées.

    Args:
        target_dir: Répertoire de l'agent ou du système
        agent_name: Nom de l'agent à visualiser (pour les systèmes multi-agents)
    """
    st.subheader("Erreurs de l'agent")

    # Générer des données d'exemple pour les erreurs
    now = datetime.datetime.now()
    error_types = ["ValidationError", "RuntimeError", "ConnectionError", "TimeoutError", "ValueError"]
    error_modules = ["core", "llm", "memory", "reasoning", "eventbus", "scheduler"]
    error_levels = ["CRITICAL", "ERROR", "WARNING"]
    
    errors = []
    for i in range(20):  # Générer 20 erreurs d'exemple
        timestamp = now - datetime.timedelta(hours=random.randint(1, 24), minutes=random.randint(0, 59))
        error_type = random.choice(error_types)
        module = random.choice(error_modules)
        level = random.choices(error_levels, weights=[0.1, 0.6, 0.3])[0]
        
        # Générer un message d'erreur en fonction du type
        if error_type == "ValidationError":
            message = f"Échec de validation des données dans le module {module}"
            details = f"Détails: Le champ '{random.choice(['input', 'output', 'config'])}' est manquant ou invalide."
        elif error_type == "RuntimeError":
            message = f"Erreur d'exécution dans le module {module}"
            details = f"Détails: {random.choice(['Mémoire insuffisante', 'Condition de course détectée', 'État inattendu'])}"
        elif error_type == "ConnectionError":
            message = f"Échec de connexion au service {random.choice(['LLM', 'base de données', 'API externe'])}"
            details = f"Détails: Impossible d'établir une connexion après {random.randint(1, 5)} tentatives"
        elif error_type == "TimeoutError":
            message = f"Délai d'attente dépassé pour la requête vers {random.choice(['service externe', 'API', 'base de données'])}"
            details = f"Détails: Aucune réponse après {random.randint(5, 30)} secondes"
        else:  # ValueError
            message = f"Valeur invalide dans le module {module}"
            details = f"Détails: La valeur '{random.choice(['None', 'null', 'undefined', ''])}' n'est pas valide pour ce champ"
        
        # Ajouter une trace de pile factice
        traceback = (
            f"Traceback (most recent call last):\n"
            f'  File "/path/to/module/{module}/file.py", line {random.randint(10, 100)}, in function_{random.randint(1, 10)}\n'
            f'    raise {error_type}("{message}")\n'
            f"{error_type}: {message}"
        )
        
        errors.append({
            "timestamp": timestamp,
            "type": error_type,
            "module": module,
            "level": level,
            "message": message,
            "details": details,
            "traceback": traceback,
            "agent": agent_name or "main_agent"
        })
    
    # Trier les erreurs par ordre chronologique inverse
    errors.sort(key=lambda x: x["timestamp"], reverse=True)
    df_errors = pd.DataFrame(errors)
    
    # Créer des onglets pour différentes vues
    tab1, tab2, tab3 = st.tabs(["Liste", "Détails", "Statistiques"])
    
    with tab1:
        # Filtres interactifs
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_types = st.multiselect("Filtrer par type", error_types, default=error_types)
        with col2:
            selected_modules = st.multiselect("Filtrer par module", error_modules, default=error_modules)
        with col3:
            selected_levels = st.multiselect("Filtrer par niveau", error_levels, default=error_levels)
        
        # Appliquer les filtres
        filtered = df_errors[
            (df_errors["type"].isin(selected_types)) &
            (df_errors["module"].isin(selected_modules)) &
            (df_errors["level"].isin(selected_levels))
        ]
        
        # Afficher le nombre d'erreurs filtrées
        st.info(f"{len(filtered)} erreurs affichées sur {len(df_errors)} au total")
        
        if not filtered.empty:
            # Afficher les erreurs avec mise en forme
            for _, error in filtered.iterrows():
                # Définir la couleur en fonction du niveau d'erreur
                color = {
                    "CRITICAL": "#d32f2f",
                    "ERROR": "#f44336",
                    "WARNING": "#ff9800"
                }.get(error["level"], "gray")
                
                # Afficher l'erreur avec mise en forme
                with st.expander(f"{error['type']}: {error['message']}"):
                    st.markdown(f"**Niveau:** <span style='color:{color};'>{error['level']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Module:** `{error['module']}`")
                    st.markdown(f"**Date:** {error['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                    st.markdown(f"**Détails:** {error['details']}")
                    
                    # Afficher la trace de pile dans une zone de texte défilante
                    st.markdown("**Trace de pile:**")
                    st.code(error['traceback'], language='python')
        else:
            st.success("Aucune erreur ne correspond aux filtres sélectionnés.")
    
    with tab2:
        st.subheader("Détails des erreurs")
        
        if not df_errors.empty:
            # Afficher un graphique de répartition des erreurs
            st.write("Répartition des erreurs")
            
            # Graphique à barres empilées par type et niveau
            error_dist = df_errors.groupby(['type', 'level']).size().reset_index()
            error_dist.columns = ['Type', 'Niveau', 'Nombre']
            
            fig = px.bar(error_dist, x='Type', y='Nombre', color='Niveau',
                        title='Répartition des erreurs par type et niveau',
                        color_discrete_map={
                            'CRITICAL': '#d32f2f',
                            'ERROR': '#f44336',
                            'WARNING': '#ff9800'
                        })
            st.plotly_chart(fig, use_container_width=True)
            
            # Graphique circulaire des modules les plus problématiques
            st.write("Modules les plus problématiques")
            module_counts = df_errors['module'].value_counts().reset_index()
            module_counts.columns = ['Module', 'Nombre']
            
            fig = px.pie(module_counts, values='Nombre', names='Module',
                        title='Répartition des erreurs par module',
                        color_discrete_sequence=px.colors.sequential.Reds_r)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Statistiques des erreurs")
        
        if not df_errors.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                # Statistiques de base
                st.metric("Nombre total d'erreurs", len(df_errors))
                st.metric("Taux d'erreurs critiques", 
                         f"{len(df_errors[df_errors['level'] == 'CRITICAL']) / len(df_errors) * 100:.1f}%")
                
                # Dernière erreur
                last_error = df_errors.iloc[0]
                st.metric("Dernière erreur", 
                         f"{last_error['type']} - {last_error['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            
            with col2:
                # Distribution temporelle des erreurs
                st.write("Évolution des erreurs dans le temps")
                try:
                    # Grouper par jour
                    df_errors['date'] = df_errors['timestamp'].dt.date
                    date_counts = df_errors.groupby(['date', 'level']).size().reset_index()
                    date_counts.columns = ['Date', 'Niveau', 'Nombre']
                    
                    fig = px.line(date_counts, x='Date', y='Nombre', color='Niveau',
                                title='Évolution des erreurs dans le temps',
                                color_discrete_map={
                                    'CRITICAL': '#d32f2f',
                                    'ERROR': '#f44336',
                                    'WARNING': '#ff9800'
                                })
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.warning(f"Impossible de créer la distribution temporelle: {str(e)}")
        else:
            st.info("Aucune donnée d'erreur disponible pour l'analyse statistique.")
    
    # Section d'exportation
    st.subheader("Exportation des erreurs")
    create_export_section(df_errors, "errors_export")
    
    st.info("Note: Ces données sont des exemples. Dans une implémentation complète, elles seraient chargées dynamiquement à partir des journaux de l'agent.")
