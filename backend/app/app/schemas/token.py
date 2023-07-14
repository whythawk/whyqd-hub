from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from app.schema_types import RoleType


class RefreshTokenBase(BaseModel):
    token: str
    authenticates_id: Optional[UUID] = None


class RefreshTokenCreate(RefreshTokenBase):
    authenticates_id: UUID


class RefreshTokenUpdate(RefreshTokenBase):
    pass


class RefreshToken(RefreshTokenUpdate):
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
    refresh: Optional[bool] = False
    ogun: Optional[bool] = False
    totp: Optional[bool] = False


class MagicTokenPayload(BaseModel):
    sub: Optional[UUID] = None
    fingerprint: Optional[UUID] = None


class WebToken(BaseModel):
    claim: str


class OgunTokenCreate(RefreshTokenBase):
    created: Optional[datetime] = Field(None, description="Automatically generated date ogun token was created.")
    authenticates_id: UUID
    responsibility: RoleType = Field(
        default=RoleType.SEEKER,
        description="Responsibility assigned to this ogun.",
    )


class OgunTokenUpdate(OgunTokenCreate):
    pass


class OgunToken(BaseModel):
    created: datetime = Field(..., description="Automatically generated date ogun token was created.")
    token: str
    responsibility: RoleType = Field(
        default=RoleType.SEEKER,
        description="Responsibility assigned to this ogun.",
    )

    class Config:
        orm_mode = True
