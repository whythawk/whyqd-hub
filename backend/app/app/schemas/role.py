from __future__ import annotations
from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema, BaseSummarySchema
from app.schemas.user import UserSummary
from app.schema_types import RoleType


class RoleBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    researcher_id: UUID = Field(
        ...,
        description="Specified researcher with responsibility.",
    )
    responsibility: RoleType = Field(
        default=RoleType.SEEKER,
        description="Responsibility assigned to this researcher.",
    )
    is_validated: Optional[bool] = Field(
        False,
        description="Any assigned role must be accepted by the user.",
    )
    project_id: Optional[UUID] = Field(
        None,
        description="Unique identity for the referenced resource.",
    )
    task_id: Optional[UUID] = Field(
        None,
        description="Unique identity for the referenced resource.",
    )
    resource_id: Optional[UUID] = Field(
        None,
        description="Unique identity for the referenced resource.",
    )
    reference_id: Optional[UUID] = Field(
        None,
        description="Unique identity for the referenced resource.",
    )
    referencetemplate_id: Optional[UUID] = Field(
        None,
        description="Unique identity for the referenced resource.",
    )

    class Config:
        orm_mode = True


class RoleCreate(RoleBase):
    pass


class RoleUpdate(RoleBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the resource.")


class Role(BaseSchema):
    id: UUID = Field(..., description="Automatically generated unique identity for the invitation.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    researcher: UserSummary = Field(..., description="Specified researcher with responsibility.")
    project: Optional[BaseSummarySchema] = Field(None, description="Project summary.")
    task: Optional[BaseSummarySchema] = Field(None, description="Task summary.")
    resource: Optional[BaseSummarySchema] = Field(None, description="Resource summary.")
    reference: Optional[BaseSummarySchema] = Field(None, alias="schema", description="Reference summary.")
    referencetemplate: Optional[BaseSummarySchema] = Field(None, description="Reference template summary.")

    class Config:
        orm_mode = True
