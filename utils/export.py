"""
Utilitaires d'export et gestion des données
"""

import pandas as pd
import time
import random
import string


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


def generate_nonwords(word, n_nonwords=5, similarity_level='strong'):
    """
    Génère des non-mots par mutation caractère du mot cible.
    
    Args:
        word (str): Mot cible
        n_nonwords (int): Nombre de non-mots à générer
        similarity_level (str): 'weak', 'medium', 'strong'
        
    Returns:
        list: Liste de non-mots générés
    """
    from similarite_orthographique import similarite_orthographique_avancee_ponderee
    
    # Paramètres de mutation selon le niveau
    params = {
        'weak': {'n_mutations': 3, 'max_attempts': 100},
        'medium': {'n_mutations': 2, 'max_attempts': 100},
        'strong': {'n_mutations': 1, 'max_attempts': 100}
    }
    
    n_mutations = params.get(similarity_level, params['strong'])['n_mutations']
    max_attempts = params.get(similarity_level, params['strong'])['max_attempts']
    
    nonwords = []
    attempts = 0
    
    while len(nonwords) < n_nonwords and attempts < max_attempts:
        # Mutation aléatoire du mot
        word_list = list(word.lower())
        positions = random.sample(range(len(word_list)), min(n_mutations, len(word_list)))
        
        for pos in positions:
            # Remplacer par une lettre aléatoire
            new_char = random.choice(string.ascii_lowercase)
            while new_char == word_list[pos]:
                new_char = random.choice(string.ascii_lowercase)
            word_list[pos] = new_char
        
        nonword = ''.join(word_list)
        
        # Vérifier que ce n'est pas un mot existant
        # (on assume qu'on veut des non-mots)
        similarity = similarite_orthographique_avancee_ponderee(word, nonword)
        
        # Ajouter si c'est suffisamment similaire (selon le niveau)
        if similarity_level == 'strong' and 0.4 <= similarity <= 0.95:
            if nonword not in nonwords:
                nonwords.append(nonword)
        elif similarity_level == 'medium' and 0.25 <= similarity <= 0.7:
            if nonword not in nonwords:
                nonwords.append(nonword)
        elif similarity_level == 'weak' and 0.1 <= similarity <= 0.5:
            if nonword not in nonwords:
                nonwords.append(nonword)
        
        attempts += 1
    
    return nonwords

