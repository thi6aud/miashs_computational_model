"""
Visualisation et analyse graphique des résultats
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from .data_loader import mot_cible

try:
    from statsmodels.nonparametric.smoothers_lowess import lowess
except ImportError:
    lowess = None


def plot_similarity_vs_comparison(df_resultats):
    """
    Similarité vs Temps de comparaison avec gradient de couleur.
    """
    df_sim = df_resultats[df_resultats["mot"] != mot_cible]
    
    if len(df_sim) == 0:
        return
    
    x_comp = df_sim["similarite"]
    y_comp = df_sim["comparaison"]
    
    plt.figure(figsize=(10, 6))
    
    # Gradient de couleur
    norm_sim = plt.Normalize(x_comp.min(), x_comp.max())
    cmap = plt.cm.coolwarm
    scatter = plt.scatter(x_comp, y_comp, c=x_comp, cmap=cmap, norm=norm_sim)
    
    # Annotations
    for i, row in df_sim.iterrows():
        color = cmap(norm_sim(row["similarite"]))
        plt.annotate(
            row["mot"],
            (row["similarite"], row["comparaison"]),
            textcoords="offset points",
            xytext=(5, 5),
            ha='left',
            fontsize=9,
            color=color
        )
    
    # LOWESS
    if lowess is not None and len(x_comp.dropna()) >= 2:
        smoothed_comp = lowess(y_comp, x_comp, frac=0.6)
        plt.plot(smoothed_comp[:, 0], smoothed_comp[:, 1], color='green', label='LOWESS')
    
    # Régression linéaire
    if len(x_comp.dropna()) >= 2:
        slope_comp, intercept_comp = np.polyfit(x_comp, y_comp, 1)
        x_comp_sorted = np.sort(x_comp)
        y_comp_fit = slope_comp * x_comp_sorted + intercept_comp
        plt.plot(x_comp_sorted, y_comp_fit, linestyle='--', color='black', label='Régression linéaire')
    
    plt.xlabel("Similarité orthographique")
    plt.ylabel("Temps de comparaison (ms)")
    plt.title("Similarité vs Temps de comparaison")
    plt.grid(True)
    
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Mot', markerfacecolor='blue', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Non-mot', markerfacecolor='purple', markersize=8)
    ]
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles=legend_elements + handles, loc="upper right")


def plot_frequency_vs_identification(df_resultats):
    """
    Fréquence vs Temps d'identification avec codes couleur.
    """
    plt.figure(figsize=(10, 6))
    x_id = df_resultats["freq"]
    y_id = df_resultats["identification"]
    
    # Codes couleur
    colors = []
    for _, row in df_resultats.iterrows():
        if row["mot"] == mot_cible:
            colors.append("red")
        elif row["freq"] == 0:
            colors.append("purple")
        else:
            colors.append("blue")
    
    plt.scatter(x_id, y_id, c=colors)
    
    # Annotations
    for i, row in df_resultats.iterrows():
        color = "red" if row["mot"] == mot_cible else "purple" if row["freq"] == 0 else "blue"
        plt.annotate(
            row["mot"],
            (row["freq"], row["identification"]),
            textcoords="offset points",
            xytext=(5, 5),
            ha='left',
            fontsize=9,
            color=color
        )
    
    # LOWESS
    if lowess is not None and len(x_id.dropna()) >= 2:
        smoothed_id = lowess(y_id, x_id, frac=0.6)
        plt.plot(smoothed_id[:, 0], smoothed_id[:, 1], color='green', label='LOWESS')
    
    # Régression linéaire
    if len(x_id.dropna()) >= 2:
        slope_id, intercept_id = np.polyfit(x_id, y_id, 1)
        x_id_sorted = np.sort(x_id)
        y_id_fit = slope_id * x_id_sorted + intercept_id
        plt.plot(x_id_sorted, y_id_fit, linestyle='--', color='black', label='Régression linéaire')
    
    plt.xlabel("Fréquence (freqlivres)")
    plt.ylabel("Temps d'identification (ms)")
    plt.title("Fréquence vs Temps d'identification")
    
    from matplotlib.lines import Line2D
    legend_points = [
        Line2D([0], [0], marker='o', color='w', label='Mot cible', markerfacecolor='red', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Mot', markerfacecolor='blue', markersize=8),
        Line2D([0], [0], marker='o', color='w', label='Non-mot', markerfacecolor='purple', markersize=8)
    ]
    handles, labels = plt.gca().get_legend_handles_labels()
    plt.legend(handles=legend_points + handles, loc="upper right")
    plt.grid(True)


def plot_length_vs_identification(df_resultats):
    """
    Longueur du mot vs Temps d'identification avec gradient de couleur.
    """
    plt.figure(figsize=(10, 6))
    df_resultats["longueur"] = df_resultats["mot"].apply(len)
    x_len = df_resultats["longueur"]
    y_id = df_resultats["identification"]
    
    # Gradient de couleur
    norm_len = plt.Normalize(x_len.min(), x_len.max())
    cmap = plt.cm.coolwarm
    scatter = plt.scatter(x_len, y_id, c=x_len, cmap=cmap, norm=norm_len)
    
    # Annotations
    for i, row in df_resultats.iterrows():
        color = cmap(norm_len(row["longueur"]))
        plt.annotate(
            row["mot"],
            (row["longueur"], row["identification"]),
            textcoords="offset points",
            xytext=(5, 5),
            ha='left',
            fontsize=9,
            color=color
        )
    
    # LOWESS
    if lowess is not None and len(x_len.dropna()) >= 2:
        smoothed_len = lowess(y_id, x_len, frac=0.6)
        plt.plot(smoothed_len[:, 0], smoothed_len[:, 1], color='green', label='LOWESS')
    
    # Régression linéaire
    if len(x_len.dropna()) >= 2:
        slope_len, intercept_len = np.polyfit(x_len, y_id, 1)
        x_len_sorted = np.sort(x_len)
        y_len_fit = slope_len * x_len_sorted + intercept_len
        plt.plot(x_len_sorted, y_len_fit, linestyle='--', color='black', label='Régression linéaire')
    
    plt.xlabel("Longueur du mot (nb lettres)")
    plt.ylabel("Temps d'identification (ms)")
    plt.title("Longueur du mot vs Temps d'identification")
    handles_len, labels_len = plt.gca().get_legend_handles_labels()
    plt.legend(handles=handles_len, loc="upper left")
    plt.grid(True)


def show_all_plots(df_resultats):
    """
    Affiche tous les graphiques d'analyse.
    
    Args:
        df_resultats (DataFrame): Résultats de la simulation
    """
    if lowess is None:
        print("LOWESS non disponible (statsmodels manquant) — les plots continueront sans LOWESS.")
    
    plot_similarity_vs_comparison(df_resultats)
    plot_frequency_vs_identification(df_resultats)
    plot_length_vs_identification(df_resultats)
    plt.show()
