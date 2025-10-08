###########################
## Import des librairies ##
###########################

import numpy as np

###########################
##  Distance levenshtein ##
###########################

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

###########################
## Calculs de similarite ##
###########################

def get_bigrams(mot):
    """Extrait les bigrammes d'un mot"""
    return [mot[i:i+2] for i in range(len(mot)-1)]

def similarite_orthographique_avancee(mot1, mot2):
    """Version originale sans ponderation positionnelle"""
    mot1_lower, mot2_lower = mot1.lower(), mot2.lower()
    ratio_levenshtein = levenshtein(mot1, mot2, ratio=True, lowercase=True)
    set1, set2 = set(mot1_lower), set(mot2_lower)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    jaccard = intersection / union if union > 0 else 0

    similarite_position = 0
    min_len = min(len(mot1_lower), len(mot2_lower))
    for i in range(min_len):
        if mot1_lower[i] == mot2_lower[i]:
            similarite_position += 1
    similarite_position /= max(len(mot1_lower), len(mot2_lower)) if max(len(mot1_lower), len(mot2_lower)) > 0 else 1

    bigrammes1 = get_bigrams(mot1_lower)
    bigrammes2 = get_bigrams(mot2_lower)
    bigrammes_communs = len(set(bigrammes1) & set(bigrammes2))
    similarite_bigrammes = bigrammes_communs / max(len(bigrammes1), len(bigrammes2)) if max(len(bigrammes1), len(bigrammes2)) > 0 else 0

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
        if i == 0:
            poids = 2.0
        elif i == min_len - 1:
            poids = 1.5
        else:
            poids = 0.5 + (0.5 * (1 - i/min_len))
        
        if mot1_lower[i] == mot2_lower[i]:
            score_total += poids
        poids_total += poids
    
    penalite_longueur = abs(len(mot1_lower) - len(mot2_lower)) * 0.3
    score_pondere = (score_total / poids_total) if poids_total > 0 else 0
    score_final = max(0, score_pondere - penalite_longueur / max_len)
    
    return min(score_final, 1.0)

def similarite_orthographique_avancee_ponderee(mot1, mot2):
    """
    Version amelioree avec ponderation cognitive des positions
    """
    mot1_lower, mot2_lower = mot1.lower(), mot2.lower()
    ratio_levenshtein = levenshtein(mot1, mot2, ratio=True, lowercase=True)
    set1, set2 = set(mot1_lower), set(mot2_lower)
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    jaccard = intersection / union if union > 0 else 0

    similarite_pos = similarite_position_ponderee(mot1, mot2)

    bigrammes1 = get_bigrams(mot1_lower)
    bigrammes2 = get_bigrams(mot2_lower)
    if not bigrammes1 or not bigrammes2:
        similarite_bigrammes = 0
    else:
        bigrammes_communs_ponderes = 0
        total_ponderation = 0
        for i, bigram in enumerate(bigrammes1):
            if bigram in bigrammes2:
                if i == 0 or i == len(bigrammes1) - 1:
                    poids = 1.5
                else:
                    poids = 1.0
                bigrammes_communs_ponderes += poids
            total_ponderation += 1.0
        similarite_bigrammes = bigrammes_communs_ponderes / total_ponderation

    score_final = (0.25 * ratio_levenshtein +
                   0.15 * jaccard +
                   0.45 * similarite_pos +
                   0.15 * similarite_bigrammes)

    return min(score_final, 1.0)