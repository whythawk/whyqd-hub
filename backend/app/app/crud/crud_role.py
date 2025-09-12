from __future__ import annotations
from sqlalchemy.orm import Session, Query
from uuid import UUID

# from app.schema_types import ReferenceType

# from pydantic import parse_obj_as
# from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate  # , Role as RoleInDB
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.resource import Resource
from app.models.reference import Reference
from app.models.reference_template import ReferenceTemplate
from app.schema_types import RoleType
from app.core.config import settings


class CRUDRole(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def create(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        db_obj: Project | Task | Resource | Reference | ReferenceTemplate,
        is_validated: bool = False,
    ) -> Role:
        obj_in = {"researcher_id": user.id, "responsibility": responsibility, "is_validated": is_validated}
        obj_in[self._get_by_type(db_obj=db_obj)] = db_obj.id
        obj_in = RoleCreate(**obj_in)
        return super().create(db=db, obj_in=obj_in)

    def extend(
        self,
        db: Session,
        *,
        user: User,
        old_obj: Project | Task | Resource | Reference | ReferenceTemplate,
        new_obj: Project | Task | Resource | Reference | ReferenceTemplate,
    ) -> None:
        db_objs = (
            db.query(Role)
            .filter(
                (self._get_by_type(db_obj=old_obj, as_model=True) == old_obj.id) & (self.model.researcher_id != user.id)
            )
            .all()
        )
        for obj in db_objs:
            obj_in = RoleUpdate.model_validate(obj).dict()
            for term in ["created", "id", self._get_by_type(db_obj=old_obj)]:
                # The two resources don't have to be the same so pop it here
                obj_in.pop(term, None)
            obj_in[self._get_by_type(db_obj=new_obj)] = new_obj.id
            obj_in = RoleCreate(**obj_in)
            super().create(db=db, obj_in=obj_in)

    def update(self, db: Session, *, db_obj: Role, responsibility: RoleType = RoleType.SEEKER) -> Role:
        obj_in = RoleUpdate.model_validate(db_obj)
        obj_in.responsibility = responsibility
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def validate(self, db: Session, *, db_obj: Role) -> Role:
        obj_in = RoleUpdate.model_validate(db_obj)
        obj_in.is_validated = True
        return super().update(db=db, db_obj=db_obj, obj_in=obj_in)

    def _get_responsibility(self, *, responsibility: RoleType) -> list[RoleType]:
        responsibilities = [RoleType.CUSTODIAN]
        if responsibility == RoleType.CURATOR:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR]
        if responsibility == RoleType.WRANGLER:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR, RoleType.WRANGLER]
        if responsibility == RoleType.SEEKER:
            responsibilities = [RoleType.CUSTODIAN, RoleType.CURATOR, RoleType.WRANGLER, RoleType.SEEKER]
        return responsibilities

    def _get_filter(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType,
        db_obj: Project | Task | Resource | Reference | ReferenceTemplate,
    ) -> Query | None:
        query = db.query(self.model)
        responsibilities = self._get_responsibility(responsibility=responsibility)
        filter = (
            (self.model.researcher_id == user.id)
            & (self.model.responsibility.in_(responsibilities))
            & (self.model.is_validated)
        )
        if isinstance(db_obj, Project):
            return query.filter(filter & (self.model.project_id == db_obj.id))
        if isinstance(db_obj, Task):
            return query.filter(filter & (self.model.task_id == db_obj.id))
        if isinstance(db_obj, Resource):
            return query.filter(filter & (self.model.resource_id == db_obj.id))
        if isinstance(db_obj, Reference):
            return query.filter(filter & (self.model.reference_id == db_obj.id))
        if isinstance(db_obj, ReferenceTemplate):
            return query.filter(filter & (self.model.referencetemplate_id == db_obj.id))
        return None

    def has_responsibility(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType,
        db_obj: Project | Task | Resource | Reference | ReferenceTemplate,
    ) -> bool:
        if user.is_superuser:
            return True
        query = self._get_filter(db=db, user=user, responsibility=responsibility, db_obj=db_obj)
        if query:
            return query.first() is not None
        return False

    def _get_by_type(
        self, *, db_obj: Project | Task | Resource | Reference | ReferenceTemplate, as_model: bool = False
    ) -> str:
        # This will fail if the `rtn_obj` doesn't have these terms
        if isinstance(db_obj, Project):
            if as_model:
                return self.model.project_id
            return "project_id"
        if isinstance(db_obj, Task):
            if as_model:
                return self.model.task_id
            return "task_id"
        if isinstance(db_obj, Resource):
            if as_model:
                return self.model.resource_id
            return "resource_id"
        if isinstance(db_obj, Reference):
            if as_model:
                return self.model.reference_id
            return "reference_id"
        if isinstance(db_obj, ReferenceTemplate):
            if as_model:
                return self.model.referencetemplate_id
            return "referencetemplate_id"

    def get_multi_by_project(
        self, db: Session, *, project_id: UUID, page: int = 0, page_break: bool = False
    ) -> list[Role]:
        db_objs = db.query(self.model).filter(Role.project_id == project_id)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def get_multi_by_member(
        self, db: Session, *, researcher_id: str, page: int = 0, page_break: bool = False
    ) -> list[Role]:
        db_objs = db.query(self.model).filter(Role.researcher_id == researcher_id)
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()

    def remove_member_from_project(self, db: Session, *, researcher_id: str, project_obj: Project) -> list[Role]:
        # NOTE: highly destructive ... cascades and removes member from all objects associated with this project
        # This may need review if it results in adverse behaviours (stranded assets or users being removed
        # from assets they should control but were attached to other assets, for example)
        db_objs = db.query(self.model).filter(Role.researcher_id == researcher_id)
        # Create the various lists of Project assets
        task_ids = [t.id for t in project_obj.tasks.all()]
        resource_ids = [r.id for t in project_obj.tasks.all() for r in t.resources.all()]
        reference_ids = [
            [
                r.datasource_id,
                r.data_id,
                r.schema_subject_id,
                r.crosswalk_id,
                r.schema_object_id,
                r.transform_id,
                r.transformdata_id,
                r.transformdatasource_id,
            ]
            for t in project_obj.tasks.all()
            for r in t.resources.all()
        ]
        # And flatten it (and remove any adverse Nones)
        reference_ids = [item for sublist in reference_ids for item in sublist if item is not None]
        db_objs = db_objs.filter(
            self.model.project_id.in_([project_obj.id])
            | self.model.task_id.in_(task_ids)
            | self.model.resource_id.in_(resource_ids)
            | self.model.reference_id.in_(reference_ids)
        ).all()
        for db_o in db_objs:
            db.delete(db_o)
        db.commit()
        db.refresh(project_obj)
        return project_obj


role = CRUDRole(Role)
