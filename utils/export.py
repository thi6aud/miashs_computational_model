"""
Utilitaires d'export et gestion des données
"""

import pandas as pd
import time


def export_results_to_csv(df_resultats, ask_user=True):
    """
    Exporte les résultats de la simulation en CSV.
    
    Args:
        df_resultats (DataFrame): Résultats à exporter
        ask_user (bool): Si True, demande à l'utilisateur avant d'exporter
        
    Returns:
        str: Nom du fichier exporté, ou None si pas d'export
    """
    if ask_user:
        rep_export = input("Exporter les données sous forme CSV ? (y/N) : ").strip().lower()
        if rep_export != 'y':
            return None
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"resultats_simulation_{timestamp}.csv"
    df_resultats.to_csv(filename, index=False, encoding='utf-8')
    print(f"'{filename}' exporté dans le dossier courant.")
    return filename


def should_show_plots(ask_user=True):
    """
    Demande à l'utilisateur s'il veut afficher les graphiques.
    
    Args:
        ask_user (bool): Si True, pose la question à l'utilisateur
        
    Returns:
        bool: True si l'utilisateur veut les graphiques
    """
    if not ask_user:
        return False
    
    rep = input("Afficher les graphiques ? (y/N) : ").strip().lower()
    return rep == 'y'
