from __future__ import annotations
from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.schema_types import ReferenceType, MimeType
from app.schemas.base_schema import BaseSchema


class ReferenceTemplateBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    isPrivate: Optional[bool] = Field(
        True, alias="is_private", description="Whether the reference is private to roleplayers."
    )
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
    # OF DATA SOURCE MIME TYPE
    mimeType: Optional[MimeType] = Field(
        None, alias="mime_type", description="Reference to model type of the source model file."
    )


class ReferenceTemplateCreate(ReferenceTemplateBase):
    name: str = Field(..., description="A machine-readable name given to the reference.")

    class Config:
        allow_population_by_field_name = True


class ReferenceTemplateUpdate(ReferenceTemplateCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class ReferenceTemplate(ReferenceTemplateBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")

    class Config:
        orm_mode = True
