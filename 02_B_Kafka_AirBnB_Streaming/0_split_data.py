import pandas as pd
import os

# 1. Création du dossier pour les morceaux
os.makedirs("chunks_data", exist_ok=True)

# 2. Lecture du gros fichier brut
print("Lecture du fichier original...")
df_complet = pd.read_csv("listings.csv")

# 3. LA DEMANDE DU PROF : Le Tri par prix pour l'échantillonnage
# On s'assure que le prix est un nombre, puis on trie du moins cher au plus cher
df_complet['price'] = pd.to_numeric(df_complet['price'], errors='coerce')
df_complet = df_complet.sort_values(by='price')

# 4. Le découpage (Stratégie de la "Distribution de cartes")
# Pour avoir un bon échantillon, on ne coupe pas en blocs de 1000 à la suite.
# On distribue comme des cartes : la ligne 1 va au fichier 1, la ligne 2 au fichier 2...
# Cela garantit que CHAQUE fichier aura des apparts pas chers, moyens, et chers !
nombre_de_fichiers = 10  # On va créer 10 fichiers

print(f"Découpage en {nombre_de_fichiers} échantillons représentatifs...")

for i in range(nombre_de_fichiers):
    # L'astuce mathématique (iloc[i::nombre_de_fichiers]) : 
    # Prend une ligne toutes les 10 lignes en commençant par 'i'
    df_echantillon = df_complet.iloc[i::nombre_de_fichiers]
    
    # On sauvegarde l'échantillon
    df_echantillon.to_csv(f"chunks_data/chunk_{i+1}.csv", index=False)

print("✅ Fichiers créés avec succès ! Chaque fichier contient un mix parfait de prix.")