from __future__ import annotations
from pydantic import Field, EmailStr, validator
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.models import User
from app.schema_types import SubscriptionType, SubscriptionEventType
from app.schemas.base_schema import BaseSchema


class SubscriptionBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity for the fee.")
    subscription_id: Optional[str] = Field(None, description="Stripe payment intent id.")
    subscription_event_type: SubscriptionEventType = Field(
        default=SubscriptionEventType.PENDING, description="Event process status."
    )
    subscription_type: SubscriptionType = Field(..., description="Class of membership.")
    started: Optional[datetime] = Field(None, description="Payment date.")
    ends: Optional[datetime] = Field(None, description="End of the subscription period.")
    override: bool = Field(
        default=False, description="Admin-level override to generate free, persistent subscriptions."
    )
    subscriber_id: Optional[UUID] = Field(None, description="Automatically generated unique identity for the fee.")


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(SubscriptionBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the fee.")


class SubscriptionInDBBase(SubscriptionUpdate):
    created: datetime = Field(..., description="Automatically generated datetime of creation.")

    class Config:
        orm_mode = True


# Properties to return to client
class Subscription(SubscriptionInDBBase):
    pass


# Properties properties stored in DB
class SubscriptionInDB(SubscriptionInDBBase):
    pass


class SubscriptionInProfile(BaseSchema):
    membership: SubscriptionType = Field(..., description="Class of membership.")
    ends: Optional[datetime] = Field(None, description="End of the subscription period.")
    override: bool = Field(
        default=False, description="Admin-level override to generate free, persistent subscriptions."
    )


class SubscriptionInView(BaseSchema):
    id: UUID = Field(..., description="Automatically generated unique identity for the fee.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    subscription_event_type: SubscriptionEventType = Field(
        default=SubscriptionEventType.PENDING, description="Event process status."
    )
    subscription_type: SubscriptionType = Field(..., description="Class of membership.")
    ends: Optional[datetime] = Field(None, description="End of the subscription period.")
    override: bool = Field(
        default=False, description="Admin-level override to generate free, persistent subscriptions."
    )
    subscriber: EmailStr = Field(..., description="User email.")

    class Config:
        orm_mode = True

    @validator("subscriber", pre=True)
    def evaluate_lazy_subscriber(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, User):
            return v.email
        return v


class SubscriptionAdminCreate(SubscriptionBase):
    subscription_type: SubscriptionType = Field(..., description="Class of membership.")
    ends: Optional[datetime] = Field(None, description="End of the subscription period.")
    override: bool = Field(
        default=False, description="Admin-level override to generate free, persistent subscriptions."
    )
    subscriber: EmailStr = Field(..., description="User email.")
