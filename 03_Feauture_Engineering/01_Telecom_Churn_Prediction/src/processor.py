import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, OneHotEncoder, KBinsDiscretizer
from sklearn.decomposition import PCA

def construire_pipeline():
    """
    Construit l'usine de transformation (Le Pipeline).
    C'est ici qu'on définit QUOI faire sur QUELLE colonne.
    """
    
    # 1. Stratégie pour les Outliers (Revenu et Data)
    # On utilise RobustScaler (Valeur Ajoutée Senior) qui ignore les extrêmes.
    pipeline_numerique = Pipeline(steps=[
        ('scaler', RobustScaler()) 
    ])

    # 2. Stratégie pour l'Âge (Discrétisation)
    # On transforme l'âge exact en 4 tranches (Jeune, Adulte, Senior, etc.)
    # strategy='quantile' est l'équivalent de qcut (même nombre de personnes par boîte)
    pipeline_age = Pipeline(steps=[
        ('discretizer', KBinsDiscretizer(n_bins=4, encode='ordinal', strategy='quantile'))
    ])

    # 3. Stratégie pour le texte (One-Hot Encoding)
    # Transforme 'Basic', 'Premium' en colonnes de 0 et 1.
    pipeline_categoriel = Pipeline(steps=[
        ('onehot', OneHotEncoder(drop='first', sparse_output=False)) # drop='first' évite la colinéarité !
    ])

    # --- L'AIGUILLAGE (ColumnTransformer) ---
    # On relie nos stratégies aux vraies colonnes du fichier
    preprocesseur = ColumnTransformer(
        transformers=[
            ('num', pipeline_numerique, ['Revenu_Mensuel', 'Data_Consommee_GB']),
            ('age_bins', pipeline_age, ['Age']),
            ('cat', pipeline_categoriel, ['Type_Abonnement'])
        ],
        remainder='drop' # 'drop' jette les colonnes non listées (comme l'ID_Client qui ne sert à rien)
    )

    return preprocesseur