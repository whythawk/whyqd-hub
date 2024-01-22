from __future__ import annotations
from typing import Optional, List
from pydantic import Field
from uuid import UUID
from datetime import datetime
from whyqd.models import FieldModel, DataSourceAttributeModel

from app.schemas.base_schema import BaseSchema, BaseSummarySchema
from app.schemas.crosswalk import ActionModel
from app.schemas.activity import ResourceActivity
from app.schema_types import StateType, ReferenceType, MimeType


class ResourceBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date reference was last modified.")
    isPrivate: Optional[bool] = Field(
        True, alias="is_private", description="Whether the reference is private to roleplayers."
    )
    name: Optional[str] = Field(None, description="A machine-readable name given to the resource.")
    title: Optional[str] = Field(None, description="A human-readable title given to the resource.")
    description: Optional[str] = Field(
        None,
        description="A short description of the resource.",
    )
    sourceURL: Optional[str] = Field(
        None,
        description="A related URL from which the described source data is imported.",
    )
    state: Optional[StateType] = Field(default=StateType.READY, description="Resource work state.")


class ResourceCreate(ResourceBase):
    datasource_id: Optional[UUID] = Field(None, description="Source data model reference.")
    data_id: Optional[UUID] = Field(None, description="Data model reference.")
    schema_subject_id: Optional[UUID] = Field(None, description="Schema subject model reference.")
    crosswalk_id: Optional[UUID] = Field(None, description="Crosswalk model reference.")
    schema_object_id: Optional[UUID] = Field(None, description="Schema object model reference.")
    transform_id: Optional[UUID] = Field(None, description="Transform model reference.")
    transformdata_id: Optional[UUID] = Field(None, description="Transform data model reference.")
    transformdatasource_id: Optional[UUID] = Field(None, description="Transform data model reference.")
    task_id: Optional[UUID] = Field(None, description="Task model reference.")


class ResourceUpdate(ResourceCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")

    class Config:
        orm_mode = True


class Resource(ResourceBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    # datasource: Optional[BaseSummarySchema] = Field(None, description="Source data table reference.")
    data: Optional[BaseSummarySchema] = Field(None, description="Data table reference.")
    schema_subject: Optional[BaseSummarySchema] = Field(None, description="Schema subject table reference.")
    crosswalk: Optional[BaseSummarySchema] = Field(None, description="Crosswalk table reference.")
    schema_object: Optional[BaseSummarySchema] = Field(None, description="Schema object table reference.")
    transform: Optional[BaseSummarySchema] = Field(None, description="Transform table reference.")
    transformdata: Optional[BaseSummarySchema] = Field(None, description="Transform data table reference.")
    # transformdatasource: Optional[Reference] = Field(None, description="Transform source data table reference.")
    task: Optional[BaseSummarySchema] = Field(None, description="Associated task table reference.")

    class Config:
        orm_mode = True


class ResourceActivitySummary(ResourceBase):
    task_id: Optional[UUID] = Field(None, description="Task model reference.")
    project_id: Optional[UUID] = Field(None, description="Project model reference.")
    latest_activity: ResourceActivity = Field(..., description="Summary of latest activity")

    class Config:
        orm_mode = True


########################################################################################################################
# RESOURCE MANAGER
########################################################################################################################
class ResourceModelLinks(BaseSchema):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    modelType: ReferenceType = Field(
        ..., alias="model_type", description="Reference to model type of the source model file."
    )


class ResourceReference(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was last modified.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the reference.")
    title: Optional[str] = Field(None, description="A human-readable title given to the reference.")
    description: Optional[str] = Field(
        None,
        description="A short description.",
    )
    links: Optional[List[ResourceModelLinks]] = Field([], description="List of model references informing this field.")

    class Config:
        orm_mode = True


class ResourceDataReference(ResourceReference):
    sheet_name: Optional[str] = Field(
        None,
        description="Needed if MimeType is either of XLS or XLSX, and the data consists of multiple sheets.",
    )
    mimeType: Optional[MimeType] = Field(None, alias="mime_type", description="Reference to data mime type.")
    index: Optional[int] = Field(None, description="Index of last row.")
    summarykeys: Optional[List[str]] = Field([], description="Keys for first fifty rows of data source.")
    summary: Optional[List[DataSourceAttributeModel]] = Field([], description="First fifty rows of data source.")


class ResourceSchemaReference(ResourceReference):
    isFeatured: Optional[bool] = Field(False, description="Schema is a featured destination / object.")
    fields: List[FieldModel] = Field(
        default=[],
        description="A list of fields which define the schema. Fields, similarly, contain `name`, `title` and `description`, as well as `type` as compulsory.",
    )


class ResourceCrosswalkReference(ResourceReference):
    actions: List[ActionModel] = Field(
        default=[],
        description="A list of actions which define the crosswalk.",
    )


class ResourceManager(ResourceBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    data: Optional[ResourceDataReference] = Field(None, description="Data table reference.")
    schema_subject: Optional[ResourceSchemaReference] = Field(None, description="Schema subject table reference.")
    crosswalk: Optional[BaseSummarySchema] = Field(None, description="Crosswalk table reference.")
    schema_object: Optional[BaseSummarySchema] = Field(None, description="Schema object table reference.")
    transform: Optional[BaseSummarySchema] = Field(None, description="Transform table reference.")
    transformdata: Optional[ResourceDataReference] = Field(None, description="Transform data table reference.")
    task: Optional[BaseSummarySchema] = Field(None, description="Associated task table reference.")

    class Config:
        orm_mode = True


class ResourceCrosswalkManager(ResourceBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    data: Optional[ResourceDataReference] = Field(None, description="Data table reference.")
    schema_subject: Optional[ResourceSchemaReference] = Field(None, description="Schema subject table reference.")
    crosswalk: Optional[ResourceCrosswalkReference] = Field(None, description="Crosswalk table reference.")
    schema_object: Optional[ResourceSchemaReference] = Field(None, description="Schema object table reference.")
    task: Optional[BaseSummarySchema] = Field(None, description="Associated task table reference.")

    class Config:
        orm_mode = True
