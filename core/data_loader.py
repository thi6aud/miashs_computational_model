"""
Chargement et gestion des données pour le simulateur CogReact
"""

import json
import pandas as pd

# Chargement des stimuli
with open("stimuli.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mot_cible = data["mot_cible"]
mots_affiches = data["mots_affiches"]

# Chargement du lexique
lexique = pd.read_csv("Lexique383.tsv", sep="\t", encoding="utf-8")


def get_freq_livre(mot):
    """
    Accès aux fréquences du lexique pour un mot donné.
    
    Args:
        mot (str): Mot à chercher
        
    Returns:
        float: Fréquence (freqlivres), 0 si mot inconnu
    """
    rows = lexique[lexique["ortho"] == mot.lower()]
    if not rows.empty:
        # On somme les fréquences si plusieurs lignes existent
        return rows["freqlivres"].sum()
    else:
        return 0  # Mot inconnu
