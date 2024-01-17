from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sqlalchemy import nullslast
from uuid import UUID
from datetime import datetime

from app.crud.whyqd_base import CRUDWhyqdBase
from app.models.project import Project
from app.models.task import Task
from app.models.reference import Reference
from app.models.reference_template import ReferenceTemplate
from app.schemas.task import TaskCreate, TaskUpdate
from app.schema_types import RoleType, ReferenceType, DCAccrualPolicyType, DCFrequencyType

# from app.crud.crud_project import project as crud_project
from app.crud.crud_role import role as crud_role
from app.crud.crud_activity import activity as crud_activity
from app.core.config import settings

if TYPE_CHECKING:
    from app.models.resource import Resource
    from app.models.user import User


class CRUDTask(CRUDWhyqdBase[Task, TaskCreate, TaskUpdate]):
    def add_project(
        self,
        db: Session,
        *,
        db_obj: Task,
        project_obj: Project,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Task | None:
        task_in = TaskUpdate.from_orm(db_obj)
        task_in.project_id = project_obj.id
        return super().update(db=db, id=db_obj.id, obj_in=task_in, user=user, responsibility=responsibility)

    def remove_project(
        self,
        db: Session,
        *,
        db_obj: Task,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Task | None:
        task_in = TaskUpdate.from_orm(db_obj)
        task_in.project_id = None
        return super().update(db=db, id=db_obj.id, obj_in=task_in, user=user, responsibility=responsibility)

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
        page: int = 0,
        page_break: bool = False,
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
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def get_scheduled_multi(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        project_obj: Project | None = None,
        match: str | None = None,
        scheduled: bool = False,
        accrualPolicy: DCAccrualPolicyType | None = None,
        accrualPeriodicity: DCFrequencyType | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        prioritised: bool = True,
        page: int = 0,
        page_break: bool = False,
    ) -> list[Task]:
        db_objs = db.query(self.model)
        if scheduled:
            db_objs = db_objs.filter(
                (
                    (func.extract("EPOCH", func.now()) - func.extract("EPOCH", self.model.last_scheduled))
                    >= self.model.scheduled_period
                )
                | (
                    (self.model.last_scheduled == None)  # noqa: E711
                    & (
                        (func.extract("EPOCH", func.now()) - func.extract("EPOCH", self.model.temporalStart))
                        >= self.model.scheduled_period
                    )
                )
                | (
                    (self.model.last_scheduled == None)  # noqa: E711
                    & (self.model.temporalStart == None)  # noqa: E711
                    & (
                        (func.extract("EPOCH", func.now()) - func.extract("EPOCH", self.model.created))
                        >= self.model.scheduled_period
                    )
                )
            )
        if accrualPolicy:
            db_objs = db_objs.filter(self.model.accrualPolicy == accrualPolicy)
        if accrualPeriodicity:
            db_objs = db_objs.filter(self.model.accrualPeriodicity == accrualPeriodicity)
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
        if prioritised:
            db_objs = db_objs.order_by(
                self.model.scheduled.desc(), nullslast(self.model.accrualPriority.desc()), self.model.title
            )
        else:
            db_objs = db_objs.order_by(self.model.title)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
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
