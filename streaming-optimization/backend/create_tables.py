from app.db.database import engine
from app.models import Base

# Tabellen basierend auf den Modellen erstellen
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tabellen erfolgreich erstellt:)")

if __name__ == "__main__":
    create_tables()