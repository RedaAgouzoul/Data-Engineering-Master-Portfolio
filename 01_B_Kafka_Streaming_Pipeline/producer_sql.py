import time
import json
import os
import pandas as pd
from sqlalchemy import create_engine
from kafka import KafkaProducer

# ==========================================
# 1. CONFIGURATION (Le matériel du Garde-Barrière)
# ==========================================

# Notre connexion à Kafka (Le chef à qui on envoie les infos)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Notre connexion à PostgreSQL (Le péage où passent les bus)
engine = create_engine("postgresql+psycopg2://postgres:admin@localhost:5432/transport_meteo")

# Le fichier "Carnet de notes" pour se souvenir du dernier bus vu
TRACKER_FILE = "last_id_read.txt"

# ==========================================
# 2. FONCTIONS DE MÉMOIRE (Le High-Water Mark)
# ==========================================

def get_last_read_id():
    """Ouvre le carnet et lit le dernier numéro d'ID. S'il est vide, on renvoie 0."""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return int(f.read().strip())
    return 0

def update_last_read_id(new_id):
    """Écrit le nouveau numéro d'ID maximum dans le carnet."""
    with open(TRACKER_FILE, "w") as f:
        f.write(str(new_id))

# ==========================================
# 3. LE MOTEUR DU STREAMING (La boucle infinie)
# ==========================================

print("🚌 Producer SQL (CDC) démarré. Surveillance de PostgreSQL en cours...")

while True:
    try:
        # On regarde dans notre carnet où on s'était arrêté
        last_id = get_last_read_id()
        
        # LA MAGIE EST ICI : On demande UNIQUEMENT les lignes strictement plus récentes !
        query = f"SELECT t.id, t.ligne, t.arret, t.date, t.nombre_passagers FROM trafic_bus t WHERE t.id > {last_id} ORDER BY t.id ASC"
        df = pd.read_sql(query, engine)
        
        # S'il y a des nouvelles lignes (le tableau n'est pas vide)
        if not df.empty:
            print(f"🔥 {len(df)} nouvelles lignes détectées dans PostgreSQL !")
            
            # On lit chaque nouvelle ligne une par une
            for index, row in df.iterrows():
                
                # On fabrique l'Event (le JSON)
                # Note: On transforme la date en texte (str) car JSON ne comprend pas le format 'Date' natif
                event = {
                    "event_id": f"BUS-{row['id']}",
                    "ligne": row['ligne'],
                    "arret": row['arret'],
                    "date": str(row['date']),
                    "nombre_passagers": row['nombre_passagers']
                }
                
                # On l'envoie dans un NOUVEAU tuyau Kafka dédié aux bus !
                producer.send('bus_topic', value=event)
                print(f"🚀 Envoyé à Kafka : Bus Ligne {row['ligne']} (ID: {row['id']})")
                
                # On met à jour notre mémoire avec cet ID
                last_id = row['id']
            
            # On force l'envoi immédiat de tous les messages
            producer.flush()
            
            # On écrit notre dernier ID dans le carnet sur le disque dur
            update_last_read_id(last_id)
            
    except Exception as e:
        print(f"⚠️ Erreur : {e}")
        
    # On attend 5 secondes avant de regarder à nouveau la base de données
    time.sleep(5)