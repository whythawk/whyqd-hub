from __future__ import annotations
from typing import TYPE_CHECKING

# from fastapi.encoders import jsonable_encoder
# from pydantic import parse_obj_as
from sqlalchemy.orm import Session

# from sqlalchemy import desc, and_, or_
from uuid import UUID

# from copy import deepcopy

from app.crud.whyqd_base import CRUDWhyqdBase

# from app.crud.crud_role import role
from app.models.project import Project
from app.schemas import ProjectCreate, ProjectUpdate  # , ResearchResources, RolesCreate
from app.schema_types import RoleType

# from app.schema_types import RoleType
from app.crud.crud_activity import activity as crud_activity

# from app.schema_types import ReferenceType, ResearcherRoleType

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User
    from app.models.reference import Reference


class CRUDProject(CRUDWhyqdBase[Project, ProjectCreate, ProjectUpdate]):
    def create(self, db: Session, *, obj_in: ProjectCreate, user: User) -> Project:
        db_obj = super().create(db=db, obj_in=obj_in, user=user)
        # https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html
        for subject in obj_in.subjects:
            if subject.lower() not in db_obj.subjects:
                db_obj.subjects.append(subject.lower())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        id: UUID | str,
        obj_in: ProjectCreate,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Project:
        db_obj = super().update(db=db, id=id, obj_in=obj_in, user=user, responsibility=responsibility)
        # https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html
        db_obj.subjects = []
        for subject in obj_in.subjects:
            if subject.lower() not in db_obj.subjects:
                db_obj.subjects.append(subject.lower())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_task(self, db: Session, *, db_obj: Project, task_obj: Task) -> Project | None:
        db_obj.tasks.append(task_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_task(self, db: Session, *, db_obj: Project, task_obj: Task) -> Project | None:
        db_obj.tasks.remove(task_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_schema(
        self,
        db: Session,
        *,
        db_obj: Project,
        schema_obj: Reference,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Project | None:
        obj_in = ProjectUpdate.from_orm(db_obj)
        obj_in.schema_id = schema_obj.id
        return self.update(db=db, id=db_obj.id, obj_in=obj_in, user=user, responsibility=responsibility)

    def remove_schema(
        self,
        db: Session,
        *,
        db_obj: Project,
    ) -> Project | None:
        if not (db_obj.schema_id):
            return None
        db_obj.schema.project_schema.remove(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def record_activity(
        self,
        db: Session,
        *,
        user: User,
        db_obj: Project,
        custodians_only: bool = False,
        alert: bool = False,
        message: str = "",
    ) -> bool:
        obj_in = {
            "custodians_only": custodians_only,
            "alert": alert,
            "message": message,
            "researcher_id": user.id,
            "project_id": db_obj.id,
        }
        return crud_activity.create(db=db, obj_in=obj_in)


project = CRUDProject(Project)
