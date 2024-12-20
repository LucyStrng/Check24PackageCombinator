import datetime
from pydantic import BaseModel, SkipValidation

class GameSchema(BaseModel):
    id: int
    team_home: str
    team_away: str
    starts_at: SkipValidation[datetime]
    tournament_name: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True