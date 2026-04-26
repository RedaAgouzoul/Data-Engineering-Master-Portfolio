# 🧹 TP 2 : Data Preprocessing & Cleaning (Cas AirBnB)

Ce dossier contient le deuxième TP du module de Data Processing & Feature Engineering. L'objectif est de préparer un jeu de données brut pour le rendre exploitable par des algorithmes de Machine Learning.

## 🎯 Objectifs réalisés
1. **Gestion des valeurs manquantes (NaN) :** Identification, suppression et imputation de données.
2. **Nettoyage des dates :** Conversion au format `datetime` et gestion des erreurs de formatage.
3. **Feature Engineering :** Encodage One-Hot (`get_dummies`) pour transformer les variables textuelles (catégorielles) en vecteurs mathématiques.
4. **Traitement des Outliers :** Utilisation de la méthode mathématique de l'Écart Interquartile (IQR) pour détecter et exclure les valeurs aberrantes (ex: prix extrêmes).

## 🛠️ Stack Technique
* Python 3
* `pandas` & `numpy` (Manipulation des données)
* `seaborn` & `matplotlib` (Visualisation des distributions et Boxplots)

## 🚀 Comment exécuter
1. Activer l'environnement virtuel : `.\venv\Scripts\activate`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer le notebook Jupyter `tp2_cleaning_airbnb.ipynb`.
*(Note : Le fichier dataset `listings.csv` n'est pas inclus sur GitHub pour des raisons de volume et de bonnes pratiques, vous devez le placer à la racine du dossier).*