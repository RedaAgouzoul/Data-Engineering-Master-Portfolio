# TP 1 : Pipeline ETL - API Météo & PostgreSQL 🌦️🚌

Ce dossier contient le premier TP du module de Data Processing & Feature Engineering.

## 🎯 Objectifs réalisés
1. **Extraction via API REST :** Récupération de données météorologiques en direct via OpenWeatherMap.
2. **Conteneurisation :** Mise en place d'une base de données PostgreSQL via `docker-compose`.
3. **Extraction SQL & Jointure :** Requêtage de données simulées de trafic de bus croisées avec la météo.
4. **Automatisation :** Planification des tâches d'extraction (Job Scheduling) avec la librairie `schedule`.

## 🛠️ Stack Technique
* Python 3 (Pandas, SQLAlchemy, Requests)
* PostgreSQL & Docker
* DBeaver

## 🚀 Comment lancer ce TP
1. Activer l'environnement virtuel : `.\venv\Scripts\activate`
2. Installer les dépendances : `pip install -r requirements.txt`
3. Lancer la base de données : `docker compose up -d`
4. Exécuter le notebook Jupyter.