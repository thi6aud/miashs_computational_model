import numpy as np

def levenshtein(a, b, ratio=False, print_matrix=False, lowercase=False):
    if type(a) != type(''):
        raise TypeError('First argument is not a string!')
    if type(b) != type(''):
        raise TypeError('Second argument is not a string!')
    if a == '':
        return len(b)
    if b == '':
        return len(a)
    if lowercase:
        a = a.lower()
        b = b.lower()

    n = len(a)
    m = len(b)
    lev = np.zeros((n+1, m+1))

    for i in range(0, n+1):
        lev[i, 0] = i 
    for i in range(0, m+1):
        lev[0, i] = i

    for i in range(1, n+1):
        for j in range(1, m+1):
            insertion = lev[i-1, j] + 1
            deletion = lev[i, j-1] + 1
            substitution = lev[i-1, j-1] + (1 if a[i-1] != b[j-1] else 0)
            lev[i, j] = min(insertion, deletion, substitution)

    if print_matrix:
        print(lev)

    if ratio:
        return (n + m - lev[n, m]) / (n + m)
    else:
        return lev[n, m]

def get_bigrams(mot):
    """Extrait les bigrammes d'un mot"""
    return [mot[i:i+2] for i in range(len(mot)-1)]

# Version originale (non ponderee) pour la comparaison
def similarite_orthographique_avancee(mot1, mot2):
    """Version originale sans ponderation positionnelle"""
    mot1_lower, mot2_lower = mot1.lower(), mot2.lower()
    
    # 1. Ratio Levenshtein
    ratio_levenshtein = levenshtein(mot1, mot2, ratio=True, lowercase=True)
    
    # 2. Jaccard (lettres communes)
    set1, set2 = set(mot1_lower), set(mot2_lower)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    jaccard = intersection / union if union > 0 else 0
    
    # 3. Similarite positionnelle (non ponderee)
    similarite_position = 0
    min_len = min(len(mot1_lower), len(mot2_lower))
    for i in range(min_len):
        if mot1_lower[i] == mot2_lower[i]:
            similarite_position += 1
    similarite_position /= max(len(mot1_lower), len(mot2_lower))
    
    # 4. Similarite des bigrammes (non ponderee)
    bigrammes1 = get_bigrams(mot1_lower)
    bigrammes2 = get_bigrams(mot2_lower)
    bigrammes_communs = len(set(bigrammes1) & set(bigrammes2))
    similarite_bigrammes = bigrammes_communs / max(len(bigrammes1), len(bigrammes2)) if max(len(bigrammes1), len(bigrammes2)) > 0 else 0
    
    # Ponderation equilibree
    score_final = (0.35 * ratio_levenshtein +
                   0.25 * jaccard + 
                   0.25 * similarite_position + 
                   0.15 * similarite_bigrammes)
    
    return min(score_final, 1.0)

def similarite_position_ponderee(mot1, mot2):
    """
    Similarite positionnelle avec ponderation cognitive :
    - Première lettre : poids maximum
    - Dernière lettre : poids eleve  
    - Lettres medianes : poids reduit
    """
    mot1_lower, mot2_lower = mot1.lower(), mot2.lower()
    min_len = min(len(mot1_lower), len(mot2_lower))
    max_len = max(len(mot1_lower), len(mot2_lower))
    
    if max_len == 0:
        return 0
    
    score_total = 0
    poids_total = 0
    
    for i in range(min_len):
        # Attribution des poids selon la position
        if i == 0:  # Première lettre - très importante
            poids = 2.0
        elif i == min_len - 1:  # Dernière lettre - importante
            poids = 1.5
        else:  # Lettres medianes - moins importantes
            poids = 0.5 + (0.5 * (1 - i/min_len))  # Decroissance legère
        
        if mot1_lower[i] == mot2_lower[i]:
            score_total += poids
        poids_total += poids
    
    # Penalite pour les lettres en trop
    penalite_longueur = abs(len(mot1_lower) - len(mot2_lower)) * 0.3
    
    score_pondere = (score_total / poids_total) if poids_total > 0 else 0
    score_final = max(0, score_pondere - penalite_longueur / max_len)
    
    return min(score_final, 1.0)

def similarite_orthographique_avancee_ponderee(mot1, mot2):
    """
    Version amelioree avec ponderation cognitive des positions
    """
    mot1_lower, mot2_lower = mot1.lower(), mot2.lower()
    
    # 1. Ratio Levenshtein (global)
    ratio_levenshtein = levenshtein(mot1, mot2, ratio=True, lowercase=True)
    
    # 2. Jaccard (lettres communes) - moins important
    set1, set2 = set(mot1_lower), set(mot2_lower)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    jaccard = intersection / union if union > 0 else 0
    
    # 3. Similarite positionnelle PONDeReE (nouvelle version)
    similarite_pos = similarite_position_ponderee(mot1, mot2)
    
    # 4. Bigrammes avec ponderation positionnelle
    bigrammes1 = get_bigrams(mot1_lower)
    bigrammes2 = get_bigrams(mot2_lower)
    
    if not bigrammes1 or not bigrammes2:
        similarite_bigrammes = 0
    else:
        # Ponderation des bigrammes initiaux/finaux
        bigrammes_communs_ponderes = 0
        total_ponderation = 0
        
        for i, bigram in enumerate(bigrammes1):
            if bigram in bigrammes2:
                # Bigrammes en position initiale/finale plus importants
                if i == 0 or i == len(bigrammes1) - 1:  # Debut ou fin
                    poids = 1.5
                else:  # Milieu
                    poids = 1.0
                bigrammes_communs_ponderes += poids
            total_ponderation += 1.0  # Ponderation de base pour tous les bigrammes
        
        similarite_bigrammes = bigrammes_communs_ponderes / total_ponderation
    
    # NOUVELLE ponderation qui favorise la similarite positionnelle
    score_final = (0.25 * ratio_levenshtein +     # Mesure globale
                   0.15 * jaccard +              # Lettres communes (moins important)
                   0.45 * similarite_pos +       # POSITIONS (très important)
                   0.15 * similarite_bigrammes)  # Patterns
    
    return min(score_final, 1.0)

def tester_comparaison():
    """Compare l'ancienne et la nouvelle version"""
    
    paires_test = [
        ("maison", "raisin"),   # Votre exemple problematique
        ("chant", "champ"),     # Très similaire
        ("chant", "chien"),     # Un peu similaire  
        ("chant", "table"),     # Different
        ("porte", "parte"),     # Similaire debut
        ("livre", "liver"),     # Similaire sauf fin
        ("arbre", "arbuste"),   # Prefixe commun
        ("main", "mains"),      # Singulier/pluriel
    ]
    
    print("=== COMPARAISON ANCIENNE vs NOUVELLE VERSION ===\n")
    
    for mot1, mot2 in paires_test:
        # Ancienne version (position non ponderee)
        sim_ancienne = similarite_orthographique_avancee(mot1, mot2)
        
        # Nouvelle version (position ponderee)
        sim_nouvelle = similarite_orthographique_avancee_ponderee(mot1, mot2)
        
        # Similarite positionnelle seule pour comprendre
        sim_pos_ancienne = sum(1 for i in range(min(len(mot1), len(mot2))) 
                             if mot1[i].lower() == mot2[i].lower()) / max(len(mot1), len(mot2))
        sim_pos_nouvelle = similarite_position_ponderee(mot1, mot2)
        
        print(f"{mot1} vs {mot2}:")
        print(f"  Ancienne: {sim_ancienne:.3f} (position: {sim_pos_ancienne:.3f})")
        print(f"  Nouvelle: {sim_nouvelle:.3f} (position: {sim_pos_nouvelle:.3f})")
        print(f"  Difference: {sim_nouvelle - sim_ancienne:+.3f}")
        print()

# Test specifique pour votre exemple
def test_maison_raisin():
    print("=== ANALYSE DeTAILLeE maison vs raisin ===")
    mot1, mot2 = "maison", "raisin"
    
    # Detail des similarites
    print("Lettres en commun:", set(mot1) & set(mot2))
    print("Alignement:")
    for i, (l1, l2) in enumerate(zip(mot1, mot2)):
        egal = "✓" if l1 == l2 else "✗"
        poids = "DeBUT" if i == 0 else "FIN" if i == min(len(mot1), len(mot2))-1 else "milieu"
        print(f"  Position {i} ({poids}): {l1} vs {l2} {egal}")
    
    sim_ancienne = similarite_orthographique_avancee(mot1, mot2)
    sim_nouvelle = similarite_orthographique_avancee_ponderee(mot1, mot2)
    print(f"\nSimilarite ancienne: {sim_ancienne:.3f}")
    print(f"Similarite nouvelle: {sim_nouvelle:.3f}")

if __name__ == "__main__":
    tester_comparaison()
    test_maison_raisin()