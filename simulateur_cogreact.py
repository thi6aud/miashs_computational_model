###########################
## Import des librairies ##
###########################

import random
from similarite_orthographique import similarite_orthographique_avancee_ponderee

import pandas as pd
import numpy as np

lexique = pd.read_csv("Lexique383.tsv", sep="\t", encoding="utf-8")

def get_freq_livre(mot):
    row = lexique[lexique["ortho"] == mot.lower()]
    if not row.empty:
        return row.iloc[0]["freqlivres"]
    else:
        return 0

###########################
##   Variables globales  ##
###########################

mot_cible = "bonjour"
mot_affiche = "salut"

t_perception = 75 + random.gauss(0, 25)           # constant
t_identification = 200 + random.gauss(0, 50)      # frequence/longueur/concretude
t_comparaison = 150 + random.gauss(0, 50)         # similarite/charge cognitive
t_decision = 150 + random.gauss(0, 25)            # meme + rapide que different ?
t_motrice = 200 + random.gauss(0, 30)             # si meme bouton a la suite + rapide

t_total = (
    t_perception
    + t_identification
    + t_comparaison
    + t_decision
    + t_motrice
)

############################
##   Variables corrigees  ##
############################

frequence = 0  # entre -5 et +5
similarite = similarite_orthographique_avancee_ponderee(mot_cible, mot_affiche)

# t_perception_corrige = t_perception

# t_identification_corrige = t_identification + random.gauss(0, 10 * frequence)

t_comparaison_corrige = (similarite * 150) + random.gauss(0, 30)

if mot_cible == mot_affiche:
    t_decision_corrige = t_decision - random.gauss(0, 20)
else:
    t_decision_corrige = t_decision + random.gauss(0, 20)

# t_motrice_corrige = t_motrice

t_total_corrige = (
    t_perception
    + t_identification
    + t_comparaison_corrige
    + t_decision_corrige
    + t_motrice
)

############################
##     Test liste mots    ##
############################

mots_affiches = [
    "bonjour", "bonsoir", "salut", "coucou", "allo", "hey",
    "merci", "plat", "moi", "pardon",
    "oui", "non", "être", "certainement",
    "revoir", "bientôt", "demain"
]

total_temps = 0

for mot_affiche in mots_affiches:
    mot_courant = mot_affiche
    similarite = similarite_orthographique_avancee_ponderee(mot_cible, mot_courant)

    t_perception_corrige = 75 + random.gauss(0, 25)
    freq = get_freq_livre(mot_affiche)
    log_freq = np.log(freq + 1)
    t_identification_corrige = 220 - 15 * log_freq + 2 * len(mot_affiche) + random.gauss(0, 20)
    t_motrice_corrige = 200 + random.gauss(0, 20)

    if mot_cible == mot_courant:
        # Si le mot est identique au mot cible, la comparaison est quasi immédiate
        t_comparaison_corrige = 30 + random.gauss(0, 10)
        t_decision_corrige = t_decision - random.gauss(0, 20)
    else:
        # Sinon, la comparaison dépend de la similarité (plus c'est proche, plus c'est lent)
        t_comparaison_corrige = max(10, (similarite * 150) + random.gauss(0, 20))
        t_decision_corrige = t_decision + random.gauss(0, 20)

    t_total_corrige = (
        t_perception_corrige
        + t_identification_corrige
        + t_comparaison_corrige
        + t_decision_corrige
        + t_motrice_corrige
    )

    print(f"{mot_affiche:<14} | Simil : {similarite:>4.2f} | Freq : {freq:>6.1f} | Percep : {round(t_perception_corrige):>3} | ID : {round(t_identification_corrige):>3} | Comp : {round(t_comparaison_corrige):>4} | Dec : {round(t_decision_corrige):>3} | Motr : {round(t_motrice_corrige):>3} | Total : {round(t_total_corrige):>4} ms")

    total_temps += t_total_corrige

moyenne_temps = total_temps / len(mots_affiches)
print(f"\nTemps moyen (TR simulé) : {round(moyenne_temps)} ms")

############################
##    Test mot par mot    ##
############################

'''
print("=== Simulation CogReact ===")
print(f"Mot cible         : {mot_cible}")
print(f"Mot affiché       : {mot_affiche}")
print(f"Similarité ortho  : {round(similarite, 3)}")
print()
print("--- Temps (ms) ---")
print(f"Perception        : {round(t_perception_corrige)}")
print(f"Identification    : {round(t_identification_corrige)}")
print(f"Comparaison       : {round(t_comparaison_corrige)}")
print(f"Décision          : {round(t_decision_corrige)}")
print(f"Motrice           : {round(t_motrice_corrige)}")
print(f"→ Temps total     : {round(t_total_corrige)} ms")
'''