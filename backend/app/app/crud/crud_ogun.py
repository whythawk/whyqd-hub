from __future__ import annotations
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import User, OgunUser
from app.schemas import OgunUserCreate, OgunUserUpdate
from app.schema_types import RoleType
from app.core.config import settings
from app.core.security import get_password_hash


class CRUDOgunUser(CRUDBase[OgunUser, OgunUserCreate, OgunUserUpdate]):
    def create(self, db: Session, *, obj_in: OgunUserCreate) -> OgunUser:
        db_obj = OgunUser(
            authorises_id=obj_in.authorises_id,
            responsibility=obj_in.responsibility,
            access_key=obj_in.access_key,
            secret_key=get_password_hash(obj_in.secret_key),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: OgunUser) -> OgunUser:
        return db_obj

    def get(self, *, user: User, access_key: str) -> OgunUser:
        return user.ogun_tokens.filter(self.model.access_key == access_key).first()

    def get_multi(
        self, *, user: User, skip: int = 0, limit: int = None, responsibility: RoleType | None = None
    ) -> list[OgunUser]:
        db_objs = user.ogun_users
        if responsibility:
            db_objs = db_objs.filter(self.model.responsibility == responsibility)
        if skip:
            db_objs = db_objs.offset(skip)
        if limit and (limit <= settings.MULTI_MAX):
            db_objs = db_objs.limit(limit)
        return db_objs.all()

    def remove(self, db: Session, *, db_obj: OgunUser) -> None:
        db.delete(db_obj)
        db.commit()
        return None


ogun = CRUDOgunUser(OgunUser)
