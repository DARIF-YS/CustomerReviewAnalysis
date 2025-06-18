import time
import pandas as pd
from googletrans import Translator
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

def load():

    current_dir = os.path.dirname(os.path.abspath(__file__))
    path        = os.path.join(current_dir, '..', 'raw_data', 'raw_data.json')

    df = pd.read_json(path)
    df.index.name = 'id'
    df = df.reset_index()
    
    translator = Translator()

    def translate_text(text):
        if text is None or text == '':
            return None
        else:
            try:
                print(f"Bien fait 😎")
                translation = translator.translate(text, dest='en')
                return translation.text
            except Exception as e:
                print(f"Translation error: {e}")
                return None

    df['en_review'] = df['review_text'].apply(translate_text)
    
    # Charger les variables d'environnement depuis le fichier .env
    load_dotenv()

    # Lire les paramètres de connexion depuis les variables d'environnement
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host     = os.getenv("DB_HOST")
    port     = os.getenv("DB_PORT")
    database = os.getenv("DB_NAME")

        # Construire l'URL de connexion PostgreSQL
    DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

    # Créer le moteur SQLAlchemy
    engine = create_engine(DATABASE_URL)

    df.to_sql('bank_reviews', engine, if_exists='replace', index=False)

