from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Lade die .env-Datei
load_dotenv()

# Erstelle die Datenbank-URL aus den Umgebungsvariablen
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

# Verbindung testen
try:
    engine = create_engine(DATABASE_URL)
    connection = engine.connect()
    print("Verbindung erfolgreich!")
    connection.close()
except Exception as e:
    print("Verbindungsfehler:", e)