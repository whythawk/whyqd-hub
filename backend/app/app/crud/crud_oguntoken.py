from __future__ import annotations
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import User, OgunToken
from app.schemas import OgunTokenCreate, OgunTokenUpdate
from app.schema_types import RoleType
from app.core.config import settings


class CRUDOgunToken(CRUDBase[OgunToken, OgunTokenCreate, OgunTokenUpdate]):
    # Everything is user-dependent
    def create(
        self, db: Session, *, obj_in: str, user_obj: User, responsibility: RoleType = RoleType.SEEKER
    ) -> OgunToken:
        db_obj = db.query(self.model).filter(self.model.token == obj_in).first()
        if db_obj and db_obj.authenticates != user_obj:
            raise ValueError("Token mismatch between key and user.")
        obj_in = OgunTokenCreate(**{"token": obj_in, "authenticates_id": user_obj.id, "responsibility": responsibility})
        return super().create(db=db, obj_in=obj_in)

    def get(self, *, user: User, token: str) -> OgunToken:
        return user.ogun_tokens.filter(self.model.token == token).first()

    def get_responsibility(self, *, user: User, token: str) -> RoleType:
        db_obj = self.get(token=token, user=user)
        return db_obj.responsibility

    def get_multi(self, *, user: User, page: int = 0, page_break: bool = False) -> list[OgunToken]:
        db_objs = user.ogun_tokens
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def remove(self, db: Session, *, db_obj: OgunToken) -> None:
        db.delete(db_obj)
        db.commit()
        return None


oguntoken = CRUDOgunToken(OgunToken)
