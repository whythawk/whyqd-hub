from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base import CRUDBase
from app.models import User, OgunUser
from app.schemas import OgunUserCreate, OgunUserUpdate
from app.schema_types import RoleType
from app.core.config import settings
from app.core.security import get_password_hash, verify_password


class CRUDOgunUser(CRUDBase[OgunUser, OgunUserCreate, OgunUserUpdate]):
    def get_by_access_key(self, db: Session, *, access_key: str) -> Optional[OgunUser]:
        return db.query(OgunUser).filter(OgunUser.access_key == access_key).first()

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
        return user.ogun_users.filter(self.model.access_key == access_key).first()

    def authenticate(self, db: Session, *, access_key: str | UUID, password: str) -> Optional[OgunUser]:
        db_obj = self.get_by_access_key(db, access_key=access_key)
        if not db_obj:
            return None
        if not verify_password(plain_password=password, hashed_password=db_obj.secret_key):
            return None
        return db_obj

    def get_multi(
        self, *, user: User, page: int = 0, page_break: bool = False, responsibility: RoleType | None = None
    ) -> list[OgunUser]:
        db_objs = user.ogun_users
        if responsibility:
            db_objs = db_objs.filter(self.model.responsibility == responsibility)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def remove(self, db: Session, *, user: User, access_key: str) -> None:
        db_obj = self.get(user=user, access_key=access_key)
        if not db_obj:
            return None
        db.delete(db_obj)
        db.commit()
        return None


ogun = CRUDOgunUser(OgunUser)
