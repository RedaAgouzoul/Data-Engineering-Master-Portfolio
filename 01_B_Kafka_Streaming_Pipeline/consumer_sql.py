import json
import pandas as pd
import os
from kafka import KafkaConsumer

# 1. Registre d'Idempotence
processed_ids = set()

# 2. Configuration du Consumer
consumer = KafkaConsumer(
    'bus_topic', # ATTENTION : On écoute le tuyau des bus, pas la météo !
    bootstrap_servers=['localhost:9092'],
    group_id='bus_group_1', # Nouveau groupe pour les bus
    auto_offset_reset='earliest', # On rattrape tout l'historique
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🎧 Consumer Bus prêt. En écoute de Kafka...")

# 3. Boucle de Streaming
for message in consumer:
    event = message.value
    event_id = event.get("event_id")
    
    if event_id in processed_ids:
        print(f"⚠️ Doublon ignoré : {event_id}")
        continue
        
    print(f"✅ Nouveau trajet de bus traité : {event_id}")
    
    # 4. Sauvegarde
    df = pd.DataFrame([event])
    file_exists = os.path.isfile('bus_streaming.csv')
    
    # On ajoute au CSV sans écraser (mode='a')
    df.to_csv('bus_streaming.csv', mode='a', header=not file_exists, index=False)
    
    processed_ids.add(event_id)