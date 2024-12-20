import os
import sys
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session, sessionmaker # type: ignore

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.database import engine
from app.models import Game, StreamingOffer, StreamingPackage

# Absoluter Pfad zur CSV-Datei
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data")

def load_games(db: Session, csv_path: str):
    """Lädt die 'games'-Daten in die Datenbank."""
    db.query(StreamingOffer).delete()  # Löschen Sie zuerst die referenzierten Einträge
    db.commit()
    db.query(Game).delete()
    db.commit()
    games_df = pd.read_csv(csv_path)
    for _, row in games_df.iterrows():
        game = Game(
            id=int(row['id']),
            team_home=row['team_home'],
            team_away=row['team_away'],
            tournament_name=row['tournament_name'],
            starts_at=row['starts_at']  # Verwenden Sie 'starts_at' anstelle von 'date'
        )
        db.add(game)
    db.commit()
    print("Spiele erfolgreich geladen.")

def load_streaming_packages(db: Session, csv_path: str):
    """Lädt die 'streaming_packages'-Daten in die Datenbank."""
    db.query(StreamingPackage).delete()
    db.commit()
    packages_df = pd.read_csv(csv_path)
    for _, row in packages_df.iterrows():
        package = StreamingPackage(
            id=int(row['id']),
            name=row['name'],
            monthly_price_cents=int(row['monthly_price_cents']) if not pd.isna(row['monthly_price_cents']) else 0,
            monthly_price_yearly_subscription_in_cents=int(row['monthly_price_yearly_subscription_in_cents']) if not pd.isna(row['monthly_price_yearly_subscription_in_cents']) else 0
        )
        db.add(package)
    db.commit()
    print("Streaming-Pakete erfolgreich geladen.")
    
def load_streaming_offers(db: Session, csv_path: str):
    """Lädt die 'streaming_offers'-Daten in die Datenbank."""
    db.query(StreamingOffer).delete()
    db.commit()
    offers_df = pd.read_csv(csv_path)
    for _, row in offers_df.iterrows():
        offer = StreamingOffer(
            game_id=int(row['game_id']),
            streaming_package_id=int(row['streaming_package_id']),
            live=bool(row['live']), 
            highlights=bool(row['highlights']) 
        )
        db.add(offer)
    db.commit()
    print("Streaming-Angebote erfolgreich geladen.")


def main():
    # Beispielpfade zu den CSV-Dateien
    games_csv = os.path.join(DATA_DIR, "bc_game.csv")
    packages_csv = os.path.join(DATA_DIR, "bc_streaming_package.csv")
    offers_csv = os.path.join(DATA_DIR, "bc_streaming_offer.csv")

    # Datenbankverbindung herstellen
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    # Daten laden
    load_games(session, games_csv)
    load_streaming_packages(session, packages_csv)
    load_streaming_offers(session, offers_csv)

if __name__ == "__main__":
    main()