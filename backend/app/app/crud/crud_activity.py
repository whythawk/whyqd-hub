from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Session

# from sqlalchemy import and_, or_
# from uuid import UUID

from app.crud.base import CRUDBase
from app.models import Activity, User, Role, Project, Task, Resource
from app.schemas import ActivityCreate, ActivityUpdate
from app.schema_types.role import RoleType
from app.schema_types.state import StateType
from app.crud.crud_role import role as crud_role
from app.core.config import settings


class CRUDActivity(CRUDBase[Activity, ActivityCreate, ActivityUpdate]):
    def get_for_researcher(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        state: StateType | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        alert: bool = False,
        custodian: bool = False,
        descending: bool = True,
        page: int = 0,
        page_break: bool = False,
    ) -> list[Activity]:
        db_objs = db.query(self.model)
        responsibilities = crud_role._get_responsibility(responsibility=responsibility)
        auth_filter = (
            (Role.researcher_id == user.id)
            & (Role.is_validated)
            & (
                ((self.model.custodians_only) & (Role.responsibility == RoleType.CUSTODIAN))
                | (~(self.model.custodians_only) & (Role.responsibility.in_(responsibilities)))
            )
        )
        db_objs = db_objs.filter(
            Activity.project.has(Project.auths.any(auth_filter))
            | Activity.task.has(Task.auths.any(auth_filter))
            | Activity.resource.has(Resource.auths.any(auth_filter))
        )
        if state:
            db_objs = db_objs.filter(self.model.resource.has(Resource.state == state))
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
        if alert:
            db_objs = db_objs.filter(self.model.alert)
        if custodian:
            db_objs = db_objs.filter(self.model.custodians_only)
        order_by = self.model.created
        if descending:
            order_by = order_by.desc()
        db_objs = db_objs.distinct().order_by(order_by)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def get_by_researcher(
        self,
        db: Session,
        *,
        user: User,
        researcher: User,
        responsibility: RoleType = RoleType.SEEKER,
        state: StateType | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        alert: bool = False,
        custodian: bool = False,
        descending: bool = True,
        page: int = 0,
        page_break: bool = False,
    ) -> list[Activity]:
        db_objs = db.query(self.model)
        responsibilities = crud_role._get_responsibility(responsibility=responsibility)
        auth_filter = (
            (Role.researcher_id == user.id)
            & (Role.is_validated)
            & (
                ((self.model.custodians_only) & (Role.responsibility == RoleType.CUSTODIAN))
                | (~(self.model.custodians_only) & (Role.responsibility.in_(responsibilities)))
            )
        )
        db_objs = db_objs.filter(
            (
                Activity.project.has(Project.auths.any(auth_filter))
                | Activity.task.has(Task.auths.any(auth_filter))
                | Activity.resource.has(Resource.auths.any(auth_filter))
            )
            & (Activity.researcher_id == researcher.id)
        )
        if state:
            db_objs = db_objs.filter(self.model.resource.has(Resource.state == state))
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
        if alert:
            db_objs = db_objs.filter(self.model.alert)
        if custodian:
            db_objs = db_objs.filter(self.model.custodians_only)
        order_by = self.model.created
        if descending:
            order_by = order_by.desc()
        db_objs = db_objs.distinct().order_by(order_by)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()


activity = CRUDActivity(Activity)
