"""
This script defines the database models for the sports streaming application using SQLAlchemy.
It includes three main tables:
1. `Game`: Stores information about games (e.g., teams, start time, and tournament name).
2. `StreamingPackage`: Stores information about streaming packages (e.g., name, monthly prices).
3. `StreamingOffer`: Links games and streaming packages, indicating if live streaming or highlights are available.
Relationships between tables are defined to facilitate easy querying.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Basis-Klasse für alle SQLAlchemy-Tabellen
Base = declarative_base()

# Tabelle für Spiele
class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_home = Column(String, nullable=False)
    team_away = Column(String, nullable=False)
    starts_at = Column(DateTime, nullable=False)
    tournament_name = Column(String, nullable=False)

    # Beziehung zu Streaming Offers
    streaming_offers = relationship("StreamingOffer", back_populates="game")

# Tabelle für Streaming-Pakete
class StreamingPackage(Base):
    __tablename__ = "streaming_packages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    monthly_price_cents = Column(Integer, nullable=True)
    monthly_price_yearly_subscription_in_cents = Column(Integer, nullable=True)

    # Beziehung zu Streaming Offers
    streaming_offers = relationship("StreamingOffer", back_populates="package")

# Tabelle für Streaming-Angebote
class StreamingOffer(Base):
    __tablename__ = "streaming_offers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    streaming_package_id = Column(Integer, ForeignKey("streaming_packages.id"), nullable=False)
    live = Column(Boolean, nullable=False)
    highlights = Column(Boolean, nullable=False)

    # Beziehungen zu anderen Tabellen
    game = relationship("Game", back_populates="streaming_offers")
    package = relationship("StreamingPackage", back_populates="streaming_offers")