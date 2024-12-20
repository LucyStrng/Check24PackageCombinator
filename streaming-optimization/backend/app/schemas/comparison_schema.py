from pydantic import BaseModel

class StreamingPackageResponse(BaseModel):
    package_name: str
    monthly_price_cents: int
    streamed_matches: int

    class Config:
        from_attributes = True  