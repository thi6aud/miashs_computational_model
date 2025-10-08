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

resultats = []

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

    resultats.append({
        "mot": mot_affiche,
        "similarite": similarite,
        "freq": freq,
        "perception": t_perception_corrige,
        "identification": t_identification_corrige,
        "comparaison": t_comparaison_corrige,
        "decision": t_decision_corrige,
        "motrice": t_motrice_corrige,
        "total": t_total_corrige
    })

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

import matplotlib.pyplot as plt

# Demande à l'utilisateur s'il souhaite afficher les graphiques
rep = input("Afficher les graphiques ? (y/N) : ").strip().lower()
show_plots = (rep == 'y')

if show_plots:
    # Crée une DataFrame pour les résultats
    df_resultats = pd.DataFrame(resultats)

    # Ajout LOWESS pour fréquence et similarité
    from statsmodels.nonparametric.smoothers_lowess import lowess

    x = df_resultats["freq"]
    y = df_resultats["total"]
    colors = ["red" if mot == mot_cible else "blue" for mot in df_resultats["mot"]]

    # LOWESS pour fréquence
    smoothed_freq = lowess(y, x, frac=0.5)
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, c=colors)
    for i, row in df_resultats.iterrows():
        color = "red" if row["mot"] == mot_cible else "blue"
        plt.annotate(row["mot"], (row["freq"], row["total"]), textcoords="offset points", xytext=(5,5), ha='left', fontsize=9, color=color)
    plt.plot(smoothed_freq[:, 0], smoothed_freq[:, 1], color='green', label='LOWESS')
    # Régression linéaire
    slope, intercept = np.polyfit(x, y, 1)
    x_sorted = np.sort(x)
    y_fit = slope * x_sorted + intercept
    plt.plot(x_sorted, y_fit, linestyle='--', color='black', label='Régression linéaire')
    plt.xlabel("Fréquence (freqlivres)")
    plt.ylabel("Temps total simulé (ms)")
    plt.title("Relation entre fréquence et TR (LOWESS)")
    plt.legend()
    plt.grid(True)

    # LOWESS pour similarité (on exclut le mot cible)
    df_sim = df_resultats[df_resultats["mot"] != mot_cible]

    x_sim = df_sim["similarite"]
    y_sim = df_sim["total"]
    smoothed_sim = lowess(y_sim, x_sim, frac=0.5)
    plt.figure(figsize=(10, 6))
    sim_colors = ["blue" for _ in x_sim]
    plt.scatter(x_sim, y_sim, c=sim_colors)
    for i, row in df_sim.iterrows():
        plt.annotate(row["mot"], (row["similarite"], row["total"]), textcoords="offset points", xytext=(5,5), ha='left', fontsize=9, color='blue')
    plt.plot(smoothed_sim[:, 0], smoothed_sim[:, 1], color='green', label='LOWESS')
    # Régression linéaire
    slope_sim, intercept_sim = np.polyfit(x_sim, y_sim, 1)
    x_sim_sorted = np.sort(x_sim)
    y_sim_fit = slope_sim * x_sim_sorted + intercept_sim
    plt.plot(x_sim_sorted, y_sim_fit, linestyle='--', color='black', label='Régression linéaire')
    plt.xlabel("Similarité orthographique")
    plt.ylabel("Temps total simulé (ms)")
    plt.title("Relation entre similarité et TR (LOWESS)")
    plt.legend()
    plt.grid(True)

    # Titres des fenêtres (si backend le permet)
    import matplotlib.pyplot as _plt
    try:
        manager1 = _plt.figure(1).canvas.manager
        manager1.set_window_title("Fréquence vs TR")
        manager2 = _plt.figure(2).canvas.manager
        manager2.set_window_title("Similarité vs TR")
    except Exception:
        pass

    # Affiche toutes les figures simultanément
    plt.show()
else:
    print("Graphiques ignorés — exécution terminée sans affichage des figures.")