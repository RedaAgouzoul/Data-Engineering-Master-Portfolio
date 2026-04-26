import os
import json
import time
import requests
import schedule
from datetime import datetime
from dotenv import load_dotenv
from kafka import KafkaProducer

# 1. Charger les variables d'environnement (Sécurité)
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
CITY = 'Casablanca'

# 2. Configuration du Kafka Producer
# 'bootstrap_servers' : l'adresse de notre Docker Kafka
# 'value_serializer' : Kafka ne comprend que les "bytes". On lui dit comment traduire notre dictionnaire Python en JSON, puis en bytes.
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def fetch_and_publish_weather():
    """Récupère la météo et l'envoie dans Kafka"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            # 3. Création de notre ID métier (ex: Casablanca-20260426-1520)
            timestamp_str = datetime.now().strftime("%Y%m%d-%H%M")
            event_id = f"{CITY}-{timestamp_str}"
            
            # 4. Création de l'Event (Le JSON)
            event = {
                "event_id": event_id,
                "ville": data["name"],
                "temperature": data["main"]["temp"],
                "humidite": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "timestamp": timestamp_str
            }
            
            # 5. Envoi au Broker Kafka dans le topic 'weather_topic'
            producer.send('weather_topic', value=event)
            
            # 6. Flush force l'envoi immédiat (sinon Kafka attend d'avoir un gros paquet pour envoyer)
            producer.flush() 
            print(f"🚀[ENVOYÉ] Météo de {CITY} envoyée avec succès ! (ID: {event_id})")
            
        else:
            print(f"❌ Erreur API : {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Erreur de connexion : {e}")

# 7. Automatisation : On lance la fonction toutes les 1 minute
schedule.every(1).minutes.do(fetch_and_publish_weather)

print("📡 Producer Météo démarré. En attente de l'envoi des messages vers Kafka...")

# Pour tester sans attendre 1 minute la première fois, on l'appelle manuellement une fois :
fetch_and_publish_weather()

while True:
    schedule.run_pending()
    time.sleep(1)