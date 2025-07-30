"""
Utilitaires de visualisation pour le tableau de bord Nüm Agents.

Ce module contient des fonctions pour générer des visualisations
à partir des données des agents.
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
from typing import Dict, List, Any, Optional, Tuple

def format_timestamp(timestamp: float) -> str:
    """
    Formate un timestamp Unix en chaîne de caractères lisible.
    
    Args:
        timestamp: Timestamp Unix
        
    Returns:
        Chaîne de caractères formatée
    """
    dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def create_time_series_chart(data: List[Dict[str, Any]], 
                           x_key: str, 
                           y_key: str, 
                           title: str = "",
                           x_label: str = "",
                           y_label: str = "") -> None:
    """
    Crée un graphique de série temporelle à partir de données.
    
    Args:
        data: Liste de dictionnaires contenant les données
        x_key: Clé pour l'axe X (généralement un timestamp)
        y_key: Clé pour l'axe Y
        title: Titre du graphique
        x_label: Étiquette de l'axe X
        y_label: Étiquette de l'axe Y
    """
    if not data:
        st.warning("Aucune donnée disponible pour le graphique.")
        return
    
    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(data)
    
    # Vérifier si les clés existent
    if x_key not in df.columns or y_key not in df.columns:
        st.warning(f"Clés {x_key} ou {y_key} non trouvées dans les données.")
        return
    
    # Si x_key est un timestamp, le convertir en datetime
    if "timestamp" in x_key.lower():
        df[x_key] = pd.to_datetime(df[x_key], unit='s')
    
    # Trier par x_key
    df = df.sort_values(by=x_key)
    
    # Créer le graphique
    st.line_chart(
        df,
        x=x_key,
        y=y_key
    )
    
    # Ajouter le titre et les étiquettes
    if title:
        st.write(f"**{title}**")

def create_bar_chart(data: Dict[str, float], 
                   title: str = "",
                   x_label: str = "",
                   y_label: str = "") -> None:
    """
    Crée un graphique à barres à partir de données.
    
    Args:
        data: Dictionnaire avec les clés comme étiquettes et les valeurs comme hauteurs
        title: Titre du graphique
        x_label: Étiquette de l'axe X
        y_label: Étiquette de l'axe Y
    """
    if not data:
        st.warning("Aucune donnée disponible pour le graphique.")
        return
    
    # Convertir les données en DataFrame pandas
    df = pd.DataFrame({
        'Category': list(data.keys()),
        'Value': list(data.values())
    })
    
    # Créer le graphique
    st.bar_chart(
        df,
        x='Category',
        y='Value'
    )
    
    # Ajouter le titre et les étiquettes
    if title:
        st.write(f"**{title}**")

def create_pie_chart(data: Dict[str, float], title: str = "") -> None:
    """
    Crée un graphique circulaire à partir de données.
    
    Args:
        data: Dictionnaire avec les clés comme étiquettes et les valeurs comme proportions
        title: Titre du graphique
    """
    if not data:
        st.warning("Aucune donnée disponible pour le graphique.")
        return
    
    # Ajouter le titre
    if title:
        st.write(f"**{title}**")
    
    # Créer le graphique
    fig = {
        'data': [{
            'values': list(data.values()),
            'labels': list(data.keys()),
            'type': 'pie',
        }],
    }
    st.plotly_chart(fig)

def create_gauge_chart(value: float, 
                     min_value: float = 0.0, 
                     max_value: float = 1.0, 
                     title: str = "",
                     color_ranges: Optional[List[Tuple[float, float, str]]] = None) -> None:
    """
    Crée un graphique de jauge à partir d'une valeur.
    
    Args:
        value: Valeur à afficher
        min_value: Valeur minimale
        max_value: Valeur maximale
        title: Titre du graphique
        color_ranges: Liste de tuples (min, max, couleur) pour les plages de couleurs
    """
    # Ajouter le titre
    if title:
        st.write(f"**{title}**")
    
    # Valeur par défaut pour color_ranges
    if color_ranges is None:
        color_ranges = [
            (min_value, max_value * 0.33, "red"),
            (max_value * 0.33, max_value * 0.67, "orange"),
            (max_value * 0.67, max_value, "green")
        ]
    
    # Déterminer la couleur en fonction de la valeur
    color = color_ranges[-1][2]  # Couleur par défaut
    for min_range, max_range, range_color in color_ranges:
        if min_range <= value <= max_range:
            color = range_color
            break
    
    # Créer le graphique de jauge
    fig = {
        'data': [{
            'type': 'indicator',
            'mode': 'gauge+number',
            'value': value,
            'gauge': {
                'axis': {'range': [min_value, max_value]},
                'bar': {'color': color},
                'steps': [
                    {'range': [min_range, max_range], 'color': range_color}
                    for min_range, max_range, range_color in color_ranges
                ],
            }
        }],
    }
    st.plotly_chart(fig)

def create_heatmap(data: List[List[float]], 
                 x_labels: List[str], 
                 y_labels: List[str], 
                 title: str = "") -> None:
    """
    Crée une carte de chaleur à partir de données.
    
    Args:
        data: Liste de listes contenant les valeurs
        x_labels: Étiquettes pour l'axe X
        y_labels: Étiquettes pour l'axe Y
        title: Titre du graphique
    """
    if not data or not x_labels or not y_labels:
        st.warning("Données incomplètes pour la carte de chaleur.")
        return
    
    # Ajouter le titre
    if title:
        st.write(f"**{title}**")
    
    # Créer la carte de chaleur
    fig = {
        'data': [{
            'z': data,
            'x': x_labels,
            'y': y_labels,
            'type': 'heatmap',
        }],
    }
    st.plotly_chart(fig)

def create_network_graph(nodes: List[Dict[str, Any]], 
                       edges: List[Dict[str, Any]], 
                       title: str = "") -> None:
    """
    Crée un graphe de réseau à partir de nœuds et d'arêtes.
    
    Args:
        nodes: Liste de dictionnaires représentant les nœuds
        edges: Liste de dictionnaires représentant les arêtes
        title: Titre du graphique
    """
    if not nodes or not edges:
        st.warning("Données incomplètes pour le graphe de réseau.")
        return
    
    # Ajouter le titre
    if title:
        st.write(f"**{title}**")
    
    # Créer le graphe de réseau
    # Note: Streamlit n'a pas de support natif pour les graphes de réseau
    # Nous utilisons donc une bibliothèque tierce comme Pyvis ou NetworkX
    
    # Pour l'instant, afficher un message
    st.info("Le graphe de réseau sera affiché ici. Nécessite l'installation de bibliothèques supplémentaires.")
    
    # Afficher les nœuds et les arêtes sous forme de tableaux
    st.write("**Nœuds:**")
    st.dataframe(pd.DataFrame(nodes))
    
    st.write("**Arêtes:**")
    st.dataframe(pd.DataFrame(edges))

def format_metrics_card(title: str, value: Any, delta: Optional[Any] = None, help_text: str = "") -> None:
    """
    Affiche une carte de métrique formatée.
    
    Args:
        title: Titre de la métrique
        value: Valeur de la métrique
        delta: Variation de la métrique (optionnel)
        help_text: Texte d'aide (optionnel)
    """
    if delta is not None:
        st.metric(
            label=title,
            value=value,
            delta=delta,
            help=help_text
        )
    else:
        st.metric(
            label=title,
            value=value,
            help=help_text
        )

def create_metrics_grid(metrics: List[Dict[str, Any]], cols: int = 3) -> None:
    """
    Affiche une grille de métriques.
    
    Args:
        metrics: Liste de dictionnaires contenant les métriques
        cols: Nombre de colonnes dans la grille
    """
    if not metrics:
        st.warning("Aucune métrique disponible.")
        return
    
    # Créer les colonnes
    columns = st.columns(cols)
    
    # Afficher chaque métrique dans une colonne
    for i, metric in enumerate(metrics):
        with columns[i % cols]:
            format_metrics_card(
                title=metric.get("title", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta"),
                help_text=metric.get("help", "")
            )

def format_log_entry(log: Dict[str, Any]) -> str:
    """
    Formate une entrée de journal pour l'affichage.
    
    Args:
        log: Dictionnaire représentant une entrée de journal
        
    Returns:
        Chaîne de caractères formatée
    """
    level = log.get("level", "")
    timestamp = log.get("timestamp", "")
    component = log.get("component", "")
    message = log.get("message", "")
    
    # Déterminer la couleur en fonction du niveau
    if level == "ERROR":
        color = "red"
    elif level == "WARNING":
        color = "orange"
    elif level == "INFO":
        color = "blue"
    else:  # DEBUG
        color = "gray"
    
    # Formater le timestamp
    if isinstance(timestamp, (int, float)):
        timestamp_str = format_timestamp(timestamp)
    elif isinstance(timestamp, datetime.datetime):
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    else:
        timestamp_str = str(timestamp)
    
    # Formater l'entrée de journal
    return (
        f"<div style='padding: 5px; margin-bottom: 5px; border-left: 3px solid {color};'>"
        f"<span style='color: {color}; font-weight: bold;'>[{level}]</span> "
        f"<span style='color: gray;'>{timestamp_str}</span> "
        f"<span style='color: purple;'>[{component}]</span> "
        f"{message}"
        f"</div>"
    )

def display_logs(logs: List[Dict[str, Any]], max_logs: int = 100) -> None:
    """
    Affiche une liste de journaux.
    
    Args:
        logs: Liste de dictionnaires représentant des entrées de journal
        max_logs: Nombre maximum de journaux à afficher
    """
    if not logs:
        st.info("Aucun journal disponible.")
        return
    
    # Limiter le nombre de journaux
    logs = logs[:max_logs]
    
    # Afficher chaque journal
    for log in logs:
        st.markdown(format_log_entry(log), unsafe_allow_html=True)

def create_status_indicator(status: str) -> None:
    """
    Affiche un indicateur de statut.
    
    Args:
        status: Statut à afficher (running, stopped, error, etc.)
    """
    # Déterminer la couleur en fonction du statut
    if status.lower() in ["running", "active", "online"]:
        color = "green"
        emoji = "🟢"
    elif status.lower() in ["stopped", "inactive", "offline"]:
        color = "gray"
        emoji = "⚪"
    elif status.lower() in ["error", "failed"]:
        color = "red"
        emoji = "🔴"
    elif status.lower() in ["warning", "degraded"]:
        color = "orange"
        emoji = "🟠"
    else:
        color = "blue"
        emoji = "🔵"
    
    # Afficher l'indicateur
    st.markdown(
        f"<span style='color: {color}; font-weight: bold;'>{emoji} {status.upper()}</span>",
        unsafe_allow_html=True
    )
