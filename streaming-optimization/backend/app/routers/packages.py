"""
This FastAPI router handles advanced queries and calculations for streaming packages and their relation to games and teams.

Key features:
1. `get_streaming_packages`: Retrieves streaming packages with optional filters for name and prices.
2. `get_packages_by_teams`: Retrieves packages that stream games for specific teams.
3. `rank_streaming_packages`: Ranks streaming packages based on the number of streamed games for specified teams.
4. `get_optimal_package_combination`: Calculates the optimal combination of streaming packages to cover all games for a given list of teams at the minimum cost.

Pagination is implemented where applicable, and advanced SQL queries are used for filtering, grouping, and ranking.
"""


from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.package_schema import StreamingPackageSchema
from sqlalchemy.sql import func
from app.db.database import SessionLocal
from app.models import StreamingPackage, Game, StreamingOffer


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[StreamingPackageSchema], tags=["Streaming Packages"])
def get_streaming_packages(
    name: Optional[str] = None,
    monthly_price_cents: Optional[int] = None,
    monthly_price_yearly_subscription_in_cents: Optional[int] = None,
    limit: int = 10,
    offset: int = 0, 
    db: Session = Depends(get_db)
):
    """
    Abfragen von Streaming-Paketen mit optionalen Filtern wie Name und Preis.
    """
    query = db.query(StreamingPackage)
    
    if name is not None:
        query = query.filter(StreamingPackage.name.ilike(f"%{name}%"))
    if monthly_price_cents is not None:
        query = query.filter(StreamingPackage.monthly_price_cents == monthly_price_cents)
    if monthly_price_yearly_subscription_in_cents is not None:
        query = query.filter(StreamingPackage.monthly_price_yearly_subscription_in_cents == monthly_price_yearly_subscription_in_cents)
    
    query = query.limit(limit).offset(offset)
    results = query.all()

    return results


@router.get("/teams", response_model=List[StreamingPackageSchema], tags=["Streaming Packages"])
def get_packages_by_teams(
    teams: List[str] = Query(..., description="List of team names"), 
    limit: int = Query(10, ge=1),
    # offset: int = Query(10, ge=0),
    db: Session = Depends(get_db)
):
    """
    Abfragen von Streaming-Paketen basierend auf den Teams, die gestreamt werden.
    """
    
    # Finde Spiele
    games_query = db.query(Game).filter(
        (Game.team_home.in_(teams)) | (Game.team_away.in_(teams))
    )
    games = games_query.all()
   
    """
    Debugging 
    print("Gefundene Spiele:", games)
    print("SQL-Query für Spiele:", games_query.statement)
    print([{"id": game.id, "team_home": game.team_home, "team_away": game.team_away} for game in games])
    """

    # Finde Angebote
    offers_query = db.query(StreamingOffer).filter(StreamingOffer.game_id.in_([game.id for game in games]))
    offers = offers_query.all()
    
    # Finde Pakete
    packages_query = db.query(StreamingPackage).filter(StreamingPackage.id.in_([offer.streaming_package_id for offer in offers]))
    package_ids = [offer.streaming_package_id for offer in offers]
    
    query = packages_query # TODO:  Paginierung? 
    results = query.all()

    print("Gefundene Pakete:", results)
    return results


@router.get("/ranked", tags=["Streaming Packages"])
def rank_streaming_packages(
    teams: List[str] = Query(..., description="List of team names"),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Ranking der Streaming-Pakete basierend auf der Verfügbarkeit gestreamter Spiele.
    """
    # SQL-Abfrage mit Ranking
    query = (
        db.query(
            StreamingPackage.id.label("package_id"),
            StreamingPackage.name.label("package_name"),
            StreamingPackage.monthly_price_cents,
            StreamingPackage.monthly_price_yearly_subscription_in_cents,
            func.count(StreamingOffer.game_id).label("streamed_matches")
        )
        .join(StreamingOffer, StreamingOffer.streaming_package_id == StreamingPackage.id)
        .join(Game, StreamingOffer.game_id == Game.id)
        .filter((Game.team_home.in_(teams)) | (Game.team_away.in_(teams)))
        .group_by(StreamingPackage.id)
        .order_by(func.count(StreamingOffer.game_id).desc())  # Sortiere nach gestreamten Spielen
        .limit(limit)
        .offset(offset)
    )

    results = query.all()

    # Rückgabe formatieren
    return [
        {
            "package_id": row.package_id,
            "package_name": row.package_name,
            "monthly_price_cents": row.monthly_price_cents,
            "monthly_price_yearly_subscription_in_cents": row.monthly_price_yearly_subscription_in_cents,
            "streamed_matches": row.streamed_matches,
        }
        for row in results
    ]

@router.get("/optimal-combination", tags=["Streaming Packages"])
def get_optimal_package_combination(
    teams: List[str] = Query(..., description="List of team names"),
    db: Session = Depends(get_db),
):
    """
    Find the smallest price combination of streaming packages to cover all games for the given teams.
    """
    # Step 1: Find all relevant games for the given teams
    print("Teams:", teams)
    games = db.query(Game).filter(
        (Game.team_home.in_(teams)) | (Game.team_away.in_(teams))
    ).all()
    print("Games:", games)
    if not games:
        return {"message": "No games found for the specified teams."}

    game_ids = {game.id for game in games}

    # Step 2: Find all streaming offers for these games
    offers = db.query(StreamingOffer).filter(StreamingOffer.game_id.in_(game_ids)).all()

    # Step 3: erstelle Mapping: Paket -> Spiele
    package_to_games = {}
    for offer in offers:
        if offer.streaming_package_id not in package_to_games:
            package_to_games[offer.streaming_package_id] = set()
        package_to_games[offer.streaming_package_id].add(offer.game_id)

    # Step 4: Paketpreise abrufen
    packages = db.query(StreamingPackage).filter(
        StreamingPackage.id.in_(package_to_games.keys())
    ).all()
    package_prices = {pkg.id: pkg.monthly_price_cents for pkg in packages}

    print("Package Prices:", package_prices)

    # Step 5: Kostenfreie Pakete berücksichtigen
    selected_packages = []
    covered_games = set()

    for package_id, price in package_prices.items():
        if price == 0 and (package_to_games[package_id] - covered_games):
            selected_packages.append({"id": package_id, "price_cents": price})
            covered_games.update(package_to_games[package_id])

    # Step 6: Kostenpflichtige Pakete hinzufügen, wenn nötig
    while covered_games != game_ids:
        # Find the package that covers the most uncovered games for the lowest price
        best_package = None
        best_value = 0  # Value = games covered / price
        for package_id, games in package_to_games.items():
            if package_id in [pkg["id"] for pkg in selected_packages]:
                continue  # Berets ausgewählte Pakete überspringen

            uncovered_games = games - covered_games
            if uncovered_games and package_prices[package_id] > 0:  # Exclude free packages here
                value = len(uncovered_games) / package_prices[package_id]
                if value > best_value:
                    best_value = value
                    best_package = package_id

        if not best_package:
            return {"message": "Cannot cover all games with available packages."}

        # Package hinzufügen
        selected_packages.append(
            {"id": best_package, "price_cents": package_prices[best_package]}
        )
        covered_games.update(package_to_games[best_package])

    print("Teams:", teams)
    print("Game IDs:", [game.id for game in games])
    print("Package Prices:", package_prices)
    print("Package to Games Mapping:", package_to_games)

    # Step 7: Gesamtpreis berechnen
    total_price = sum(pkg["price_cents"] for pkg in selected_packages)
    return {
        "selected_packages": selected_packages,
        "total_price_cents": total_price,
    }