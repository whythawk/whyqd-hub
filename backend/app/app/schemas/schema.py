from __future__ import annotations
from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema
from app.schemas.reference import Reference


class SchemaBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date reference was last modified.")
    isPrivate: Optional[bool] = Field(
        True, alias="is_private", description="Whether the reference is private to roleplayers."
    )
    name: Optional[str] = Field(None, description="A machine-readable name given to the schema.")
    title: Optional[str] = Field(None, description="A human-readable title given to the schema.")
    description: Optional[str] = Field(
        None,
        description="A short description of the schema.",
    )
    version: Optional[datetime] = Field(None, description="Version date reference model file was created.")
    reference: Optional[Reference] = Field(None, description="Reference model of schema definition.")


class SchemaCreate(SchemaBase):
    reference_id: UUID = Field(..., description="Schema reference model reference.")


class SchemaUpdate(SchemaCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")


class Schema(SchemaBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    name: str = Field(..., description="A machine-readable name given to the schema.")
    reference: Reference = Field(..., description="Reference model of schema definition.")

    class Config:
        orm_mode = True
