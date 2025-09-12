from typing import Optional
from uuid import UUID
from pydantic import field_validator, StringConstraints, ConfigDict, BaseModel, Field, EmailStr
from sqlalchemy.orm import Query
from sqlalchemy import or_
from datetime import datetime, timedelta


from app.schemas.subscription import SubscriptionInProfile
from app.models.subscription import Subscription as SubscriptionMDL
from app.schema_types import SubscriptionType
from typing_extensions import Annotated


class UserLogin(BaseModel):
    username: str
    password: str


# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    email_validated: Optional[bool] = False
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    full_name: Optional[str] = None


class UserSummary(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserSearch(BaseModel):
    email: EmailStr


# Properties to receive via API on creation
class UserCreate(UserBase):
    email: EmailStr
    password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None


# Properties to receive via API on update
class UserUpdate(UserBase):
    original: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None
    password: Optional[Annotated[str, StringConstraints(min_length=8, max_length=64)]] = None


class UserInDBBase(UserBase):
    id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class User(UserInDBBase):
    hashed_password: bool = Field(default=False, alias="password")
    totp_secret: bool = Field(default=False, alias="totp")
    subscriptions: Optional[SubscriptionInProfile] = None
    model_config = ConfigDict(populate_by_name=True)

    @field_validator("hashed_password", mode="before")
    @classmethod
    def evaluate_hashed_password(cls, hashed_password):
        if hashed_password:
            return True
        return False

    @field_validator("totp_secret", mode="before")
    @classmethod
    def evaluate_totp_secret(cls, totp_secret):
        if totp_secret:
            return True
        return False

    @field_validator("subscriptions", mode="before")
    @classmethod
    def evaluate_lazy_subscriptions(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.from_orm(dbQuery)
        if isinstance(v, Query):
            expires = datetime.utcnow() - timedelta(days=1)  # 1 day grace
            v = (
                v.filter(or_(SubscriptionMDL.ends > expires, SubscriptionMDL.override.is_(True)))
                .order_by(SubscriptionMDL.created.desc())
                .first()
            )
            if v:
                return {"membership": v.subscription_type, "ends": v.ends, "override": v.override}
        return {"membership": SubscriptionType.REVIEWER, "ends": datetime.max, "override": False}


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: Optional[str] = None
    totp_secret: Optional[str] = None
    totp_counter: Optional[int] = None


# class UserProfile(UserInDBBase):
#     subscriptions: SubscriptionInProfile

#     @validator("subscriptions", pre=True)
#     def evaluate_lazy_subscriptions(cls, v):
#         # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
#         # Call PydanticModel.from_orm(dbQuery)
#         if isinstance(v, Query):
#             expires = datetime.utcnow() - timedelta(days=1)  # 1 day grace
#             v = (
#                 v.filter(or_(SubscriptionMDL.ends > expires, SubscriptionMDL.override.is_(True)))
#                 .order_by(SubscriptionMDL.created.desc())
#                 .first()
#             )
#             if v:
#                 return {"membership": v.subscription_type, "ends": v.ends, "override": v.override}
#         return {"membership": SubscriptionType.REVIEWER, "ends": datetime.max, "override": False}


# class UserCustodialProfile(UserInDBBase):
#     subscriptions: Optional[List[Subscription]] = []

#     @validator("subscriptions", pre=True)
#     def evaluate_lazy_subscriptions(cls, v):
#         # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
#         # Call PydanticModel.from_orm(dbQuery)
#         if isinstance(v, Query):
#             return (
#                 v.filter(SubscriptionMDL.subscription_event_type == SubscriptionEventType.RENEWED)
#                 .order_by(desc("ends"))
#                 .all()
#             )
#         return v
