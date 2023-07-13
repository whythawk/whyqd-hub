from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base import CRUDBase
from app.models import Invitation
from app.schemas import InvitationCreate, InvitationUpdate


class CRUDInvitation(CRUDBase[Invitation, InvitationCreate, InvitationUpdate]):
    def get_multi_by_team(self, db: Session, *, skip: int = 0, limit: int = 100, team_id: UUID) -> List[Invitation]:
        return db.query(self.model).filter(Invitation.team_id == team_id).offset(skip).limit(limit).all()

    def get_multi_by_email(self, db: Session, *, skip: int = 0, limit: int = 100, email: str) -> List[Invitation]:
        return db.query(self.model).filter(Invitation.email == email).offset(skip).limit(limit).all()


invitation = CRUDInvitation(Invitation)
