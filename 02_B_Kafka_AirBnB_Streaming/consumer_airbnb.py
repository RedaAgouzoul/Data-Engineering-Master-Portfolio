import json
import pandas as pd
import os
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'airbnb_topic',
    bootstrap_servers=['localhost:9092'],
    group_id='airbnb_cleaners',
    auto_offset_reset='earliest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🎧 Consumer AirBnB en écoute...")

# Notre fameuse "Salle d'attente" (Micro-batch)
salle_d_attente =[]
TAILLE_MICRO_BATCH = 1000

for message in consumer:
    event = message.value
    salle_d_attente.append(event)
    
    # Quand on a atteint 1000 lignes, on nettoie !
    if len(salle_d_attente) == TAILLE_MICRO_BATCH:
        print(f"🧹 Nettoyage d'un lot de {TAILLE_MICRO_BATCH} annonces en cours...")
        
        # 1. Conversion de la salle d'attente en DataFrame Pandas
        df = pd.DataFrame(salle_d_attente)
        
        # --- DÉBUT DU CODE DU TP2 (NETTOYAGE) ---
        
        # A. Valeurs manquantes
        if 'reviews_per_month' in df.columns:
            df['reviews_per_month'] = df['reviews_per_month'].fillna(0)
        if 'last_review' in df.columns:
            df = df.dropna(subset=['last_review'])
            
        # B. Nettoyage des dates
        df['last_review'] = pd.to_datetime(df['last_review'], errors='coerce')
        
        # C. Suppression des Outliers (IQR sur la colonne 'price')
        if 'price' in df.columns:
            # On s'assure que le prix est un nombre
            df['price'] = pd.to_numeric(df['price'], errors='coerce')
            Q1 = df['price'].quantile(0.25)
            Q3 = df['price'].quantile(0.75)
            IQR = Q3 - Q1
            # On garde ce qui est normal
            df = df[(df['price'] >= Q1 - 1.5 * IQR) & (df['price'] <= Q3 + 1.5 * IQR)]
            
        # D. Encodage One-Hot (Optionnel, parfois on le fait juste avant l'IA, mais voici la syntaxe)
        colonnes_a_encoder = [col for col in ['room_type', 'neighbourhood'] if col in df.columns]
        if colonnes_a_encoder:
            df = pd.get_dummies(df, columns=colonnes_a_encoder, drop_first=True)
            
        # --- FIN DU NETTOYAGE ---
        
        # 2. Sauvegarde du lot propre dans notre fichier final
        file_exists = os.path.isfile('clean_airbnb_streaming.csv')
        df.to_csv('clean_airbnb_streaming.csv', mode='a', header=not file_exists, index=False)
        print(f"✅ Lot propre sauvegardé. Lignes restantes après nettoyage : {len(df)}")
        
        # 3. On vide la salle d'attente pour les prochains events !
        salle_d_attente.clear()