"""
Application de tableau de bord pour Nüm Agents SDK.

Cette application fournit une interface web pour visualiser et surveiller
le fonctionnement des agents, leurs graphes logiques, leur mémoire,
leurs métriques et leurs traces d'exécution.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Optional, Union, List, Dict, Any

# Import des composants
from num_agents.dashboard.components.agent_view import render_agent_view
from num_agents.dashboard.components.graph_view import render_graph_view
from num_agents.dashboard.components.memory_view import render_memory_view
from num_agents.dashboard.components.metrics_view import render_metrics_view
from num_agents.dashboard.components.trace_view import render_trace_view

# Import des utilitaires
from num_agents.dashboard.utils.styling import set_page_config, apply_custom_css, create_header, create_footer


def run_dashboard(
    target_dir: Path,
    is_system: bool = False,
    port: int = 8080,
    debug: bool = False,
    generate_sample_data: bool = False
):
    """
    Lance l'application de tableau de bord.
    
    Args:
        target_dir: Répertoire de l'agent ou du système à surveiller
        is_system: Indique si la cible est un système multi-agents
        port: Port pour le serveur de tableau de bord
        debug: Active le mode débogage
        generate_sample_data: Génère des données d'exemple pour la démonstration
    """
    try:
        import streamlit as st
    except ImportError:
        print("Streamlit n'est pas installé. Installation en cours...")
        os.system("pip install streamlit>=1.30.0")
        import streamlit as st
    
    # Génération de données d'exemple si demandé
    if generate_sample_data:
        print("Génération de données d'exemple pour la démonstration...")
        try:
            from num_agents.dashboard.data_providers.metrics_provider import generate_sample_metrics
            from num_agents.dashboard.data_providers.trace_provider import generate_sample_traces
            
            # Créer les répertoires nécessaires
            if is_system:
                from num_agents.dashboard.data_providers.agent_provider import get_agent_directories
                agent_dirs = get_agent_directories(target_dir)
                for agent_dir in agent_dirs:
                    generate_sample_metrics(agent_dir)
                    generate_sample_traces(agent_dir)
            else:
                generate_sample_metrics(target_dir)
                generate_sample_traces(target_dir)
                
            print("Données d'exemple générées avec succès.")
        except Exception as e:
            print(f"Erreur lors de la génération des données d'exemple: {e}")
    
    # Configuration de Streamlit
    os.environ["STREAMLIT_SERVER_PORT"] = str(port)
    if debug:
        os.environ["STREAMLIT_LOGGER_LEVEL"] = "debug"
    
    # Lancement de l'application Streamlit
    sys.argv = ["streamlit", "run", __file__, "--", 
                f"--target-dir={target_dir}", 
                f"--is-system={'true' if is_system else 'false'}"]
    
    import streamlit.web.bootstrap as bootstrap
    bootstrap.run(__file__, "", [], [])


def main():
    """Point d'entrée principal pour l'application Streamlit."""
    try:
        import streamlit as st
        import pandas as pd
        import numpy as np
    except ImportError:
        print("Dépendances manquantes. Veuillez installer les packages requis avec:")
        print("pip install streamlit>=1.30.0 pandas numpy")
        sys.exit(1)
    
    # Configuration de la page
    set_page_config(
        title="Nüm Agents Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Appliquer les styles personnalisés
    apply_custom_css()
    
    # Créer l'en-tête
    create_header("Nüm Agents Dashboard", "Visualisation et surveillance des agents intelligents", "🧠")
    
    # Analyse des arguments de ligne de commande
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-dir", type=str, required=True)
    parser.add_argument("--is-system", type=str, required=True)
    args = parser.parse_args()
    
    target_dir = Path(args.target_dir)
    is_system = args.is_system.lower() == "true"
    
    # Informations sur la cible
    st.sidebar.info(f"Visualisation de {'système multi-agents' if is_system else 'agent'} dans {target_dir}")
    
    # Navigation dans la barre latérale
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Sélectionner une vue",
        ["Agents", "Graphes Logiques", "Mémoire", "Métriques", "Traces"]
    )
    
    # Rendu de la vue sélectionnée
    if page == "Agents":
        render_agent_view(target_dir, is_system)
        
        # Placeholder pour la liste des agents
        st.subheader("Agents actifs")
        agents = ["Agent1", "Agent2", "Agent3"]  # À remplacer par la vraie liste des agents
        for agent in agents:
            st.write(f"- {agent}")
        
    elif page == "Graphes Logiques":
        render_graph_view(target_dir, is_system)
    
    elif page == "Mémoire":
        render_memory_view(target_dir, is_system)
    
    elif page == "Métriques":
        render_metrics_view(target_dir, is_system)
    
    elif page == "Traces":
        render_trace_view(target_dir, is_system)
        
    # Ajouter un pied de page
    create_footer()


if __name__ == "__main__":
    main()
