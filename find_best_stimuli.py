"""
Tester plusieurs configurations de stimuli et trouver la meilleure
"""

import json
import subprocess
import pandas as pd
from similarite_orthographique import similarite_orthographique_avancee_ponderee

# Générer 5 configurations différentes
seeds_to_test = [101, 102, 103, 104, 105]
results_summary = []

for seed in seeds_to_test:
    print(f"\n{'='*60}")
    print(f"Test seed {seed}")
    print(f"{'='*60}")
    
    # Générer les stimuli
    subprocess.run(["python", "generate_stimuli.py", str(seed)], 
                   capture_output=True)
    
    # Charger les stimuli
    with open("stimuli.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    mot_cible = data["mot_cible"]
    mots_affiches = data["mots_affiches"]
    
    # Calculer les scores de similarité
    scores = []
    for mot in mots_affiches:
        if mot.lower() != mot_cible.lower():
            sim = similarite_orthographique_avancee_ponderee(mot_cible, mot)
            scores.append(sim)
    
    # Statistiques
    import statistics
    scores_array = pd.Series(scores)
    
    n_fort = len([s for s in scores if s >= 0.75])
    n_moyen = len([s for s in scores if 0.5 <= s < 0.75])
    n_faible = len([s for s in scores if s < 0.5])
    
    print(f"Mot cible: {mot_cible}")
    print(f"Fort (≥0.75): {n_fort} | Moyen (0.5-0.75): {n_moyen} | Faible (<0.5): {n_faible}")
    print(f"Score moyen: {scores_array.mean():.3f}")
    print(f"Score min: {scores_array.min():.3f}")
    print(f"Score max: {scores_array.max():.3f}")
    print(f"Écart-type: {scores_array.std():.3f}")
    
    # Variation = mesure de la diversité
    variation = scores_array.max() - scores_array.min()
    print(f"Variation (max-min): {variation:.3f}")
    
    results_summary.append({
        'seed': seed,
        'mot_cible': mot_cible,
        'score_moyen': scores_array.mean(),
        'score_std': scores_array.std(),
        'variation': variation,
        'n_fort': n_fort,
        'n_moyen': n_moyen,
        'n_faible': n_faible
    })

# Résumé et recommandation
print(f"\n{'='*60}")
print("RÉSUMÉ DES TESTS")
print(f"{'='*60}")

df_summary = pd.DataFrame(results_summary)
print(df_summary.to_string(index=False))

# Choisir la meilleure : bonne variation + bonne distribution
df_summary['score_qualite'] = (
    df_summary['variation'] * 0.4 +  # variation importante
    df_summary['score_std'] * 0.3    # écart-type important
)

best_idx = df_summary['score_qualite'].idxmax()
best_seed = df_summary.loc[best_idx, 'seed']
best_mot = df_summary.loc[best_idx, 'mot_cible']

print(f"\n✨ MEILLEURE CONFIG: seed {int(best_seed)} (mot: {best_mot})")
print(f"   → Génère la meilleure diversité et variation des résultats")

# Générer la meilleure config
subprocess.run(["python", "generate_stimuli.py", str(int(best_seed))], 
               capture_output=True)

print(f"\n✅ Config optimale sauvegardée dans stimuli.json")
