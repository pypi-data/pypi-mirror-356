"""
Utilitaires d'interactivité pour le tableau de bord Nüm Agents.

Ce module fournit des fonctions pour créer des éléments interactifs
permettant de modifier les paramètres des agents en temps réel.
"""

import streamlit as st
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union, Callable
import os


def load_agent_config(config_path: Path) -> Dict[str, Any]:
    """
    Charge la configuration d'un agent depuis un fichier YAML.
    
    Args:
        config_path: Chemin vers le fichier de configuration
        
    Returns:
        Dictionnaire de configuration
    """
    try:
        if not config_path.exists():
            st.error(f"Le fichier de configuration n'existe pas: {config_path}")
            return {}
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        return config or {}
    
    except Exception as e:
        st.error(f"Erreur lors du chargement de la configuration: {str(e)}")
        return {}


def save_agent_config(config: Dict[str, Any], config_path: Path) -> bool:
    """
    Sauvegarde la configuration d'un agent dans un fichier YAML.
    
    Args:
        config: Dictionnaire de configuration
        config_path: Chemin vers le fichier de configuration
        
    Returns:
        True si la sauvegarde a réussi, False sinon
    """
    try:
        # Créer le répertoire parent s'il n'existe pas
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
        
        return True
    
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
        return False


def create_config_editor(config_path: Path, 
                        on_save: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
    """
    Crée un éditeur de configuration interactif.
    
    Args:
        config_path: Chemin vers le fichier de configuration
        on_save: Fonction à appeler après la sauvegarde
        
    Returns:
        Configuration modifiée
    """
    # Charger la configuration
    config = load_agent_config(config_path)
    
    if not config:
        st.warning(f"Configuration vide ou invalide: {config_path}")
        return {}
    
    # Créer un éditeur de texte pour la configuration
    st.subheader("Éditeur de configuration")
    
    # Convertir la configuration en YAML pour l'édition
    config_yaml = yaml.dump(config, default_flow_style=False)
    
    # Créer une zone de texte pour éditer la configuration
    edited_config_yaml = st.text_area(
        "Configuration YAML",
        value=config_yaml,
        height=300,
        key="config_editor"
    )
    
    # Bouton pour sauvegarder les modifications
    if st.button("Sauvegarder les modifications"):
        try:
            # Convertir le YAML édité en dictionnaire
            edited_config = yaml.safe_load(edited_config_yaml)
            
            # Sauvegarder la configuration modifiée
            if save_agent_config(edited_config, config_path):
                st.success(f"Configuration sauvegardée avec succès: {config_path}")
                
                # Appeler la fonction de callback si elle est fournie
                if on_save:
                    on_save(edited_config)
                
                return edited_config
            else:
                st.error("Échec de la sauvegarde de la configuration.")
        
        except Exception as e:
            st.error(f"Erreur lors de l'analyse du YAML: {str(e)}")
    
    return config


def create_parameter_editor(config: Dict[str, Any], 
                           section_key: str,
                           title: str = "Paramètres",
                           on_change: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
    """
    Crée un éditeur de paramètres interactif pour une section spécifique de la configuration.
    
    Args:
        config: Dictionnaire de configuration
        section_key: Clé de la section à éditer
        title: Titre de la section
        on_change: Fonction à appeler après un changement
        
    Returns:
        Section de configuration modifiée
    """
    if section_key not in config:
        st.warning(f"Section '{section_key}' non trouvée dans la configuration.")
        return {}
    
    section = config[section_key]
    
    if not isinstance(section, dict):
        st.warning(f"La section '{section_key}' n'est pas un dictionnaire.")
        return section
    
    # Créer un formulaire pour éditer les paramètres
    st.subheader(title)
    
    # Créer une copie de la section pour les modifications
    edited_section = section.copy()
    
    # Créer des widgets pour chaque paramètre
    for key, value in section.items():
        if isinstance(value, bool):
            edited_section[key] = st.checkbox(key, value)
        
        elif isinstance(value, int):
            edited_section[key] = st.number_input(key, value=value, step=1)
        
        elif isinstance(value, float):
            edited_section[key] = st.number_input(key, value=value, format="%.5f")
        
        elif isinstance(value, str):
            if key.lower() in ["model", "modèle"]:
                # Pour les modèles, créer une liste déroulante avec des options communes
                models = ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet", "gemini-1.5-pro", "gemini-1.5-flash", value]
                edited_section[key] = st.selectbox(key, options=list(set(models)))
            else:
                edited_section[key] = st.text_input(key, value)
        
        elif isinstance(value, list):
            if all(isinstance(item, str) for item in value):
                # Pour les listes de chaînes, créer un champ de texte avec séparateur
                items_str = ", ".join(value)
                new_items_str = st.text_input(key, items_str)
                edited_section[key] = [item.strip() for item in new_items_str.split(",") if item.strip()]
            else:
                st.info(f"Le paramètre '{key}' est une liste complexe qui ne peut pas être éditée directement.")
        
        elif isinstance(value, dict):
            st.info(f"Le paramètre '{key}' est un dictionnaire qui ne peut pas être édité directement.")
        
        else:
            st.info(f"Le paramètre '{key}' est de type {type(value).__name__} et ne peut pas être édité directement.")
    
    # Appeler la fonction de callback si des modifications ont été apportées
    if edited_section != section and on_change:
        on_change(edited_section)
    
    return edited_section


def create_agent_control_panel(agent_dir: Path) -> None:
    """
    Crée un panneau de contrôle pour un agent.
    
    Args:
        agent_dir: Répertoire de l'agent
    """
    st.subheader("Panneau de contrôle de l'agent")
    
    # Vérifier si l'agent est en cours d'exécution
    pid_file = agent_dir / "agent.pid"
    is_running = pid_file.exists()
    
    # Afficher le statut de l'agent
    status_col, action_col = st.columns(2)
    
    with status_col:
        if is_running:
            try:
                with open(pid_file, 'r') as f:
                    pid = f.read().strip()
                st.success(f"Agent en cours d'exécution (PID: {pid})")
            except:
                st.success("Agent en cours d'exécution")
        else:
            st.warning("Agent arrêté")
    
    with action_col:
        if is_running:
            if st.button("Arrêter l'agent"):
                try:
                    with open(pid_file, 'r') as f:
                        pid = f.read().strip()
                    
                    # Tenter d'arrêter l'agent
                    os.kill(int(pid), 15)  # Signal SIGTERM
                    pid_file.unlink(missing_ok=True)
                    st.success("Agent arrêté avec succès.")
                except Exception as e:
                    st.error(f"Erreur lors de l'arrêt de l'agent: {str(e)}")
        else:
            if st.button("Démarrer l'agent"):
                try:
                    # Vérifier si le script principal existe
                    main_script = agent_dir / "main.py"
                    if not main_script.exists():
                        st.error(f"Script principal non trouvé: {main_script}")
                        return
                    
                    # Démarrer l'agent en arrière-plan
                    import subprocess
                    process = subprocess.Popen(
                        ["python", str(main_script)],
                        cwd=str(agent_dir),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        start_new_session=True
                    )
                    
                    # Sauvegarder le PID
                    with open(pid_file, 'w') as f:
                        f.write(str(process.pid))
                    
                    st.success(f"Agent démarré avec succès (PID: {process.pid}).")
                except Exception as e:
                    st.error(f"Erreur lors du démarrage de l'agent: {str(e)}")
    
    # Afficher les options de configuration
    st.subheader("Configuration de l'agent")
    
    # Vérifier si le fichier de configuration existe
    config_path = agent_dir / "agent.yaml"
    if not config_path.exists():
        st.warning(f"Fichier de configuration non trouvé: {config_path}")
        return
    
    # Charger la configuration
    config = load_agent_config(config_path)
    
    # Créer des onglets pour les différentes sections de configuration
    tabs = ["Général", "LLM", "Mémoire", "Configuration avancée"]
    tab1, tab2, tab3, tab4 = st.tabs(tabs)
    
    with tab1:
        # Éditer les paramètres généraux
        if "name" in config:
            st.text_input("Nom de l'agent", value=config["name"], disabled=True)
        
        if "description" in config:
            st.text_area("Description", value=config["description"])
        
        if "universes" in config:
            universes_str = ", ".join(config["universes"])
            st.text_input("Univers", value=universes_str, disabled=True)
    
    with tab2:
        # Éditer les paramètres du LLM
        if "llm" in config:
            llm_config = create_parameter_editor(
                config, 
                "llm", 
                "Paramètres du modèle de langage",
                lambda edited: save_agent_config({**config, "llm": edited}, config_path)
            )
    
    with tab3:
        # Éditer les paramètres de mémoire
        if "memory" in config:
            memory_config = create_parameter_editor(
                config, 
                "memory", 
                "Paramètres de mémoire",
                lambda edited: save_agent_config({**config, "memory": edited}, config_path)
            )
    
    with tab4:
        # Éditeur de configuration avancé
        create_config_editor(config_path)


def create_system_control_panel(system_dir: Path) -> None:
    """
    Crée un panneau de contrôle pour un système multi-agents.
    
    Args:
        system_dir: Répertoire du système
    """
    st.subheader("Panneau de contrôle du système")
    
    # Vérifier si le système est en cours d'exécution
    pid_file = system_dir / "system.pid"
    is_running = pid_file.exists()
    
    # Afficher le statut du système
    status_col, action_col = st.columns(2)
    
    with status_col:
        if is_running:
            try:
                with open(pid_file, 'r') as f:
                    pid = f.read().strip()
                st.success(f"Système en cours d'exécution (PID: {pid})")
            except:
                st.success("Système en cours d'exécution")
        else:
            st.warning("Système arrêté")
    
    with action_col:
        if is_running:
            if st.button("Arrêter le système"):
                try:
                    with open(pid_file, 'r') as f:
                        pid = f.read().strip()
                    
                    # Tenter d'arrêter le système
                    os.kill(int(pid), 15)  # Signal SIGTERM
                    pid_file.unlink(missing_ok=True)
                    st.success("Système arrêté avec succès.")
                except Exception as e:
                    st.error(f"Erreur lors de l'arrêt du système: {str(e)}")
        else:
            if st.button("Démarrer le système"):
                try:
                    # Vérifier si le script principal existe
                    main_script = system_dir / "main.py"
                    if not main_script.exists():
                        st.error(f"Script principal non trouvé: {main_script}")
                        return
                    
                    # Démarrer le système en arrière-plan
                    import subprocess
                    process = subprocess.Popen(
                        ["python", str(main_script)],
                        cwd=str(system_dir),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        start_new_session=True
                    )
                    
                    # Sauvegarder le PID
                    with open(pid_file, 'w') as f:
                        f.write(str(process.pid))
                    
                    st.success(f"Système démarré avec succès (PID: {process.pid}).")
                except Exception as e:
                    st.error(f"Erreur lors du démarrage du système: {str(e)}")
    
    # Afficher les agents du système
    st.subheader("Agents du système")
    
    # Rechercher les répertoires d'agents
    agent_dirs = [d for d in system_dir.iterdir() if d.is_dir() and (d / "agent.yaml").exists()]
    
    if not agent_dirs:
        st.info("Aucun agent trouvé dans le système.")
        return
    
    # Créer un sélecteur d'agent
    agent_names = [d.name for d in agent_dirs]
    selected_agent = st.selectbox("Sélectionner un agent", agent_names)
    
    # Afficher le panneau de contrôle de l'agent sélectionné
    selected_agent_dir = system_dir / selected_agent
    create_agent_control_panel(selected_agent_dir)
