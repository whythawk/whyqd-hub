from __future__ import annotations
from pydantic import Field
from typing import List, Optional, TYPE_CHECKING

from app.schema_types import SubscriptionType
from app.schemas.base_schema import BaseSchema
from app.schemas.price import Price, PriceUpdate


class ProductBase(BaseSchema):
    id: str = Field(..., description="Stripe product id generated from dashboard.")
    name: str = Field(..., description="Membership name.")
    description: Optional[str] = Field(None, description="Membership description.")
    subscription: SubscriptionType = Field(..., description="Class of membership.")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    prices: Optional[List[PriceUpdate]] = Field(
        [], description="List of prices by currency denomination for this product."
    )


class ProductInDBBase(ProductBase):
    prices: Optional[List[Price]] = Field([], description="List of prices by currency denomination for this product.")

    class Config:
        orm_mode = True


# Properties to return to client
class Product(ProductInDBBase):
    pass


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    pass
