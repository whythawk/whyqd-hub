from __future__ import annotations
from typing import Optional, List
from pydantic import field_validator, ConfigDict, Field

from sqlalchemy.orm import Query

# from sqlalchemy import desc
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema, BaseSummarySchema
from app.schemas.role import RoleSummary

# from app.schemas.task import Task
from app.schema_types import DCAccrualType, DCFrequencyType, DCAccrualPolicyType


class ProjectBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    modified: Optional[datetime] = Field(None, description="Automatically generated date reference was last modified.")
    isPrivate: Optional[bool] = Field(
        True, alias="is_private", description="Whether the reference is private to roleplayers."
    )
    name: Optional[str] = Field(None, description="A machine-readable name given to the project.")
    # https://www.w3.org/TR/vocab-dcat-3/#Class:Dataset
    # https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#section-2
    title: Optional[str] = Field(None, description="A human-readable title given to the project.")
    description: Optional[str] = Field(
        None,
        description="A short description of the project.",
    )
    subjects: Optional[List[str]] = Field(
        [],
        description="A list of topics of the project.",
    )
    frequency: Optional[str] = Field(
        None,
        description="The temporal frequency of update of the project.",
    )
    spatial: Optional[str] = Field(
        None,
        description="Spatial characteristics of the project.",
    )
    temporalStart: Optional[datetime] = Field(
        None,
        description="Temporal start of the project.",
    )
    temporalEnd: Optional[datetime] = Field(
        None,
        description="Temporal end of the project.",
    )
    language: Optional[str] = Field(
        None,
        description="Specify the language of the creative work. Controlled vocabulary defined by ISO 639-1, ISO 639-2 or ISO 639-3.",
    )
    creator: Optional[str] = Field(
        None,
        description="An entity primarily responsible for making the project.",
    )
    contributor: Optional[str] = Field(
        None,
        description="An entity responsible for making contributions to the project.",
    )
    publisher: Optional[str] = Field(
        None,
        description="An entity responsible for making the resource available.",
    )
    rights: Optional[str] = Field(
        None,
        description="Information about rights held in and over the project.",
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
    accrualPolicy: Optional[DCAccrualPolicyType] = Field(
        None, description="The policy governing the addition of items to a resource."
    )
    bibliographicCitation: Optional[str] = Field(
        None,
        description="A bibliographic reference for the project.",
    )
    conformsTo: Optional[str] = Field(
        None,
        description="An established standard to which the described resource conforms.",
    )
    model_config = ConfigDict(from_attributes=True)

    @field_validator("subjects", mode="before")
    @classmethod
    def evaluate_subjects(cls, v):
        return [s for s in v]


class ProjectCreate(ProjectBase):
    name: str = Field(..., description="A machine-readable name given to the project.")
    schema_id: Optional[UUID] = Field(None, description="Schema model reference.")


class ProjectUpdate(ProjectCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    name: Optional[str] = Field(None, description="A machine-readable name given to the project.")


class Project(ProjectBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    modified: datetime = Field(..., description="Automatically generated date reference was last modified.")
    name: str = Field(..., description="A machine-readable name given to the project.")
    skhema: Optional[BaseSummarySchema] = Field(None, alias="schema", description="Schema summary.")
    # tasks: Optional[List[Task]] = Field(None, description="List of tasks for this project.")
    auths: List[RoleSummary] = Field(..., description="Project members.")
    model_config = ConfigDict(from_attributes=True)

    # @validator("tasks", pre=True)
    # def evaluate_lazy_tasks(cls, v):
    #     # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
    #     # Call PydanticModel.model_validate(dbQuery)
    #     if isinstance(v, Query):
    #         return v.order_by(desc("name")).all()
    #     return v

    @field_validator("auths", mode="before")
    @classmethod
    def evaluate_lazy_auths(cls, v):
        # https://github.com/samuelcolvin/pydantic/issues/1334#issuecomment-745434257
        # Call PydanticModel.model_validate(dbQuery)
        if isinstance(v, Query):
            return v.all()
