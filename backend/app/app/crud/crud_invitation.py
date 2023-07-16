from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base import CRUDBase
from app.models import Invitation
from app.schemas import InvitationCreate, InvitationUpdate
from app.core.config import settings


class CRUDInvitation(CRUDBase[Invitation, InvitationCreate, InvitationUpdate]):
    def get_multi_by_team(
        self, db: Session, *, page: int = 0, page_break: bool = False, team_id: UUID
    ) -> List[Invitation]:
        db_objs = db.query(self.model).filter(Invitation.team_id == team_id)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def get_multi_by_email(
        self, db: Session, *, page: int = 0, page_break: bool = False, email: str
    ) -> List[Invitation]:
        db_objs = db.query(self.model).filter(Invitation.email == email)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()


invitation = CRUDInvitation(Invitation)
