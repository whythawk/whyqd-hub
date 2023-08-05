from __future__ import annotations
from pydantic import Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema


class TransformActivityBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity for the fee.")
    rows: int = Field(default=0, description="Row-count limit for performing transforms.")
    data_import: bool = Field(
        default=True, description="Transform activities documented on data import, and transformation."
    )
    researcher_id: UUID = Field(..., description="Researcher model reference.")


class TransformActivityCreate(TransformActivityBase):
    pass


class TransformActivityUpdate(TransformActivityBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the fee.")


class TransformActivityInDBBase(TransformActivityUpdate):
    created: datetime = Field(..., description="Automatically generated datetime of creation.")

    class Config:
        orm_mode = True


# Properties to return to client
class TransformActivity(TransformActivityInDBBase):
    pass
