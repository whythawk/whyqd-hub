from __future__ import annotations
from typing import Optional  # , List
from pydantic import field_validator, ConfigDict, Field

from sqlalchemy.orm import Query

# from sqlalchemy import desc
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema, BaseSummarySchema

# from app.schemas.resource import Resource
from app.schema_types import DCAccrualType, DCFrequencyType, DCAccrualPolicyType, StateType


class TaskBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date reference was last modified.")
    isPrivate: Optional[bool] = Field(
        True, alias="is_private", description="Whether the reference is private to roleplayers."
    )
    name: Optional[str] = Field(None, description="A machine-readable name given to the task.")
    # https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset
    # https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-2
    title: Optional[str] = Field(None, description="A human-readable title given to the task.")
    description: Optional[str] = Field(
        None,
        description="A short description of the task.",
    )
    frequency: Optional[str] = Field(
        None,
        description="An entity responsible for making contributions to the task.",
    )
    spatial: Optional[str] = Field(
        None,
        description="Spatial characteristics of the task.",
    )
    temporalStart: Optional[datetime] = Field(
        None,
        description="Temporal start of the task.",
    )
    temporalEnd: Optional[datetime] = Field(
        None,
        description="Temporal end of the task.",
    )
    language: Optional[str] = Field(
        None,
        description="Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    creator: Optional[str] = Field(
        None,
        description="An entity primarily responsible for making the task.",
    )
    contributor: Optional[str] = Field(
        None,
        description="An entity responsible for making contributions to the task.",
    )
    publisher: Optional[str] = Field(
        None,
        description="An entity responsible for making the resource available.",
    )
    rights: Optional[str] = Field(
        None,
        description="Information about rights held in and over the task.",
    )
    source: Optional[str] = Field(
        None,
        description="A related resource from which the described resource is derived.",
    )
    accessRights: Optional[str] = Field(
        None,
        description="Information about who may access the resource or an indication of its security status.",
    )
    accrualMethod: Optional[DCAccrualType] = Field(
        None, description="The method by which items are added to a resource."
    )
    accrualPeriodicity: Optional[DCFrequencyType] = Field(
        None, description="The frequency with which items are added to a resource."
    )
    accrualPriority: Optional[int] = Field(
        None,
        description="An accrual priority. The higher the integer, the higher the priority.",
    )
    accrualPolicy: Optional[DCAccrualPolicyType] = Field(
        None, description="The policy governing the addition of items to a resource."
    )
    bibliographicCitation: Optional[str] = Field(
        None,
        description="A bibliographic reference for the task.",
    )
    conformsTo: Optional[str] = Field(
        None,
        description="An established standard to which the described resource conforms.",
    )


class TaskCreate(TaskBase):
    name: str = Field(..., description="A machine-readable name given to the task.")
    datasource_id: Optional[UUID] = Field(None, description="Source data template model reference.")
    crosswalk_id: Optional[UUID] = Field(None, description="Crosswalk template model reference.")
    schema_id: Optional[UUID] = Field(None, description="Schema model reference.")
    project_id: Optional[UUID] = Field(None, description="Project task relationship reference.")


class TaskUpdate(TaskCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the task.")
    model_config = ConfigDict(from_attributes=True)


class Task(TaskBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    name: str = Field(..., description="A machine-readable name given to the task.")
    datasource: Optional[BaseSummarySchema] = Field(
        None, alias="datasource", description="Template for source data definition."
    )
    crosswalk: Optional[BaseSummarySchema] = Field(
        None, alias="crosswalk", description="Template for crosswalk definition."
    )
    skhema: Optional[BaseSummarySchema] = Field(None, alias="schema", description="Schema summary.")
    project: Optional[BaseSummarySchema] = Field(None, description="Project summary.")
    resources: Optional[int] = Field(None, description="Count of incomplete resources.")
    model_config = ConfigDict(from_attributes=True)

    @field_validator("resources", mode="before")
    @classmethod
    def evaluate_lazy_resources(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.model_validate(dbQuery)
        if isinstance(v, Query):
            return v.filter("state" != StateType.COMPLETE.value).count()
        return None


class ScheduledTask(TaskBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    name: str = Field(..., description="A machine-readable name given to the task.")
    last_completed: Optional[datetime] = Field(None, alias="lastCompleted", description="Last completed resource date.")
    latest_resource: Optional[BaseSummarySchema] = Field(None, alias="latestResource", description="Latest resource.")
    resources: Optional[int] = Field(None, description="Count of incomplete resources.")
    skhema: Optional[BaseSummarySchema] = Field(None, alias="schema", description="Schema summary.")
    project: Optional[BaseSummarySchema] = Field(None, description="Project summary.")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_validator("resources", mode="before")
    @classmethod
    def evaluate_lazy_resources(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.model_validate(dbQuery)
        if isinstance(v, Query):
            return v.filter("state" != StateType.COMPLETE.value).count()
        return None
