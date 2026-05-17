import pandas as pd
from src.processor import construire_pipeline

def main():
    print("🚀 Démarrage du Feature Engineering Telecom...")

    # 1. Charger les données brutes
    df_raw = pd.read_csv("data/raw_telecom.csv")
    print(f" Taille des données brutes : {df_raw.shape}")

    # 2. Séparer la Cible (Target) du reste
    # On ne transforme JAMAIS la cible (A_Resilie), on la met de côté
    X = df_raw.drop(columns=['A_Resilie'])
    y = df_raw['A_Resilie']

    # 3. Construire et Appliquer l'usine (Le Pipeline)
    usine_transformation = construire_pipeline()
    
    # fit_transform = l'usine "apprend" les maths des données ET les transforme
    X_transforme_numpy = usine_transformation.fit_transform(X)

    # 4. Reconstruire un beau tableau Pandas
    # Quand Scikit-Learn travaille, il détruit les noms des colonnes et sort une matrice Numpy.
    # Pour un Senior, on récupère les noms générés par l'usine :
    noms_colonnes = usine_transformation.get_feature_names_out()
    df_clean = pd.DataFrame(X_transforme_numpy, columns=noms_colonnes)
    
    # On recolle la cible (A_Resilie) à la fin du tableau propre
    df_clean['A_Resilie'] = y.values

    # 5. Sauvegarde
    df_clean.to_csv("data/processed_telecom.csv", index=False)
    print(f"✅ Données transformées avec succès ! Taille finale : {df_clean.shape}")
    
    print("\nAperçu des 5 premières lignes propres :")
    print(df_clean.head())

if __name__ == "__main__":
    main()