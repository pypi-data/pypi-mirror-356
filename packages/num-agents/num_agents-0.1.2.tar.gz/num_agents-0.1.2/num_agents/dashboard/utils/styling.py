"""
Utilitaires de style pour le tableau de bord Nüm Agents.

Ce module contient des fonctions pour gérer les thèmes et les styles
du tableau de bord Streamlit.
"""

import streamlit as st
from typing import Dict, Any, Optional

def set_page_config(title: str = "Nüm Agents Dashboard", 
                   layout: str = "wide",
                   initial_sidebar_state: str = "expanded") -> None:
    """
    Configure les paramètres de la page Streamlit.
    
    Args:
        title: Titre de la page
        layout: Disposition de la page ('wide' ou 'centered')
        initial_sidebar_state: État initial de la barre latérale ('expanded' ou 'collapsed')
    """
    st.set_page_config(
        page_title=title,
        page_icon="🧠",
        layout=layout,
        initial_sidebar_state=initial_sidebar_state
    )

def apply_custom_css() -> None:
    """
    Applique des styles CSS personnalisés à l'application Streamlit.
    """
    # Styles pour améliorer l'apparence du tableau de bord
    custom_css = """
    <style>
        /* Styles généraux */
        .main {
            background-color: #f8f9fa;
        }
        
        /* En-têtes */
        h1, h2, h3 {
            color: #1e3a8a;
        }
        
        /* Cartes */
        div[data-testid="stMetric"] {
            background-color: white;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Graphiques */
        .stPlotlyChart {
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Tableaux */
        .stDataFrame {
            border-radius: 10px;
            overflow: hidden;
        }
        
        /* Onglets */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #f1f5f9;
            border-radius: 4px 4px 0px 0px;
            padding: 10px 20px;
            border: none;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #3b82f6;
            color: white;
        }
        
        /* Boutons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Barre latérale */
        .css-1d391kg {
            background-color: #1e293b;
        }
        
        /* Séparateurs */
        hr {
            margin: 20px 0;
            border: none;
            height: 1px;
            background-color: #e2e8f0;
        }
    </style>
    """
    
    # Appliquer les styles
    st.markdown(custom_css, unsafe_allow_html=True)

def create_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None) -> None:
    """
    Crée un en-tête pour une page ou une section.
    
    Args:
        title: Titre principal
        subtitle: Sous-titre (optionnel)
        icon: Icône (emoji) à afficher avant le titre (optionnel)
    """
    # Afficher l'icône et le titre
    if icon:
        st.markdown(f"# {icon} {title}")
    else:
        st.markdown(f"# {title}")
    
    # Afficher le sous-titre
    if subtitle:
        st.markdown(f"*{subtitle}*")
    
    # Ajouter un séparateur
    st.markdown("---")

def create_footer() -> None:
    """
    Crée un pied de page pour l'application.
    """
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; padding: 10px;">
            <p>Nüm Agents Dashboard | Développé par Lionel TAGNE</p>
            <p>© 2025 Tous droits réservés</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_info_box(message: str, type_: str = "info") -> None:
    """
    Crée une boîte d'information avec un style personnalisé.
    
    Args:
        message: Message à afficher
        type_: Type de boîte (info, success, warning, error)
    """
    if type_ == "info":
        st.info(message)
    elif type_ == "success":
        st.success(message)
    elif type_ == "warning":
        st.warning(message)
    elif type_ == "error":
        st.error(message)
    else:
        st.write(message)

def create_card(title: str, content: str, icon: Optional[str] = None) -> None:
    """
    Crée une carte avec un titre et un contenu.
    
    Args:
        title: Titre de la carte
        content: Contenu de la carte
        icon: Icône (emoji) à afficher avant le titre (optionnel)
    """
    # Créer la carte
    with st.container():
        # Afficher le titre avec l'icône
        if icon:
            st.markdown(f"### {icon} {title}")
        else:
            st.markdown(f"### {title}")
        
        # Afficher le contenu
        st.markdown(content)
        
        # Ajouter un peu d'espace
        st.write("")

def create_tabs(tabs: Dict[str, Any]) -> None:
    """
    Crée un ensemble d'onglets.
    
    Args:
        tabs: Dictionnaire avec les noms d'onglets comme clés et les fonctions de rendu comme valeurs
    """
    if not tabs:
        st.warning("Aucun onglet défini.")
        return
    
    # Créer les onglets
    tab_objects = st.tabs(list(tabs.keys()))
    
    # Afficher le contenu de chaque onglet
    for i, (name, render_func) in enumerate(tabs.items()):
        with tab_objects[i]:
            render_func()

def create_sidebar_navigation(pages: Dict[str, Any]) -> str:
    """
    Crée une navigation dans la barre latérale.
    
    Args:
        pages: Dictionnaire avec les noms de pages comme clés et les fonctions de rendu comme valeurs
        
    Returns:
        Nom de la page sélectionnée
    """
    if not pages:
        st.sidebar.warning("Aucune page définie.")
        return ""
    
    # Ajouter un titre à la barre latérale
    st.sidebar.title("Navigation")
    
    # Créer un sélecteur de page
    selected_page = st.sidebar.radio("", list(pages.keys()))
    
    # Ajouter un séparateur
    st.sidebar.markdown("---")
    
    return selected_page

def create_theme_selector() -> Dict[str, Any]:
    """
    Crée un sélecteur de thème dans la barre latérale.
    
    Returns:
        Dictionnaire contenant les paramètres du thème sélectionné
    """
    # Définir les thèmes disponibles
    themes = {
        "Clair": {
            "primary_color": "#3b82f6",
            "background_color": "#f8f9fa",
            "text_color": "#1e293b",
            "font": "sans-serif"
        },
        "Sombre": {
            "primary_color": "#60a5fa",
            "background_color": "#1e293b",
            "text_color": "#f8fafc",
            "font": "sans-serif"
        },
        "Neutre": {
            "primary_color": "#6b7280",
            "background_color": "#f3f4f6",
            "text_color": "#1f2937",
            "font": "sans-serif"
        }
    }
    
    # Ajouter un sélecteur de thème dans la barre latérale
    st.sidebar.subheader("Thème")
    selected_theme = st.sidebar.selectbox("", list(themes.keys()))
    
    # Retourner les paramètres du thème sélectionné
    return themes[selected_theme]
