from __future__ import annotations
from typing import Optional
from pydantic import Field, EmailStr
from uuid import UUID
from datetime import datetime

from app.schema_types import InvitationResponseType
from app.schemas.base_schema import BaseSchema, BaseSummarySchema
from app.schemas.user import UserSummary


class InvitationBase(BaseSchema):
    fullName: Optional[str] = Field(None, alias="full_name", description="Name of invited project member.")
    email: Optional[EmailStr] = Field(None, description="Email of invited project member.")
    response: InvitationResponseType = Field(
        default=InvitationResponseType.WAITING, description="Invitee current response."
    )


class InvitationCreate(InvitationBase):
    sender_id: Optional[UUID] = Field(None, description="Project custodian responsible for the invitation.")
    project_id: Optional[UUID] = Field(None, description="Invitation project identity.")


class InvitationUpdate(InvitationBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the invitation.")
    response: InvitationResponseType = Field(..., description="Invitee current response.")


class Invitation(InvitationBase):
    id: UUID = Field(..., description="Automatically generated unique identity for the invitation.")
    created: datetime = Field(..., description="Automatically generated datetime of creation.")
    sender: UserSummary = Field(..., description="Project custodian responsible for the invitation.")
    project: BaseSummarySchema = Field(..., description="Invitation project summary.")
    response: InvitationResponseType = Field(
        default=InvitationResponseType.WAITING, description="Invitee current response."
    )

    class Config:
        orm_mode = True
