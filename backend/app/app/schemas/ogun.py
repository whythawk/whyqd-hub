from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from passlib import pwd
from datetime import datetime

from app.schema_types import RoleType


def generate_phrase():
    return pwd.genphrase(entropy=56, sep="-")


class OgunUserBase(BaseModel):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    authorises_id: Optional[UUID] = None
    responsibility: RoleType = Field(
        default=RoleType.SEEKER,
        description="Responsibility assigned to this ogun.",
    )


class OgunUserCreate(OgunUserBase):
    access_key: UUID = Field(default_factory=uuid4, description="Automatically generated access key.")
    secret_key: str = Field(
        default_factory=generate_phrase, description="Automatically generated secret key. Will be hashed."
    )
    authorises_id: UUID


class OgunUserUpdate(OgunUserCreate):
    secret_key: str = Field(..., description="Hashed secret key.")


class OgunUser(OgunUserBase):
    class Config:
        orm_mode = True
