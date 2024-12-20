from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Absoluten Pfad zur .env-Datei anzeigen
env_path = os.path.abspath("../.env")
print(f"Absoluter Pfad zur .env: {env_path}")

# Überprüfe, ob die .env-Datei existiert
if os.path.exists(env_path):
    print(f".env-Datei gefunden: {env_path}")
else:
    print(f".env-Datei nicht gefunden: {env_path}")

# .env laden
load_dotenv(dotenv_path=env_path)

# Werte aus der .env-Datei laden
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

print(f"DB_USER: {os.getenv('POSTGRES_USER')}")
print(f"DB_PASSWORD: {os.getenv('POSTGRES_PASSWORD')}")
print(f"DB_NAME: {os.getenv('POSTGRES_DB')}")
print(f"DB_HOST: {os.getenv('POSTGRES_HOST')}")
print(f"DB_PORT: {os.getenv('POSTGRES_PORT')}")


# Ensure DB_PORT is an integer
if DB_PORT is not None:
    DB_PORT = int(DB_PORT)

# Verbindung zur PostgreSQL-Datenbank
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Testabfrage
with engine.connect() as connection:
    result = connection.execute(text("SELECT * FROM games LIMIT 5;"))
    for row in result:
        print(row)