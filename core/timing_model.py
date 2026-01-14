"""
Modèle temporel pour les composantes du temps de réaction
"""

import random
import numpy as np
from .data_loader import get_freq_livre, mot_cible


def compute_perception_time():
    """
    Temps de perception du stimulus (relativement constant).
    
    Returns:
        float: Temps de perception en ms
    """
    return 75 + random.gauss(0, 25)


def compute_identification_time(mot, similarite=0):
    """
    Temps d'identification du mot (dépend de la fréquence et longueur).
    Basé sur les lois de fréquence et longueur des mots.
    
    Args:
        mot (str): Mot à identifier
        similarite (float): Score de similarité orthographique (0-1)
        
    Returns:
        float: Temps d'identification en ms
    """
    freq = get_freq_livre(mot)
    is_nonword = (freq == 0)
    log_freq = np.log(freq + 1)
    
    t_id = (
        220 - 15 * log_freq 
        + 2 * len(mot) 
        + (80 if is_nonword else 0) 
        + random.gauss(0, 20)
    )
    
    return t_id


def compute_comparison_time(mot, similarite):
    """
    Temps de comparaison avec le mot cible.
    Plus la similarité est élevée, plus la comparaison prend du temps (interférence).
    
    Args:
        mot (str): Mot courant
        similarite (float): Score de similarité orthographique (0-1)
        
    Returns:
        float: Temps de comparaison en ms
    """
    if mot == mot_cible:
        # Si le mot est identique au mot cible, la comparaison est quasi immédiate
        return 30 + random.gauss(0, 10)
    else:
        # Sinon, la comparaison dépend de la similarité
        # Augmenté de 150 à 180 pour mieux capturer l'effet de similarité
        return max(10, (similarite * 180) + random.gauss(0, 20))


def compute_decision_time(mot, similarite, t_decision_base):
    """
    Temps de décision (réponse OUI/NON).
    
    Args:
        mot (str): Mot courant
        similarite (float): Score de similarité orthographique (0-1)
        t_decision_base (float): Temps de décision de base
        
    Returns:
        tuple: (Temps de décision en ms, Nouvelle base pour prochains essais)
    """
    if mot == mot_cible:
        t_dec = t_decision_base - random.gauss(0, 20)
    else:
        t_dec = t_decision_base + random.gauss(0, 20)
    
    return t_dec, t_decision_base


def compute_motor_time():
    """
    Temps moteur (exécution de la réponse).
    Variable aléatoirement (capacité motrice).
    
    Returns:
        float: Temps moteur en ms
    """
    return 200 + random.gauss(0, 20)
