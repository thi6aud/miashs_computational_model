"""
Simulation du temps de réaction pour l'ensemble des mots
"""

import pandas as pd
from similarite_orthographique import similarite_orthographique_avancee_ponderee
from .timing_model import (
    compute_perception_time,
    compute_identification_time,
    compute_comparison_time,
    compute_decision_time,
    compute_motor_time
)
from .data_loader import mot_cible, get_freq_livre
import random


def simulate_single_word(mot_affiche, t_decision_base):
    """
    Simule le temps de réaction pour un seul mot.
    
    Args:
        mot_affiche (str): Mot à présenter
        t_decision_base (float): Temps de décision de base
        
    Returns:
        tuple: (résultat_dict, t_decision_base_updated)
    """
    # Calcul de la similarité
    similarite = similarite_orthographique_avancee_ponderee(mot_cible, mot_affiche)
    
    # Composantes temporelles
    t_perception = compute_perception_time()
    t_identification = compute_identification_time(mot_affiche)
    t_comparaison = compute_comparison_time(mot_affiche, similarite)
    t_decision, t_decision_base = compute_decision_time(mot_affiche, t_decision_base)
    t_motrice = compute_motor_time()
    
    # Temps total
    t_total = (
        t_perception
        + t_identification
        + t_comparaison
        + t_decision
        + t_motrice
    )
    
    # Fréquence pour contexte
    freq = get_freq_livre(mot_affiche)
    
    # Résultat
    result = {
        "mot": mot_affiche,
        "similarite": similarite,
        "freq": freq,
        "perception": t_perception,
        "identification": t_identification,
        "comparaison": t_comparaison,
        "decision": t_decision,
        "motrice": t_motrice,
        "total": t_total
    }
    
    return result, t_decision_base


def simulate_all_words(mots_affiches):
    """
    Simule le temps de réaction pour tous les mots.
    
    Args:
        mots_affiches (list): Liste des mots à tester
        
    Returns:
        tuple: (DataFrame des résultats, temps moyen)
    """
    resultats = []
    total_temps = 0
    t_decision_base = 150 + random.gauss(0, 25)
    
    for mot_affiche in mots_affiches:
        result, t_decision_base = simulate_single_word(mot_affiche, t_decision_base)
        resultats.append(result)
        total_temps += result["total"]
    
    df_resultats = pd.DataFrame(resultats)
    moyenne_temps = total_temps / len(mots_affiches)
    
    return df_resultats, moyenne_temps
