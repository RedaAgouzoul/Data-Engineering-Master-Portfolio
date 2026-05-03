# 🌊 TP 1 (Avancé) : Architecture Streaming avec Apache Kafka

Ce projet est l'évolution temps réel (Event-Driven) du TP1. L'objectif est de remplacer un traitement Batch classique par une architecture de Streaming distribuée, résiliente et découplée en utilisant **Apache Kafka (mode KRaft)**.

## 🎯 Objectifs & Implémentation
1. **Découplage API (Producer/Consumer) :** Création d'un Producer qui interroge l'API OpenWeatherMap et pousse les données brutes dans le `weather_topic`. Un Consumer indépendant récupère ces données pour les sauvegarder.
2. **CDC Simulé (Change Data Capture) :** Mise en place d'un script Python (Producer SQL) qui surveille une base de données **PostgreSQL**. Il utilise la technique du *High-Water Mark* (gestion d'état via un tracker file) pour n'extraire que les nouvelles lignes insérées (Delta) et les envoyer dans le `bus_topic`.
3. **Idempotence :** Implémentation d'un registre en mémoire dans les Consumers pour détecter et rejeter les messages en doublon grâce à des `event_id` uniques.

## 🛠️ Stack Technique
* **Infrastructure :** Docker & Docker Compose
* **Message Broker :** Apache Kafka (Image officielle `apache/kafka:3.7.0`)
* **Base de données :** PostgreSQL 15
* **Langage :** Python 3 (`kafka-python`, `pandas`, `sqlalchemy`, `requests`)

## 🚀 Lancement
1. Démarrer les conteneurs : `docker compose up -d`
2. Lancer les Consumers : `python consumer_meteo.py` et `python consumer_sql.py`
3. Lancer les Producers : `python producer_meteo.py` et `python producer_sql.py`