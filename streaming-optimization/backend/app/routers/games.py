"""
This FastAPI router handles HTTP GET requests to retrieve game information from the database.
Key features:
1. Filters games by optional query parameters: `team_home`, `team_away`, and `tournament_name` (case-insensitive).
2. Implements pagination using `limit` (maximum results) and `offset` (starting point).
3. Uses a dependency (`get_db`) to manage the database session.
The response is modeled as a list of `GameSchema` objects.
"""

from typing import List
from fastapi import FastAPI, APIRouter, Query, Depends
from sqlalchemy.orm import Session
from app.schemas.game_schema import GameSchema
from app.db.database import SessionLocal
from app.models import Game

router = APIRouter()

# Dependency: Datenbank-Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[GameSchema], tags=["Games"])
def get_games(
    team_home: str = None,
    team_away: str = None,
    tournament_name: str = None, 
    db: Session = Depends(get_db)
):
    query = db.query(Game)

    # Filter hinzufügen
    if team_home:
        query = query.filter(Game.team_home.ilike(f"%{team_home}%"))
    if team_away:
        query = query.filter(Game.team_away.ilike(f"%{team_away}%"))
    if tournament_name:
        query = query.filter(Game.tournament_name.ilike(f"%{tournament_name}%"))

    # Ergebnisse zurückgeben
    return query.all()


