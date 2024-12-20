from pydantic import BaseModel

class StreamingPackageSchema(BaseModel):
    id: int
    name: str
    monthly_price_cents: int
    monthly_price_yearly_subscription_in_cents: int

    class Config:
        from_attributes = True