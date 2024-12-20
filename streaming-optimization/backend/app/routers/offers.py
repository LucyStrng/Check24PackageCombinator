"""
This FastAPI router handles HTTP GET requests to retrieve streaming offers from the database.
Key features:
1. Filters streaming offers by optional query parameters: `game_id`, `streaming_package_id`, `live`, and `highlights`.
2. Implements pagination using `limit` (maximum results) and `offset` (starting point).
3. Uses a dependency (`get_db`) to manage the database session.
The response is modeled as a list of `StreamingOfferSchema` objects.
"""

from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.offer_schema import StreamingOfferSchema
from app.db.database import SessionLocal
from app.models import StreamingOffer

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint for streaming_offers
@router.get("/", response_model=List[StreamingOfferSchema], tags=["Streaming Offers"])
def get_streaming_offers(
    game_id: int = None,
    streaming_package_id: int = None,
    live: bool = None,
    highlights: bool = None,
    limit: int = 10,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    query = db.query(StreamingOffer)
    if game_id:
        query = query.filter(StreamingOffer.game_id == game_id)
    if streaming_package_id:
        query = query.filter(StreamingOffer.streaming_package_id == streaming_package_id)
    if live is not None:
        query = query.filter(StreamingOffer.live == live)
    if highlights is not None:
        query = query.filter(StreamingOffer.highlights == highlights)
    query = query.limit(limit).offset(offset)
    return query.all()