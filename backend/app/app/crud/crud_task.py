from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from app.crud.whyqd_base import CRUDWhyqdBase
from app.models.project import Project
from app.models.task import Task
from app.models.reference import Reference
from app.models.reference_template import ReferenceTemplate
from app.schemas.task import TaskCreate, TaskUpdate
from app.schema_types import RoleType, ReferenceType

# from app.crud.crud_project import project as crud_project
from app.crud.crud_role import role as crud_role
from app.crud.crud_activity import activity as crud_activity
from app.core.config import settings

if TYPE_CHECKING:
    from app.models.resource import Resource
    from app.models.user import User


class CRUDTask(CRUDWhyqdBase[Task, TaskCreate, TaskUpdate]):
    def add_resource(self, db: Session, *, db_obj: Task, resource_obj: Resource) -> Task | None:
        db_obj.resources.append(resource_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove_resource(self, db: Session, *, db_obj: Task, resource_obj: Resource) -> Task | None:
        db_obj.resources.remove(resource_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def add_template(
        self,
        db: Session,
        *,
        id: UUID | str,
        template_obj: Reference | ReferenceTemplate,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Task | None:
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if not db_obj:
            raise ValueError("Reference does not exist or insufficient permissions for the task.")
        task_in = TaskUpdate.from_orm(db_obj)
        if template_obj.model_type == ReferenceType.CROSSWALK:
            task_in.crosswalk_id = template_obj.id
        if template_obj.model_type == ReferenceType.DATASOURCE:
            task_in.datasource_id = template_obj.id
        if template_obj.model_type == ReferenceType.SCHEMA:
            task_in.schema_id = template_obj.id
        return super().update(db=db, id=id, obj_in=task_in, user=user, responsibility=responsibility)

    def remove_template(
        self,
        db: Session,
        *,
        id: UUID | str,
        template_type: ReferenceType,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Task | None:
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if not db_obj:
            raise ValueError("Reference does not exist or insufficient permissions for the task.")
        task_in = TaskUpdate.from_orm(db_obj)
        if template_type == ReferenceType.CROSSWALK:
            task_in.crosswalk_id = None
        if template_type == ReferenceType.DATASOURCE:
            task_in.datasource_id = None
        if template_type == ReferenceType.SCHEMA:
            task_in.schema_id = None
        return super().update(db=db, id=id, obj_in=task_in, user=user, responsibility=responsibility)

    # def has_role(self, db: Session, *, user: User, responsibility: RoleType, db_obj: Task) -> bool:
    #     if super().has_role(db=db, user=user, responsibility=responsibility, db_obj=db_obj):
    #         return True
    #     if db_obj.project:
    #         return crud_project.has_role(db=db, user=user, responsibility=responsibility, db_obj=db_obj.project)
    #     return False

    def get_multi(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        project_obj: Project | None = None,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        descending: bool = True,
        skip: int = 0,
        limit: int = None,
    ) -> list[Task]:
        db_objs = db.query(self.model)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_objs = self._get_query(db_query=db_objs, user=user, responsibilities=responsibilities)
        if project_obj:
            db_objs = db_objs.filter(self.model.project_id == project_obj.id)
        if date_from and date_to and date_from > date_to:
            date_to = None
        if date_to:
            if isinstance(date_to, str):
                date_to = datetime.strptime(date_to, "%Y-%m-%d")
            db_objs = db_objs.filter(self.model.created <= date_to)
        if date_from:
            if isinstance(date_from, str):
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
            db_objs = db_objs.filter(self.model.created >= date_from)
        if match:
            db_objs = db_objs.filter(
                (
                    self.model.name_vector.match(str(match))
                    | self.model.title_vector.match(str(match))
                    | self.model.description_vector.match(str(match))
                )
            )
        order_by = self.model.created
        if descending:
            order_by = order_by.desc()
        db_objs = db_objs.distinct().order_by(order_by)
        if skip:
            db_objs = db_objs.offset(skip)
        if limit and (limit <= settings.MULTI_MAX):
            db_objs = db_objs.limit(limit)
        return db_objs.all()

    def record_activity(
        self,
        db: Session,
        *,
        user: User,
        db_obj: Task,
        custodians_only: bool = False,
        alert: bool = False,
        message: str = "",
    ) -> bool:
        obj_in = {
            "custodians_only": custodians_only,
            "alert": alert,
            "message": message,
            "researcher_id": user.id,
            "project_id": db_obj.project_id,
            "task_id": db_obj.id,
        }
        return crud_activity.create(db=db, obj_in=obj_in)


task = CRUDTask(Task, [(Task.project, Project)])