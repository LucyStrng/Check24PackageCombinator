from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.models import Game, StreamingOffer, StreamingPackage
from app.db.database import get_db

router = APIRouter()

@router.get("/")
def get_comparison_data(
    skip: int = 0, 
    limit: int = 1, 
    teams: List[str] = Query(None), 
    db: Session = Depends(get_db)
):
    
    if teams:
        # Process and clean up the teams list
        teams = [team.strip() for t in teams for team in t.split(",")]
         # Debugging: Log the cleaned list
        print("Processed Teams:", teams) 

    competitions = db.query(Game.tournament_name).distinct().offset(skip).limit(limit).all()

    response = []

    for competition in competitions:
        competition_name = competition[0]

        # Filter games by teams if provided
        game_query = db.query(Game).filter(Game.tournament_name == competition_name)
        if teams:
            game_query = game_query.filter(
                (Game.team_home.in_(teams)) | (Game.team_away.in_(teams))
            )
        # Debugging
        print("Teams for filtering:", teams) 
        games = game_query.offset(skip).limit(limit).all()

        # Query all streaming packages
        packages = db.query(StreamingPackage).all()

        # Calculate the best coverage combination (minimum price combination covering all matches)
        cheapest_combination = []
        for package in packages:
            total_price = package.monthly_price_cents or 0
            yearly_price = package.monthly_price_yearly_subscription_in_cents or 0
            cheapest_combination.append({
                "id": package.id,
                "total_price": min(total_price, yearly_price),
            })

        # Sort by price and take the top N cheapest packages
        cheapest_combination.sort(key=lambda x: x["total_price"])
        cheapest_ids = [item["id"] for item in cheapest_combination[:3]]  # Adjust the number as needed

        package_data = []

        for package in packages:
            live_status = []
            highlights_status = []

            for game in games:
                # Check if the game is available in the package
                offer = db.query(StreamingOffer).filter(
                    StreamingOffer.game_id == game.id,
                    StreamingOffer.streaming_package_id == package.id
                ).first()

                live_status.append(offer.live if offer else False)
                highlights_status.append(offer.highlights if offer else False)

            package_data.append({
                "name": package.name,
                "live": live_status,
                "highlights": highlights_status,
                "is_in_cheapest_combination": package.id in cheapest_ids  # Add flag
            })

        response.append({
            "competition": competition_name,
            "games": [{"match": f"{game.team_home} - {game.team_away}"} for game in games],
            "packages": package_data
        })

    return {
        "total_competitions": db.query(Game.tournament_name).distinct().count(),
        "total_games": db.query(Game).count(),
        "data": response
    }