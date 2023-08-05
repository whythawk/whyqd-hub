from __future__ import annotations
from pydantic import Field, constr
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema
from app.schema_types import SubscriptionType, SubscriptionEventType, CurrencyType


class OrderBase(BaseSchema):
    subscription_event_type: SubscriptionEventType = Field(
        default=SubscriptionEventType.PENDING, description="Event process status."
    )
    subscription_type: SubscriptionType = Field(..., description="Class of membership.")
    currency: CurrencyType = Field(..., description="Currency of subscription fee.")
    amount: int = Field(..., description="Currency value of subscription fee.")
    checkout_id: Optional[str] = Field(None, description="Stripe checkout session id.")
    subscription_id: Optional[str] = Field(None, description="Stripe subscription id.")
    charge_id: Optional[str] = Field(None, description="Stripe charge id.")
    invoice_url: Optional[str] = Field(None, description="Stripe customer invoice url.")
    country_code: Optional[constr(max_length=3)] = Field(
        None, description="ISO two/three-letter country code, if possible."
    )
    country_name: Optional[str] = Field(None, description="Country name, if possible.")
    product_id: str = Field(..., description="Stripe product id.")
    price_id: str = Field(..., description="Stripe price / currency id.")
    payer_id: UUID = Field(..., description="Payer member id.")


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the fee.")


class OrderInDBBase(OrderUpdate):
    created: datetime = Field(..., description="Automatically generated datetime of creation.")

    class Config:
        orm_mode = True


# Properties to return to client
class Order(OrderInDBBase):
    pass


# Properties properties stored in DB
class OrderInDB(OrderInDBBase):
    pass


class OrderInView(BaseSchema):
    id: UUID = Field(..., description="Automatically generated unique identity for the fee.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    subscription_event_type: SubscriptionEventType = Field(
        default=SubscriptionEventType.PENDING, description="Event process status."
    )
    country_code: Optional[constr(max_length=3)] = Field(
        None, description="ISO two/three-letter country code, if possible."
    )
    country_name: Optional[str] = Field(None, description="Country name, if possible.")
    subscription_type: SubscriptionType = Field(..., description="Class of membership.")
    currency: CurrencyType = Field(..., description="Currency of subscription fee.")
    amount: int = Field(..., description="Currency value of subscription fee.")
    invoice_url: Optional[str] = Field(None, description="Stripe customer invoice url.")

    class Config:
        orm_mode = True
