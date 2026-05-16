import pandas as pd
import numpy as np
import os

def generer_donnees_telecom():
    np.random.seed(42)
    n = 1000 # 1000 clients

    donnees = {
        'ID_Client': range(1, n + 1),
        'Age': np.random.randint(18, 80, n),
        'Revenu_Mensuel': np.random.normal(3000, 1000, n),
        'Data_Consommee_GB': np.random.normal(50, 20, n),
        'Type_Abonnement': np.random.choice(['Basic', 'Premium', 'VIP'], n),
        'A_Resilie': np.random.choice([0, 1], n, p=[0.8, 0.2]) # 20% de gens qui quittent
    }
    
    df = pd.DataFrame(donnees)
    
    # AJOUT DE VALEURS ABERRANTES (Outliers) POUR TESTER NOTRE CODE
    df.loc[0:5, 'Data_Consommee_GB'] = [5000, 8000, 10000, 9500, 7000, 12000] # Hackers
    df.loc[10:15, 'Revenu_Mensuel'] = [-500, 150000, 200000, -100, 0, 300000] # Erreurs de saisie
    
    # Sauvegarde dans le dossier data/
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/raw_telecom.csv', index=False)
    print("✅ Fichier 'raw_telecom.csv' généré avec succès dans le dossier data/ !")

if __name__ == "__main__":
    generer_donnees_telecom()