from __future__ import annotations
from typing import Optional
from pydantic import Field
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema, BaseSummarySchema
from app.schemas.user import UserSummary


class ActivityBase(BaseSchema):
    id: Optional[UUID] = Field(None, description="Automatically generated unique identity.")
    created: Optional[datetime] = Field(None, description="Automatically generated date reference was created.")
    custodiansOnly: Optional[bool] = Field(
        default=False,
        alias="custodians_only",
        description="Activity view reserved for team custodians only.",
    )
    alert: Optional[bool] = Field(
        default=False,
        description="Pending alert on this activity.",
    )
    message: Optional[str] = Field(None, description="Brief phrase describing the activity.")


class ActivityCreate(ActivityBase):
    researcher_id: Optional[UUID] = Field(None, description="Researcher model reference.")
    resource_id: Optional[UUID] = Field(None, description="Resource model reference.")
    task_id: Optional[UUID] = Field(None, description="Task model reference.")
    project_id: Optional[UUID] = Field(None, description="Project model reference.")


class ActivityUpdate(ActivityCreate):
    id: UUID = Field(..., description="Automatically generated unique identity.")


class Activity(ActivityBase):
    id: UUID = Field(..., description="Automatically generated unique identity.")
    created: datetime = Field(..., description="Automatically generated date reference was created.")
    message: str = Field(..., description="Brief phrase describing the activity.")
    researcher: Optional[UserSummary] = Field(None, description="Researcher who did the thing.")
    resource: Optional[BaseSummarySchema] = Field(None, description="Summary of an associated resource.")
    task: Optional[BaseSummarySchema] = Field(None, description="Summary of an associated task.")
    project: Optional[BaseSummarySchema] = Field(None, description="Summary of an associated project.")

    class Config:
        orm_mode = True
