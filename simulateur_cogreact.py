"""
Simulateur CogReact : Décision lexicale simulée avec variables cognitives

Ce script simule un temps de réaction (TR) humain dans une tâche de décision lexicale,
en prenant en compte plusieurs composantes temporelles :
- Temps de perception
- Temps d'identification (influencé par la fréquence et la longueur du mot)
- Temps de comparaison avec un mot cible (dépend de la similarité orthographique)
- Temps de décision (plus lent pour des mots similaires au mot cible)
- Temps moteur (variable aléatoirement)
"""

###########################
## Import des librairies ##
###########################

import random
import time
from similarite_orthographique import similarite_orthographique_avancee_ponderee
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

############################
##   Chargement donnees   ##
############################

with open("stimuli.json", "r", encoding="utf-8") as f:
    data = json.load(f)

###########################
## Acces frequences mots ##
###########################

lexique = pd.read_csv("Lexique383.tsv", sep="\t", encoding="utf-8")

def get_freq_livre(mot):
    rows = lexique[lexique["ortho"] == mot.lower()]
    if not rows.empty:
        # On somme les fréquences si plusieurs lignes existent
        return rows["freqlivres"].sum()
    else:
        return 0  # Mot inconnu

###########################
##      Parametres       ##
###########################

mot_cible = data["mot_cible"]
mots_affiches = data["mots_affiches"]

# Paramètres de base pour tirer du bruit (utilisés pour génération)
t_decision = 150 + random.gauss(0, 25)  # valeur de base (sera modifiée par essai)

############################
##    Entete affichage    ##
############################

print(f"{'Mot':<12} | {'Simil':>5} | {'Freq':>7} | {'Percep':>6} | {'ID':>4} | {'Comp':>4} | {'Dec':>4} | {'Motr':>4} | {'Total':>5}")
print("-" * 75)

############################
##     Test liste mots    ##
############################

resultats = []
total_temps = 0

for mot_affiche in mots_affiches:
    mot_courant = mot_affiche
    similarite = similarite_orthographique_avancee_ponderee(mot_cible, mot_courant)

    # bruitables
    t_perception = 75 + random.gauss(0, 25)
    freq = get_freq_livre(mot_affiche)
    non_mot = (freq == 0)
    log_freq = np.log(freq + 1)
    t_identification = 220 - 15 * log_freq + 2 * len(mot_affiche) + (80 if non_mot else 0) + random.gauss(0, 20)
    t_motrice = 200 + random.gauss(0, 20)

    if mot_cible == mot_courant:
        # Si le mot est identique au mot cible, la comparaison est quasi immédiate
        t_comparaison = 30 + random.gauss(0, 10)
        t_decision = t_decision - random.gauss(0, 20)
    else:
        # Sinon, la comparaison dépend de la similarité (plus c'est proche, plus c'est lent)
        t_comparaison = max(10, (similarite * 150) + random.gauss(0, 20))
        t_decision = t_decision + random.gauss(0, 20)

    t_total = (
        t_perception
        + t_identification
        + t_comparaison
        + t_decision
        + t_motrice
    )

    # Affichage des résultats
    print(f"{mot_affiche:<12} | {similarite:5.2f} | {freq:7.2f} | {round(t_perception):6} | {round(t_identification):4} | {round(t_comparaison):4} | {round(t_decision):4} | {round(t_motrice):4} | {round(t_total):5} ms")

    # Accumulation du temps total pour moyenne
    total_temps += t_total

    # Stockage des résultats pour export et analyse
    resultats.append({
        "mot": mot_affiche,
        "similarite": similarite,
        "freq": freq,
        "perception": t_perception,
        "identification": t_identification,
        "comparaison": t_comparaison,
        "decision": t_decision,
        "motrice": t_motrice,
        "total": t_total
    })

# Calcul et affichage du temps moyen
moyenne_temps = total_temps / len(mots_affiches)
print(f"\nTemps moyen (TR simulé) : {round(moyenne_temps)} ms")

############################
##  Graphiques et export  ##
############################

df_resultats = pd.DataFrame(resultats)

rep_export = input("Exporter les données sous forme CSV ? (y/N) : ").strip().lower()
if rep_export == 'y':
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"resultats_simulation_{timestamp}.csv"
    df_resultats.to_csv(filename, index=False, encoding='utf-8')
    print(f"'{filename}' exporté dans le dossier courant.")

rep = input("Afficher les graphiques ? (y/N) : ").strip().lower()
show_plots = (rep == 'y')

if show_plots:
    # Ajout LOWESS pour fréquence et similarité (statsmodels requis)
    try:
        from statsmodels.nonparametric.smoothers_lowess import lowess
    except Exception:
        lowess = None
        print("LOWESS non disponible (statsmodels manquant) — les plots continueront sans LOWESS.")

    # --- Fréquence vs Total ---
    x = df_resultats["freq"]
    y = df_resultats["total"]
    colors = ["red" if mot == mot_cible else "blue" for mot in df_resultats["mot"]]

    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, c=colors)
    for i, row in df_resultats.iterrows():
        color = "red" if row["mot"] == mot_cible else "blue"
        plt.annotate(row["mot"], (row["freq"], row["total"]), textcoords="offset points", xytext=(5,5), ha='left', fontsize=9, color=color)

    if lowess is not None:
        smoothed_freq = lowess(y, x, frac=0.5)
        plt.plot(smoothed_freq[:, 0], smoothed_freq[:, 1], color='green', label='LOWESS')

    # Régression linéaire
    if len(x) >= 2:
        slope, intercept = np.polyfit(x, y, 1)
        x_sorted = np.sort(x)
        y_fit = slope * x_sorted + intercept
        plt.plot(x_sorted, y_fit, linestyle='--', color='black', label='Régression linéaire')

    plt.xlabel("Fréquence (freqlivres)")
    plt.ylabel("Temps total simulé (ms)")
    plt.title("Relation entre fréquence et TR")
    plt.legend()
    plt.grid(True)

    # --- Similarité vs Total (exclut le mot cible) ---
    df_sim = df_resultats[df_resultats["mot"] != mot_cible]
    x_sim = df_sim["similarite"]
    y_sim = df_sim["total"]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_sim, y_sim, c='blue')
    for i, row in df_sim.iterrows():
        plt.annotate(row["mot"], (row["similarite"], row["total"]), textcoords="offset points", xytext=(5,5), ha='left', fontsize=9, color='blue')

    if lowess is not None and len(x_sim) >= 2:
        smoothed_sim = lowess(y_sim, x_sim, frac=0.5)
        plt.plot(smoothed_sim[:, 0], smoothed_sim[:, 1], color='green', label='LOWESS')

    if len(x_sim) >= 2:
        slope_sim, intercept_sim = np.polyfit(x_sim, y_sim, 1)
        x_sim_sorted = np.sort(x_sim)
        y_sim_fit = slope_sim * x_sim_sorted + intercept_sim
        plt.plot(x_sim_sorted, y_sim_fit, linestyle='--', color='black', label='Régression linéaire')

    plt.xlabel("Similarité orthographique")
    plt.ylabel("Temps total simulé (ms)")
    plt.title("Relation entre similarité et TR")
    plt.legend()
    plt.grid(True)
    plt.show()