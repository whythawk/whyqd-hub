from __future__ import annotations
from typing import Optional
from pydantic import ConfigDict, Field
from uuid import UUID
from datetime import datetime

from app.schema_types import ReferenceType, MimeType
from app.schemas.base_schema import BaseSchema


class ReferenceBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    isPrivate: Optional[bool] = Field(
        True, alias="is_private", description="Whether the reference is private to roleplayers."
    )
    isFeatured: Optional[bool] = Field(False, description="Whether the reference is featured.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the reference.")
    title: Optional[str] = Field(None, description="A human-readable title given to the reference.")
    description: Optional[str] = Field(
        None,
        description="A short description of the reference.",
    )
    model: UUID = Field(..., description="Reference to the source model file.")
    modelType: ReferenceType = Field(
        ..., alias="model_type", description="Reference to model type of the source model file."
    )
    version: Optional[datetime] = Field(None, description="Version date reference model file was created.")
    hash: Optional[str] = Field(None, description="Some unique identifier from the reference model.")
    # OF DATA SOURCE MIME TYPE
    mimeType: Optional[MimeType] = Field(
        None, alias="mime_type", description="Reference to model type of the source model file."
    )
    index: Optional[int] = Field(None, description="Source data index of last row.")


class ReferenceCreate(ReferenceBase):
    name: str = Field(..., description="A machine-readable name given to the reference.")
    model_config = ConfigDict(populate_by_name=True)


class ReferenceUpdate(ReferenceCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class Reference(ReferenceBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    model_config = ConfigDict(from_attributes=True)
