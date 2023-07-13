from __future__ import annotations
from pydantic import Field
from typing import Optional

from app.schema_types import CurrencyType
from app.schemas.base_schema import BaseSchema


class CountryCode(BaseSchema):
    ip: str
    country_short: str
    country_long: str


class IPCode(BaseSchema):
    ip: Optional[str] = None


class PriceBase(BaseSchema):
    id: str = Field(..., description="Stripe price id generated from dashboard.")
    currency: CurrencyType = Field(..., description="Currency for the fee.")
    per_annum: Optional[int] = Field(None, description="Annual fee.")


class PriceCreate(PriceBase):
    pass


class PriceUpdate(PriceBase):
    pass


class PriceInDBBase(PriceBase):
    class Config:
        orm_mode = True


# Properties to return to client
class Price(PriceInDBBase):
    pass


# Properties properties stored in DB
class PriceInDB(PriceInDBBase):
    pass
