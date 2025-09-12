from __future__ import annotations
from pydantic import ConfigDict, Field
from typing import List, Optional

from app.schema_types import SubscriptionType, CurrencyType
from app.schemas.base_schema import BaseSchema
from app.schemas.price import Price, PriceUpdate


class ProductBase(BaseSchema):
    id: str = Field(..., description="Stripe product id generated from dashboard.")
    name: str = Field(..., description="Membership name.")
    description: Optional[str] = Field(None, description="Membership description.")
    subscription: SubscriptionType = Field(..., description="Class of membership.")
    rows: int = Field(default=0, description="Row-count limit for performing transforms.")
    transforms: int = Field(default=0, description="Transform limit per month.")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    prices: Optional[List[PriceUpdate]] = Field(
        [], description="List of prices by currency denomination for this product."
    )


class ProductInDBBase(ProductBase):
    prices: Optional[List[Price]] = Field([], description="List of prices by currency denomination for this product.")
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class Product(ProductInDBBase):
    pass


# Properties properties stored in DB
class ProductInDB(ProductInDBBase):
    pass


class ProductPricingView(BaseSchema):
    id: str = Field(..., description="Stripe product id generated from dashboard.")
    name: str = Field(..., description="Membership name.")
    description: Optional[str] = Field(None, description="Membership description.")
    subscription: SubscriptionType = Field(..., description="Class of membership.")
    rows: int = Field(..., description="Row-count limit for performing transforms.")
    transforms: int = Field(..., description="Transform limit per month.")
    currency: CurrencyType = Field(default=CurrencyType.EUR, description="Currency for the fee.")
    per_month: Optional[Price] = Field(None, description="Monthly by currency denomination for this product.")
    per_annum: Optional[Price] = Field(None, description="Annually by currency denomination for this product.")
    model_config = ConfigDict(from_attributes=True)
