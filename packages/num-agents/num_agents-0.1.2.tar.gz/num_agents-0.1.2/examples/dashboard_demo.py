#!/usr/bin/env python3
"""
Exemple de démonstration du tableau de bord Nüm Agents.

Ce script lance le tableau de bord avec des données d'exemple générées
pour démontrer les fonctionnalités de visualisation et de surveillance.
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au chemin Python pour permettre l'importation
sys.path.insert(0, str(Path(__file__).parent.parent))

from num_agents.dashboard.app import run_dashboard


def main():
    """Point d'entrée principal pour la démonstration du tableau de bord."""
    # Répertoire de démonstration pour un agent unique
    agent_dir = Path(__file__).parent / "demo_agent"
    
    # Créer le répertoire s'il n'existe pas
    agent_dir.mkdir(exist_ok=True)
    
    print(f"Lancement du tableau de bord de démonstration pour l'agent dans {agent_dir}")
    print("Des données d'exemple seront générées automatiquement.")
    print("Accédez au tableau de bord à l'adresse http://localhost:8501 une fois lancé.")
    
    # Lancer le tableau de bord avec génération de données d'exemple
    run_dashboard(
        target_dir=agent_dir,
        is_system=False,
        port=8501,
        debug=True,
        generate_sample_data=True
    )


if __name__ == "__main__":
    main()
