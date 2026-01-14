"""
Lancer le simulateur 100 fois et créer des graphiques
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from core import simulate_all_words
from core.data_loader import mot_cible, mots_affiches

# Charger les stimuli avec fréquence et similarité
with open("stimuli_website.json", "r", encoding="utf-8") as f:
    stimuli_data = json.load(f)

# Créer un mapping mot -> (similarité, est_reel)
mot_map = {item["mot"]: item for item in stimuli_data["mots_affiches"]}

# Charger le lexique pour les fréquences
import pandas as pd
lexique = pd.read_csv("Lexique383.tsv", sep="\t", encoding="utf-8")
freq_dict = dict(zip(lexique['ortho'].str.lower(), lexique['freqlivres']))

print("Lancement du simulateur 100 fois...")

all_results = []

for run in range(1, 101):
    # Lancer une simulation
    df_resultats, _ = simulate_all_words(mots_affiches)
    
    # Ajouter similarité et fréquence
    for _, row in df_resultats.iterrows():
        mot = row['mot']
        freq = freq_dict.get(mot.lower(), 0)
        
        if mot in mot_map:
            sim = mot_map[mot]["similarite"]
        else:
            sim = 0
        
        all_results.append({
            'mot': mot,
            'tempsReaction(ms)': row['total'],
            'similarite': sim,
            'frequence': freq,
            'run': run
        })
    
    if run % 20 == 0:
        print(f"  ✓ {run}/100 simulations complétées")

# Créer dataframe
df_all = pd.DataFrame(all_results)

print(f"\n✅ {len(df_all)} observations générées (100 runs × 25 mots)")

# Créer les graphiques
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Graphique 1 : Temps de réaction vs Similarité (coloré par similarité)
ax1 = axes[0]
scatter1 = ax1.scatter(df_all['similarite'], df_all['tempsReaction(ms)'], 
                       c=df_all['similarite'], cmap='RdYlGn_r', 
                       alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
cbar1 = plt.colorbar(scatter1, ax=ax1)
cbar1.set_label('Similarité', fontsize=11)

# Ajouter une ligne de tendance
z = np.polyfit(df_all['similarite'], df_all['tempsReaction(ms)'], 1)
p = np.poly1d(z)
sim_sorted = np.sort(df_all['similarite'].unique())
ax1.plot(sim_sorted, p(sim_sorted), "b--", linewidth=2.5, label='Tendance', alpha=0.8)

ax1.set_xlabel('Similarité orthographique', fontsize=12)
ax1.set_ylabel('Temps de réaction (ms)', fontsize=12)
ax1.set_title('TR vs Similarité (100 simulations)', fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend()

# Graphique 2 : Temps de réaction vs Fréquence (coloré par fréquence)
ax2 = axes[1]
scatter2 = ax2.scatter(df_all['frequence'], df_all['tempsReaction(ms)'], 
                       c=df_all['frequence'], cmap='YlOrRd', 
                       alpha=0.6, s=50, edgecolors='black', linewidth=0.5)
cbar2 = plt.colorbar(scatter2, ax=ax2)
cbar2.set_label('Fréquence', fontsize=11)

# Ajouter une ligne de tendance
z2 = np.polyfit(df_all['frequence'], df_all['tempsReaction(ms)'], 1)
p2 = np.poly1d(z2)
freq_sorted = np.sort(df_all['frequence'].unique())
ax2.plot(freq_sorted, p2(freq_sorted), "b--", linewidth=2.5, label='Tendance', alpha=0.8)

ax2.set_xlabel('Fréquence lexicale', fontsize=12)
ax2.set_ylabel('Temps de réaction (ms)', fontsize=12)
ax2.set_title('TR vs Fréquence (100 simulations)', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('simulateur_100_runs.png', dpi=150, bbox_inches='tight')
print("\n📊 Graphiques sauvegardés: simulateur_100_runs.png")

# Statistiques
print(f"\n--- Statistiques ---")
print(f"Temps de réaction moyen: {df_all['tempsReaction(ms)'].mean():.0f} ms")
print(f"Écart-type TR: {df_all['tempsReaction(ms)'].std():.0f} ms")
print(f"\nCorr(TR, similarité): {df_all['tempsReaction(ms)'].corr(df_all['similarite']):.3f}")
print(f"Corr(TR, fréquence): {df_all['tempsReaction(ms)'].corr(df_all['frequence']):.3f}")

# Sauvegarder les données
df_all.to_csv('resultats_simulateur_100.csv', index=False)
print(f"\n✅ Données sauvegardées: resultats_simulateur_100.csv")
