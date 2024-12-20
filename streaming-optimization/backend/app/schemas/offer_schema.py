from pydantic import BaseModel

class StreamingOfferSchema(BaseModel):
    id: int
    game_id: int
    streaming_package_id: int
    live: bool
    highlights: bool

    class Config:
        from_attributes = True
