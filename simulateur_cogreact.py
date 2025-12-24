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
## Import des modules    ##
###########################

from core import mot_cible, mots_affiches, simulate_all_words
from utils import export_results_to_csv, should_show_plots
from analysis import show_all_plots

############################
##    Entete affichage    ##
############################

print(f"{'Mot':<12} | {'Simil':>5} | {'Freq':>7} | {'Percep':>6} | {'ID':>4} | {'Comp':>4} | {'Dec':>4} | {'Motr':>4} | {'Total':>5}")
print("-" * 75)

############################
##     Simulation         ##
############################

df_resultats, moyenne_temps = simulate_all_words(mots_affiches)

# Affichage des résultats
for _, row in df_resultats.iterrows():
    print(f"{row['mot']:<12} | {row['similarite']:5.2f} | {row['freq']:7.2f} | {round(row['perception']):6} | {round(row['identification']):4} | {round(row['comparaison']):4} | {round(row['decision']):4} | {round(row['motrice']):4} | {round(row['total']):5} ms")

print(f"\nTemps moyen (TR simulé) : {round(moyenne_temps)} ms")

############################
##  Export et visualisation ##
############################

export_results_to_csv(df_resultats, ask_user=True)

if should_show_plots(ask_user=True):
    show_all_plots(df_resultats)