"""
Utilitaires d'exportation de données pour le tableau de bord Nüm Agents.

Ce module fournit des fonctions pour exporter les données du tableau de bord
dans différents formats (CSV, JSON, Excel).
"""

import streamlit as st
import pandas as pd
import json
import io
import base64
from typing import Dict, List, Any, Union, Optional
from pathlib import Path


def dataframe_to_csv(df: pd.DataFrame) -> str:
    """
    Convertit un DataFrame en chaîne CSV.
    
    Args:
        df: DataFrame à convertir
        
    Returns:
        Chaîne CSV
    """
    return df.to_csv(index=False)


def dataframe_to_json(df: pd.DataFrame) -> str:
    """
    Convertit un DataFrame en chaîne JSON.
    
    Args:
        df: DataFrame à convertir
        
    Returns:
        Chaîne JSON
    """
    return df.to_json(orient="records", date_format="iso")


def dataframe_to_excel(df: pd.DataFrame) -> bytes:
    """
    Convertit un DataFrame en bytes Excel.
    
    Args:
        df: DataFrame à convertir
        
    Returns:
        Bytes Excel
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Data", index=False)
    return output.getvalue()


def get_download_link(data: Union[str, bytes], 
                     filename: str, 
                     text: str,
                     mime_type: str = "text/csv") -> str:
    """
    Crée un lien de téléchargement pour des données.
    
    Args:
        data: Données à télécharger (chaîne ou bytes)
        filename: Nom du fichier
        text: Texte à afficher pour le lien
        mime_type: Type MIME des données
        
    Returns:
        HTML pour le lien de téléchargement
    """
    if isinstance(data, str):
        b64 = base64.b64encode(data.encode()).decode()
    else:
        b64 = base64.b64encode(data).decode()
    
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">{text}</a>'
    return href


def create_download_buttons(df: pd.DataFrame, base_filename: str) -> None:
    """
    Crée des boutons de téléchargement pour un DataFrame dans différents formats.
    
    Args:
        df: DataFrame à exporter
        base_filename: Nom de base pour les fichiers exportés
    """
    if df.empty:
        st.warning("Aucune donnée à exporter.")
        return
    
    st.write("### Exporter les données")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv_data = dataframe_to_csv(df)
        csv_filename = f"{base_filename}.csv"
        st.markdown(
            get_download_link(csv_data, csv_filename, "📄 Télécharger CSV"),
            unsafe_allow_html=True
        )
    
    with col2:
        json_data = dataframe_to_json(df)
        json_filename = f"{base_filename}.json"
        st.markdown(
            get_download_link(json_data, json_filename, "📋 Télécharger JSON", "application/json"),
            unsafe_allow_html=True
        )
    
    with col3:
        excel_data = dataframe_to_excel(df)
        excel_filename = f"{base_filename}.xlsx"
        st.markdown(
            get_download_link(excel_data, excel_filename, "📊 Télécharger Excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"),
            unsafe_allow_html=True
        )


def save_data_to_file(data: Any, 
                     file_path: Path, 
                     format: str = "json") -> bool:
    """
    Sauvegarde des données dans un fichier.
    
    Args:
        data: Données à sauvegarder
        file_path: Chemin du fichier
        format: Format de sauvegarde ('json', 'csv', 'excel')
        
    Returns:
        True si la sauvegarde a réussi, False sinon
    """
    try:
        # Créer le répertoire parent s'il n'existe pas
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Sauvegarder selon le format
        if format.lower() == "json":
            if isinstance(data, pd.DataFrame):
                data.to_json(file_path, orient="records", date_format="iso")
            else:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=2)
        
        elif format.lower() == "csv":
            if isinstance(data, pd.DataFrame):
                data.to_csv(file_path, index=False)
            else:
                raise ValueError("Les données doivent être un DataFrame pour l'exportation CSV")
        
        elif format.lower() == "excel":
            if isinstance(data, pd.DataFrame):
                data.to_excel(file_path, index=False)
            else:
                raise ValueError("Les données doivent être un DataFrame pour l'exportation Excel")
        
        else:
            raise ValueError(f"Format non pris en charge: {format}")
        
        return True
    
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde des données: {str(e)}")
        return False


def export_metrics_data(metrics: Dict[str, Any], 
                       target_dir: Path,
                       format: str = "json") -> bool:
    """
    Exporte les données de métriques dans un fichier.
    
    Args:
        metrics: Dictionnaire de métriques
        target_dir: Répertoire cible
        format: Format d'exportation
        
    Returns:
        True si l'exportation a réussi, False sinon
    """
    file_path = target_dir / f"metrics_export.{format.lower()}"
    return save_data_to_file(metrics, file_path, format)


def export_traces_data(traces: List[Dict[str, Any]], 
                      target_dir: Path,
                      format: str = "json") -> bool:
    """
    Exporte les données de traces dans un fichier.
    
    Args:
        traces: Liste de traces
        target_dir: Répertoire cible
        format: Format d'exportation
        
    Returns:
        True si l'exportation a réussi, False sinon
    """
    file_path = target_dir / f"traces_export.{format.lower()}"
    return save_data_to_file(traces, file_path, format)


def export_memory_data(memory_items: List[Dict[str, Any]], 
                      target_dir: Path,
                      format: str = "json") -> bool:
    """
    Exporte les données de mémoire dans un fichier.
    
    Args:
        memory_items: Liste d'éléments de mémoire
        target_dir: Répertoire cible
        format: Format d'exportation
        
    Returns:
        True si l'exportation a réussi, False sinon
    """
    file_path = target_dir / f"memory_export.{format.lower()}"
    return save_data_to_file(memory_items, file_path, format)


def create_export_section(data: Any, 
                         base_filename: str,
                         formats: List[str] = ["csv", "json", "excel"]) -> None:
    """
    Crée une section d'exportation pour des données.
    
    Args:
        data: Données à exporter (DataFrame ou dictionnaire)
        base_filename: Nom de base pour les fichiers exportés
        formats: Liste des formats d'exportation disponibles
    """
    st.write("### Exporter les données")
    
    # Convertir en DataFrame si nécessaire
    if not isinstance(data, pd.DataFrame):
        try:
            df = pd.DataFrame(data)
        except:
            st.warning("Les données ne peuvent pas être converties en DataFrame pour l'exportation.")
            return
    else:
        df = data
    
    # Créer les boutons d'exportation
    create_download_buttons(df, base_filename)
