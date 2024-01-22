from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.whyqd_base import CRUDWhyqdBase
from app.models.project import Project
from app.models.task import Task
from app.models.resource import Resource
from app.schemas.resource import ResourceCreate, ResourceUpdate
from app.schema_types import RoleType, StateType

# from app.crud.crud_task import task as crud_task
from app.crud.crud_activity import activity as crud_activity
from app.crud.crud_role import role as crud_role
from app.core.config import settings

if TYPE_CHECKING:
    from app.models.user import User


class CRUDResource(CRUDWhyqdBase[Resource, ResourceCreate, ResourceUpdate]):
    def get_multi(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        task_obj: Task | None = None,
        project_obj: Project | None = None,
        state: StateType | None = None,
        excludeComplete: bool = True,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        alert: bool = False,
        custodian: bool = False,
        prioritised: bool = True,
        page: int = 0,
        page_break: bool = False,
    ) -> list[Resource]:
        db_objs = db.query(self.model)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_objs = self._get_query(db_query=db_objs, user=user, responsibilities=responsibilities)
        if task_obj:
            db_objs = db_objs.filter(self.model.task_id == task_obj.id)
        if project_obj:
            db_objs = db_objs.filter((self.model.task_id == Task.id) & (Task.project_id == project_obj.id))
        if state:
            db_objs = db_objs.filter(self.model.state == state)
        if excludeComplete and not state:
            db_objs = db_objs.filter(self.model.state != StateType.COMPLETE)
        if date_from and date_to and date_from > date_to:
            date_to = None
        if date_to:
            if isinstance(date_to, str):
                date_to = datetime.strptime(date_to, "%Y-%m-%d")
            db_objs = db_objs.filter(self.model.latest_activity.created <= date_to)
        if date_from:
            if isinstance(date_from, str):
                date_from = datetime.strptime(date_from, "%Y-%m-%d")
            db_objs = db_objs.filter(self.model.latest_activity.created >= date_from)
        if match:
            db_objs = db_objs.filter(
                (
                    self.model.name_vector.match(str(match))
                    | self.model.title_vector.match(str(match))
                    | self.model.description_vector.match(str(match))
                )
            )
        if alert:
            db_objs = db_objs.filter(self.model.latest_activity.alert)
        if custodian:
            db_objs = db_objs.filter(self.model.latest_activity.custodians_only)
        if prioritised:
            db_objs = db_objs.order_by(self.model.latest_activity.desc(), self.model.title)
        else:
            db_objs = db_objs.order_by(self.model.title, self.model.latest_activity)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    # def has_role(self, db: Session, *, user: User, responsibility: RoleType, db_obj: Resource) -> bool:
    #     if super().has_role(db=db, user=user, responsibility=responsibility, db_obj=db_obj):
    #         return True
    #     if db_obj.task:
    #         return crud_task.has_role(db=db, user=user, responsibility=responsibility, db_obj=db_obj.task)
    #     return False

    def update_state(
        self,
        db: Session,
        *,
        db_obj: Resource,
        state: StateType,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> Resource | None:
        obj_in = ResourceUpdate.from_orm(db_obj)
        obj_in.state = state
        return super().update(db=db, id=db_obj.id, obj_in=obj_in, user=user, responsibility=responsibility)

    def record_activity(
        self,
        db: Session,
        *,
        user: User,
        db_obj: Resource,
        custodians_only: bool = False,
        alert: bool = False,
        message: str = "",
    ) -> bool:
        obj_in = {
            "custodians_only": custodians_only,
            "alert": alert,
            "message": message,
            "researcher_id": user.id,
            "task_id": db_obj.task_id,
            "resource_id": db_obj.id,
        }
        if db_obj.task:
            obj_in["project_id"] = db_obj.task.project_id
        return crud_activity.create(db=db, obj_in=obj_in)


resource = CRUDResource(Resource, [(Resource.task, Task), (Task.project, Project)])
