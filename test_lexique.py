import pandas as pd
import numpy as np
import random

lexique = pd.read_csv("Lexique383.tsv", sep="\t", encoding="utf-8")

def get_freq_livre(mot):
    row = lexique[lexique["ortho"] == mot.lower()]
    if not row.empty:
        return row.iloc[0]["freqlivres"]
    else:
        return 0

# Exemple de boucle modifiée (à adapter selon le contexte réel)
for mot_affiche in ["exemple", "test", "mot"]:
    freq = get_freq_livre(mot_affiche)
    log_freq = np.log(freq + 1)
    t_identification_corrige = 220 - 10 * log_freq + random.gauss(0, 20)
    print(f"Mot: {mot_affiche} | Temps: {t_identification_corrige:.2f} ms | Freq : {freq:.1f}")
