"""
Utilitaires de visualisation avancée pour le tableau de bord Nüm Agents.

Ce module fournit des fonctions pour créer des visualisations interactives
et des graphiques avancés pour représenter les données des agents.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple


def create_timeline(events: List[Dict[str, Any]], 
                   title: str = "Chronologie des événements") -> go.Figure:
    """
    Crée une chronologie interactive des événements.
    
    Args:
        events: Liste de dictionnaires contenant les événements avec au moins 
               'timestamp', 'event_type', et 'description'
        title: Titre du graphique
        
    Returns:
        Figure Plotly pour la chronologie
    """
    if not events:
        return go.Figure()
    
    # Convertir en DataFrame
    df = pd.DataFrame(events)
    
    # Créer des couleurs en fonction du type d'événement
    color_map = {}
    for event_type in df['event_type'].unique():
        color_map[event_type] = None  # Plotly assignera automatiquement des couleurs
    
    # Créer la figure
    fig = px.timeline(
        df, 
        x_start="timestamp", 
        x_end="timestamp", 
        y="event_type",
        color="event_type",
        hover_name="description",
        title=title
    )
    
    # Personnaliser la mise en page
    fig.update_layout(
        xaxis_title="Temps",
        yaxis_title="Type d'événement",
        legend_title="Type d'événement",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig


def create_network_graph(nodes: List[Dict[str, Any]], 
                        edges: List[Dict[str, Any]],
                        title: str = "Graphe de réseau") -> go.Figure:
    """
    Crée un graphe de réseau interactif.
    
    Args:
        nodes: Liste de dictionnaires contenant les nœuds avec au moins 'id' et 'label'
        edges: Liste de dictionnaires contenant les arêtes avec au moins 'source', 'target' et 'weight'
        title: Titre du graphique
        
    Returns:
        Figure Plotly pour le graphe de réseau
    """
    if not nodes or not edges:
        return go.Figure()
    
    # Créer les positions des nœuds (layout circulaire simple)
    n = len(nodes)
    radius = 1
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    
    node_x = radius * np.cos(angles)
    node_y = radius * np.sin(angles)
    
    # Créer le graphe
    node_trace = go.Scatter(
        x=node_x, 
        y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=15,
            colorbar=dict(
                thickness=15,
                title='Importance du nœud',
                xanchor='left',
                titleside='right'
            )
        ),
        text=[node['label'] for node in nodes],
        textposition="top center"
    )
    
    # Ajouter les arêtes
    edge_x = []
    edge_y = []
    
    for edge in edges:
        source_idx = next(i for i, node in enumerate(nodes) if node['id'] == edge['source'])
        target_idx = next(i for i, node in enumerate(nodes) if node['id'] == edge['target'])
        
        x0, y0 = node_x[source_idx], node_y[source_idx]
        x1, y1 = node_x[target_idx], node_y[target_idx]
        
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
    
    edge_trace = go.Scatter(
        x=edge_x, 
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )
    
    # Créer la figure
    fig = go.Figure(data=[edge_trace, node_trace],
                 layout=go.Layout(
                    title=title,
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                ))
    
    return fig


def create_heatmap(data: pd.DataFrame, 
                  x_column: str, 
                  y_column: str, 
                  value_column: str,
                  title: str = "Carte de chaleur") -> go.Figure:
    """
    Crée une carte de chaleur interactive.
    
    Args:
        data: DataFrame contenant les données
        x_column: Nom de la colonne pour l'axe X
        y_column: Nom de la colonne pour l'axe Y
        value_column: Nom de la colonne pour les valeurs
        title: Titre du graphique
        
    Returns:
        Figure Plotly pour la carte de chaleur
    """
    if data.empty:
        return go.Figure()
    
    # Pivoter les données pour obtenir une matrice
    heatmap_data = data.pivot_table(
        values=value_column, 
        index=y_column, 
        columns=x_column, 
        aggfunc='mean'
    )
    
    # Créer la figure
    fig = px.imshow(
        heatmap_data,
        labels=dict(x=x_column, y=y_column, color=value_column),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        title=title,
        color_continuous_scale="Viridis"
    )
    
    # Personnaliser la mise en page
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig


def create_sankey_diagram(nodes: List[str], 
                         links: List[Dict[str, Any]],
                         title: str = "Diagramme de Sankey") -> go.Figure:
    """
    Crée un diagramme de Sankey interactif pour visualiser les flux.
    
    Args:
        nodes: Liste des noms de nœuds
        links: Liste de dictionnaires contenant 'source', 'target' et 'value'
        title: Titre du graphique
        
    Returns:
        Figure Plotly pour le diagramme de Sankey
    """
    if not nodes or not links:
        return go.Figure()
    
    # Créer le diagramme
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color="blue"
        ),
        link=dict(
            source=[nodes.index(link['source']) for link in links],
            target=[nodes.index(link['target']) for link in links],
            value=[link['value'] for link in links]
        )
    )])
    
    # Personnaliser la mise en page
    fig.update_layout(
        title=title,
        font=dict(size=10),
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig


def create_radar_chart(categories: List[str], 
                      values: List[float],
                      title: str = "Graphique radar") -> go.Figure:
    """
    Crée un graphique radar interactif.
    
    Args:
        categories: Liste des catégories (axes du radar)
        values: Liste des valeurs correspondantes
        title: Titre du graphique
        
    Returns:
        Figure Plotly pour le graphique radar
    """
    if not categories or not values:
        return go.Figure()
    
    # Créer le graphique radar
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='Valeurs'
    ))
    
    # Personnaliser la mise en page
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.2]
            )
        ),
        title=title,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig


def create_tree_map(labels: List[str], 
                   parents: List[str], 
                   values: List[float],
                   title: str = "Carte arborescente") -> go.Figure:
    """
    Crée une carte arborescente interactive.
    
    Args:
        labels: Liste des étiquettes pour chaque élément
        parents: Liste des parents pour chaque élément ('' pour les éléments racines)
        values: Liste des valeurs pour chaque élément
        title: Titre du graphique
        
    Returns:
        Figure Plotly pour la carte arborescente
    """
    if not labels or not parents or not values:
        return go.Figure()
    
    # Créer la carte arborescente
    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        textinfo="label+value+percent parent+percent entry",
        hoverinfo="label+value+percent parent+percent entry"
    ))
    
    # Personnaliser la mise en page
    fig.update_layout(
        title=title,
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig


def create_gantt_chart(tasks: List[Dict[str, Any]], 
                      title: str = "Diagramme de Gantt") -> go.Figure:
    """
    Crée un diagramme de Gantt interactif.
    
    Args:
        tasks: Liste de dictionnaires contenant 'task', 'start', 'finish', et 'resource'
        title: Titre du graphique
        
    Returns:
        Figure Plotly pour le diagramme de Gantt
    """
    if not tasks:
        return go.Figure()
    
    # Convertir en DataFrame
    df = pd.DataFrame(tasks)
    
    # Créer le diagramme de Gantt
    fig = px.timeline(
        df, 
        x_start="start", 
        x_end="finish", 
        y="task",
        color="resource",
        title=title
    )
    
    # Personnaliser la mise en page
    fig.update_layout(
        xaxis_title="Temps",
        yaxis_title="Tâche",
        legend_title="Ressource",
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    # Inverser l'axe Y pour que les tâches soient affichées de haut en bas
    fig.update_yaxes(autorange="reversed")
    
    return fig


def render_plotly_chart(fig: go.Figure, use_container_width: bool = True) -> None:
    """
    Affiche un graphique Plotly dans Streamlit avec gestion des erreurs.
    
    Args:
        fig: Figure Plotly à afficher
        use_container_width: Utiliser la largeur du conteneur
    """
    try:
        st.plotly_chart(fig, use_container_width=use_container_width)
    except Exception as e:
        st.error(f"Erreur lors de l'affichage du graphique: {str(e)}")
        st.info("Essayez de rafraîchir la page ou de vérifier les données d'entrée.")
