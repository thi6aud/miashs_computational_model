import pandas as pd

# Chargement du fichier TSV (dans le même dossier)
lexique = pd.read_csv("Lexique383.tsv", sep="\t", encoding="utf-8")

def get_freq_livre(mot):
    row = lexique[lexique["ortho"] == mot.lower()]
    if not row.empty:
        return row.iloc[0]["freqlivres"]
    else:
        return 0  # ou None si tu veux détecter les absents
    
mot = "aBaissA"
frequence = get_freq_livre(mot)
print(f"Fréquence du mot '{mot}' : {frequence}")




