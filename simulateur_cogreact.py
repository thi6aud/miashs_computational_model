###########################
## Import des librairies ##
###########################

import random
from similarite_orthographique import similarite_orthographique_avancee_ponderee

###########################
##   Variables globales  ##
###########################

mot_cible = "bonjour"
mot_affiche = "bolmdzur"

t_perception = 75 + random.gauss(0, 25)           # constant
t_identification = 200 + random.gauss(0, 50)      # frequence/longueur/concretude
t_comparaison = 150 + random.gauss(0, 50)         # similarite/charge cognitive
t_decision = 150 + random.gauss(0, 25)            # meme + rapide que different ?
t_motrice = 200 + random.gauss(0, 50)             # si meme bouton a la suite + rapide

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

t_perception_corrige = t_perception

t_identification_corrige = t_identification + random.gauss(0, 10 * frequence)

t_comparaison_corrige = (similarite * 150) + random.gauss(0, 30)

if mot_cible == mot_affiche:
    t_decision_corrige = t_decision - random.gauss(0, 20)
else:
    t_decision_corrige = t_decision + random.gauss(0, 20)

t_motrice_corrige = t_motrice

t_total_corrige = (
    t_perception_corrige
    + t_identification_corrige
    + t_comparaison_corrige
    + t_decision_corrige
    + t_motrice_corrige
)

############################
##     Test du modele     ##
############################

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