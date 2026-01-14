"""
Génération aléatoire de stimuli pour le simulateur CogReact
"""

import json
import random
import pandas as pd
from similarite_orthographique import similarite_orthographique_avancee_ponderee
from utils.export import generate_nonwords

# Charger le lexique
lexique = pd.read_csv("Lexique383.tsv", sep="\t", encoding="utf-8")

def generate_stimuli(seed=None):
    """
    Génère un ensemble de stimuli aléatoires
    
    Args:
        seed (int): Graine aléatoire pour reproductibilité (optionnel)
    
    Returns:
        dict: Stimuli avec mot_cible et mots_affiches
    """
    if seed is not None:
        random.seed(seed)
    
    # 1. Piocher un mot cible (longueur 6-10) avec validation
    mots_candidates = lexique[
        (lexique['ortho'].str.len() >= 6) & 
        (lexique['ortho'].str.len() <= 10)
    ]['ortho'].dropna().tolist()
    
    # Vérifier que le mot cible a au moins 5 mots avec score > 0.75
    mot_cible = None
    attempts = 0
    while mot_cible is None and attempts < 100:
        candidate = random.choice(mots_candidates)
        
        # Compter combien de mots ont un score > 0.75
        count_high_sim = 0
        for mot in lexique['ortho'].dropna():
            if mot.lower() != candidate.lower():
                sim = similarite_orthographique_avancee_ponderee(candidate, mot)
                if sim > 0.75:
                    count_high_sim += 1
        
        if count_high_sim >= 5:
            mot_cible = candidate
        else:
            attempts += 1
    
    if mot_cible is None:
        print("⚠️  Aucun mot trouvé avec au moins 5 mots similaires à >0.75")
        return None
    
    print(f"Mot cible choisi: {mot_cible}")
    
    # 2. Calculer la similarité de tous les mots du lexique
    similarites = []
    for mot in lexique['ortho'].dropna():
        if mot.lower() != mot_cible.lower():  # Exclure le mot cible
            sim = similarite_orthographique_avancee_ponderee(mot_cible, mot)
            similarites.append((mot, sim))
    
    # Trier par similarité
    similarites.sort(key=lambda x: x[1])
    
    # 3. Extraire mots par niveau de similarité
    # Seuils absolus: faible < 0.5, moyen 0.5-0.75, fort >= 0.75
    mots_faible = []
    mots_moyen = []
    mots_fort = []
    
    for mot, sim in similarites:
        if sim < 0.5:
            mots_faible.append(mot)
        elif sim < 0.75:
            mots_moyen.append(mot)
        else:
            mots_fort.append(mot)
    
    print(f"  - Disponibles: {len(mots_faible)} faible, {len(mots_moyen)} moyen, {len(mots_fort)} fort (>0.75)")
    
    # Prélever 5 mots de chaque niveau
    mots_faible = random.sample(mots_faible, min(5, len(mots_faible)))
    mots_moyen = random.sample(mots_moyen, min(5, len(mots_moyen)))
    mots_fort = random.sample(mots_fort, min(5, len(mots_fort)))
    
    print(f"  - 5 mots faible similarité: {mots_faible}")
    print(f"  - 5 mots moyen similarité: {mots_moyen}")
    print(f"  - 5 mots fort similarité: {mots_fort}")
    
    # 4. Générer 5 non-mots de similarité forte
    nonwords = generate_nonwords(mot_cible, n_nonwords=5, similarity_level='strong')
    print(f"  - 5 non-mots (similarité forte): {nonwords}")
    
    # 5. Créer la liste complète (25 mots)
    mots_affiches = (
        mots_faible + 
        mots_moyen + 
        mots_fort + 
        nonwords + 
        [mot_cible] * 5  # 5 fois le mot cible
    )
    
    # Mélanger
    random.shuffle(mots_affiches)
    
    # 6. Sauvegarder
    stimuli = {
        "mot_cible": mot_cible,
        "mots_affiches": mots_affiches,
        "seed": seed
    }
    
    with open("stimuli.json", "w", encoding="utf-8") as f:
        json.dump(stimuli, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Stimuli générés et sauvegardés dans stimuli.json")
    print(f"  Total: {len(mots_affiches)} mots")
    
    return stimuli


if __name__ == "__main__":
    import sys
    
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else None
    generate_stimuli(seed)
