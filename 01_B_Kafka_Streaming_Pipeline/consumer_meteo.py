import json
import pandas as pd
import os
from kafka import KafkaConsumer

# 1. Registre d'Idempotence (La mémoire de notre Consumer)
# On utilise un "set" Python (une liste qui n'accepte pas les doublons)
processed_ids = set()

# 2. Configuration du Consumer
consumer = KafkaConsumer(
    'weather_topic', # Le tuyau qu'on écoute
    bootstrap_servers=['localhost:9092'],
    group_id='meteo_group_1', # Notre Consumer Group (Kafka retient nos offsets grâce à ça)
    auto_offset_reset='earliest', # Si on a raté des messages pendant qu'on était éteint, on recommence au premier non lu
    value_deserializer=lambda x: json.loads(x.decode('utf-8')) # On traduit les bytes en dictionnaire Python
)

print("🎧 Consumer Météo prêt. En écoute de Kafka...")

# 3. Écoute en Streaming (Boucle infinie)
for message in consumer:
    # On récupère le JSON
    event = message.value
    event_id = event.get("event_id") # Ex: Casablanca-20260426-1520
    
    # 4. Contrôle d'Idempotence (Le filtre intelligent)
    if event_id in processed_ids:
        print(f"⚠️ Doublon ignoré : {event_id}")
        continue # On arrête là et on passe au message suivant
        
    print(f"✅ Nouveau message traité : {event_id}")
    
    # 5. Transformation et Sauvegarde (Mode Append)
    # On met le dictionnaire dans une liste pour que Pandas comprenne
    df = pd.DataFrame([event])
    
    # On vérifie si le fichier CSV existe déjà pour savoir s'il faut écrire l'en-tête
    file_exists = os.path.isfile('meteo_streaming.csv')
    
    # On écrit dans le fichier SANS écraser l'ancien (mode='a')
    df.to_csv('meteo_streaming.csv', mode='a', header=not file_exists, index=False)
    
    # 6. On note cet ID dans notre mémoire pour ne plus jamais le traiter
    processed_ids.add(event_id)