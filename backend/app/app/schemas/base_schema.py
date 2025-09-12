from __future__ import annotations
from pydantic import ConfigDict, BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.schema_types import StateType


class BaseSchema(BaseModel):
    @property
    def as_db_dict(self):
        to_db = self.dict(exclude_defaults=True, exclude_none=True, exclude={"identifier, id"})
        for key in ["id", "identifier"]:
            if key in self.dict().keys():
                to_db[key] = self.dict()[key].hex
        return to_db


class BaseSummarySchema(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date last modified.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date last modified.")
    isPrivate: Optional[bool] = Field(True, alias="is_private", description="Whether private to roleplayers.")
    name: Optional[str] = Field(None, description="A machine-readable namek.")
    title: Optional[str] = Field(None, description="A human-readable title.")
    description: Optional[str] = Field(
        None,
        description="A short description.",
    )
    state: Optional[StateType] = Field(None, description="Resource work state.")
    model_config = ConfigDict(from_attributes=True)


class MetadataBaseSchema(BaseSchema):
    # Receive via API
    # https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-3
    title: Optional[str] = Field(None, description="A human-readable title given to the resource.")
    description: Optional[str] = Field(
        None,
        description="A short description of the resource.",
    )
    isActive: Optional[bool] = Field(default=True, description="Whether the resource is still actively maintained.")
    isPrivate: Optional[bool] = Field(
        default=True, description="Whether the resource is private to team members with appropriate authorisation."
    )


class MetadataBaseCreate(MetadataBaseSchema):
    pass


class MetadataBaseUpdate(MetadataBaseSchema):
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class MetadataBaseInDBBase(MetadataBaseSchema):
    # Identifier managed programmatically
    identifier: UUID = Field(..., description="Automatically generated unique identity for the resource.")
    created: datetime = Field(..., description="Automatically generated date resource was created.")
    isActive: bool = Field(..., description="Whether the resource is still actively maintained.")
    isPrivate: bool = Field(
        ..., description="Whether the resource is private to team members with appropriate authorisation."
    )
    model_config = ConfigDict(from_attributes=True)
