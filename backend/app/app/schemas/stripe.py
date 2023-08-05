from pydantic import Field, BaseModel, HttpUrl
from datetime import datetime

from app.schema_types import CurrencyType
from app.schemas import PriceCreate
from app.core.config import settings


class StripeIntentResponse(BaseModel):
    clientSecret: str


class StripeCheckoutIntent(BaseModel):
    price_id: str
    subscriber_id: str
    ip: str


class StripeCheckoutRedirect(BaseModel):
    redirect: HttpUrl


class StripePaymentIntent(PriceCreate):
    pass


class StripeEventData(BaseModel):
    id: str
    object: str = Field(default="event")


class StripeEvent(BaseModel):
    id: str
    object: str = Field(default="event")
    api_version: str
    created: datetime
