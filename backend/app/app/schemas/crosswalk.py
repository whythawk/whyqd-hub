from __future__ import annotations
from typing import Optional, Union, List, Tuple
from pydantic import ConfigDict, Field
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema
from app.schemas.reference import Reference
from app.schemas.schema import Schema


class CrosswalkBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date reference was last modified.")
    isPrivate: Optional[bool] = Field(
        True, alias="is_private", description="Whether the reference is private to roleplayers."
    )
    name: Optional[str] = Field(None, description="A machine-readable name given to the crosswalk.")
    title: Optional[str] = Field(None, description="A human-readable title given to the crosswalk.")
    description: Optional[str] = Field(
        None,
        description="A short description of the crosswalk.",
    )
    version: Optional[datetime] = Field(None, description="Version date reference model file was created.")
    reference: Optional[Reference] = Field(None, description="Reference model of schema definition.")
    subject: Optional[Schema] = Field(None, description="Subject schema definition for source of crosswalk.")
    object: Optional[Schema] = Field(None, description="Object schema definition for destination of crosswalk.")


class CrosswalkCreate(CrosswalkBase):
    reference_id: UUID = Field(..., description="Crosswalk reference model reference.")
    subject_id: UUID = Field(..., description="Schema subject model reference.")
    object_id: UUID = Field(..., description="Schema object model reference.")


class CrosswalkUpdate(CrosswalkCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")


class Crosswalk(CrosswalkBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    name: str = Field(..., description="A machine-readable name given to the crosswalk.")
    reference: Reference = Field(..., description="Reference model of schema definition.")
    subject: Schema = Field(..., description="Subject schema definition for source of crosswalk.")
    object: Schema = Field(..., description="Object schema definition for destination of crosswalk.")
    model_config = ConfigDict(from_attributes=True)


class ActionModel(BaseSchema):
    uuid: str = Field(..., description="Copied from original reference as a string.")
    action: str = Field(..., description="Action term for the script")
    destinationField: Optional[Union[str, List[str]]] = Field(
        None, description="Destination field names as list, or single term."
    )
    destinationTerm: Optional[Union[bool, str]] = Field(None, description="Destination category term.")
    sourceField: Optional[Union[str, List[Tuple[str, str]], List[Tuple[str, str, str]], List[str]]] = Field(
        None, description="Source field names as list, or structured list of lists."
    )
    sourceTerm: Optional[Union[str, List[str]]] = Field(None, description="Source term names as list, or single term.")
    rows: Optional[List[int]] = Field(None, description="Source row list of row-numbers, base zero.")
