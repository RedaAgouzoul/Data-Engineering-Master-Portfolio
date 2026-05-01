import os
import json
import time
import pandas as pd
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

DOSSIER_CHUNKS = "chunks_data"

print("🚀 Producer AirBnB démarré...")

# 1. On liste tous les petits fichiers qu'on a créés
fichiers = sorted(os.listdir(DOSSIER_CHUNKS))

for fichier in fichiers:
    if fichier.endswith(".csv"):
        print(f"📂 Lecture du fichier : {fichier}...")
        
        # 2. On lit le petit fichier
        chemin_complet = os.path.join(DOSSIER_CHUNKS, fichier)
        df_chunk = pd.read_csv(chemin_complet)
        
        # 3. LA CONSIGNE DU PROF : On push ligne par ligne (1 ligne = 1 event)
        for index, row in df_chunk.iterrows():
            # On transforme la ligne Pandas en Dictionnaire, on gère les NaN en mettant None
            event = row.where(pd.notnull(row), None).to_dict()
            
            # On envoie l'event dans Kafka
            producer.send('airbnb_topic', value=event)
            
            # On fait une micro-pause pour simuler le temps réel
            time.sleep(0.01) 
            
        producer.flush()
        print(f"✅ {len(df_chunk)} lignes envoyées depuis {fichier}.")
        
        # On attend 5 secondes avant de lire le prochain fichier (simule l'arrivée du mois suivant)
        time.sleep(5)