# 🧹 TP 2 (Avancé) : Ingestion et Data Cleaning en Streaming

L'objectif de ce projet est de simuler un flux de données en temps réel à partir d'un dataset statique massif (AirBnB), et d'appliquer des transformations Data Science à la volée en utilisant le concept de **Micro-Batching**.

## 🎯 Architecture & Traitements
1. **Échantillonnage et Spooling :** Un script préparatoire trie le dataset par prix et distribue les lignes intelligemment dans plusieurs sous-fichiers. Cela garantit que chaque morceau est un échantillon représentatif de la réalité économique.
2. **Streaming Ligne par Ligne :** Le Producer Kafka lit ces sous-fichiers et pousse les annonces **une par une** dans le broker.
3. **Micro-Batching (Consumer) :** Le Consumer accumule les événements dans une mémoire tampon. Lorsqu'il atteint un lot de 1000 lignes, il déclenche le pipeline de nettoyage complet :
   * Traitement des valeurs manquantes (`NaN`) et des formats de dates.
   * Calcul des Quartiles (Q1, Q3, IQR) et suppression des **Outliers** (prix aberrants).
   * Encodage One-Hot des variables catégorielles.
   * Sauvegarde du lot propre en mode "Append".

## 🛠️ Stack Technique
* Apache Kafka (Docker)
* Python 3 (`kafka-python`, `pandas`)

## 🚀 Lancement
1. Allumer Kafka : `docker compose up -d`
2. Découper la donnée : `python 0_split_data.py`
3. Démarrer le nettoyeur : `python consumer_airbnb.py`
4. Démarrer le flux : `python producer_airbnb.py`