import json
from similarite_orthographique import similarite_orthographique_avancee_ponderee

# Charger les stimuli
with open("stimuli.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mot_cible = data["mot_cible"]
mots_affiches = data["mots_affiches"]

print(f"Mot cible: {mot_cible}\n")

# Calculer scores
scores = []
for mot in mots_affiches:
    if mot.lower() != mot_cible.lower():
        sim = similarite_orthographique_avancee_ponderee(mot_cible, mot)
        scores.append((mot, sim))

scores.sort(key=lambda x: x[1], reverse=True)

# Afficher par catégorie
print("FORT (>= 0.75):")
forts = [s for _, s in scores if s >= 0.75]
for mot, sim in scores:
    if sim >= 0.75:
        print(f"  {mot}: {sim:.3f}")

print("\nMOYEN (0.5 - 0.75):")
moyens = [s for _, s in scores if 0.5 <= s < 0.75]
for mot, sim in scores:
    if 0.5 <= sim < 0.75:
        print(f"  {mot}: {sim:.3f}")

print("\nFAIBLE (< 0.5):")
faibles = [s for _, s in scores if s < 0.5]
faible_count = 0
for mot, sim in scores:
    if sim < 0.5:
        if faible_count < 5:
            print(f"  {mot}: {sim:.3f}")
        faible_count += 1
if faible_count > 5:
    print(f"  ... et {faible_count - 5} autres")

# Statistiques
print(f"\n--- Résumé ---")
print(f"Fort:  {len(forts)} mots (>= 0.75)")
print(f"Moyen: {len(moyens)} mots (0.5-0.75)")
print(f"Faible: {len(faibles)} mots (< 0.5)")
cible_count = len([m for m in mots_affiches if m.lower() == mot_cible.lower()])
print(f"Cible: {cible_count}× '{mot_cible}'")
print(f"\nTotal: {len(scores) + cible_count} mots")
