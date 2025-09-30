###########################
## Import des librairies ##
###########################

import random
from similarite_orthographique import similarite_orthographique_avancee_ponderee

###########################
##   Variables globales  ##
###########################

mot_cible = "bonjour"
mot_affiche = "salut"

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
    t_identification_corrige = 200 + random.gauss(0, 50)
    t_motrice_corrige = 200 + random.gauss(0, 50)

    t_comparaison_corrige = (similarite * 150) + random.gauss(0, 30)

    if mot_cible == mot_courant:
        t_decision_corrige = t_decision - random.gauss(0, 20)
    else:
        t_decision_corrige = t_decision + random.gauss(0, 20)

    t_total_corrige = (
        t_perception_corrige
        + t_identification_corrige
        + t_comparaison_corrige
        + t_decision_corrige
        + t_motrice_corrige
    )

    print(f"{mot_affiche:<12} | Simil : {similarite:.2f} | Percep : {round(t_perception_corrige):>3} | ID : {round(t_identification_corrige):>3} | Comp : {round(t_comparaison_corrige):>3} | Dec : {round(t_decision_corrige):>3} | Motr : {round(t_motrice_corrige):>3} | Total : {round(t_total_corrige):>4} ms")

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