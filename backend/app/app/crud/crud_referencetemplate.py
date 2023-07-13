from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Session, Query, aliased
from uuid import UUID
from whyqd.models import SchemaModel, CrosswalkModel
import whyqd as qd

from app.crud.whyqd_base import CRUDWhyqdBase
from app.models.reference_template import ReferenceTemplate
from app.models.resource import Resource
from app.models.task import Task
from app.models.project import Project
from app.schemas.reference_template import ReferenceTemplateCreate, ReferenceTemplateUpdate
from app.schemas.templates import DataSourceAttributeModel, CrosswalkTemplateModel
from app.schema_types import RoleType, ReferenceType

# from app.crud.crud_task import task as crud_task
from app.crud.crud_files import files as crud_files
from app.crud.crud_role import role as crud_role
from app.core.config import settings

if TYPE_CHECKING:
    from app.models.user import User


class CRUDReferenceTemplate(CRUDWhyqdBase[ReferenceTemplate, ReferenceTemplateCreate, ReferenceTemplateUpdate]):
    ###################################################################################################
    # CRUD ENHANCEMENT
    ###################################################################################################
    def get_multi(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        reference_type: ReferenceType | None = None,
        match: str | None = None,
        skip: int = 0,
        limit: int | None = None,
    ) -> list[ReferenceTemplate]:
        db_objs = db.query(self.model)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_objs = self._get_query(db_query=db_objs, user=user, responsibilities=responsibilities)
        if reference_type:
            db_objs = db_objs.filter(self.model.model_type == reference_type)
        if match:
            db_objs = db_objs.filter(
                (
                    self.model.name_vector.match(str(match))
                    | self.model.title_vector.match(str(match))
                    | self.model.description_vector.match(str(match))
                )
            )
        if skip:
            db_objs = db_objs.offset(skip)
        if limit and (limit <= settings.MULTI_MAX):
            db_objs = db_objs.limit(limit)
        return db_objs.all()

    def create(
        self,
        db: Session,
        *,
        user: User,
        template_in: DataSourceAttributeModel | CrosswalkTemplateModel,
        reference_type: ReferenceType,
    ) -> ReferenceTemplate:
        template_in = crud_files.create_or_update(user=user, obj_in=template_in, obj_type=reference_type)
        obj_in = {
            "name": template_in.name,
            "title": template_in.title,
            "description": template_in.description,
            "model": template_in.uuid,
            "model_type": reference_type,
        }
        if "version" in template_in.dict() and template_in.version:
            obj_in["version"] = template_in.version[-1].updated
        if "mime" in template_in.dict() and template_in.mime:
            obj_in["mime_type"] = template_in.mime
        obj_in = ReferenceTemplateCreate(**obj_in)
        return super().create(db=db, obj_in=obj_in, user=user)

    def update(
        self,
        db: Session,
        *,
        id: UUID | str,
        user: User,
        template_in: DataSourceAttributeModel | CrosswalkTemplateModel,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> ReferenceTemplate | None:
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if (
            not db_obj
            or db_obj.model != template_in.uuid
            or not crud_files.get(obj_id=template_in.uuid, obj_type=db_obj.model_type)
        ):
            raise ValueError(f"{template_in.name} mismatch.")
        template_in = crud_files.create_or_update(user=user, obj_in=template_in, obj_type=db_obj.model_type)
        obj_in = ReferenceTemplateUpdate.from_orm(db_obj).dict()
        obj_in["name"] = template_in.name
        obj_in["title"] = template_in.title
        obj_in["description"] = template_in.description
        if "version" in template_in.dict() and template_in.version:
            obj_in["version"] = template_in.version[-1].updated
        if "mimetype" in template_in.dict() and template_in.mime:
            obj_in["mimetype"] = template_in.mime
        obj_in = ReferenceTemplateUpdate(**obj_in)
        return super().update(db=db, id=db_obj.id, obj_in=obj_in, user=user, responsibility=responsibility)

    def _remove(
        self,
        db: Session,
        *,
        db_obj: ReferenceTemplate,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
        remove_history: bool = False,
    ) -> ReferenceTemplate | None:
        if remove_history and db_obj.older:
            self._remove(
                db=db,
                db_obj=db_obj.older,
                user=user,
                responsibility=responsibility,
                remove_history=remove_history,
            )
        crud_files.remove(obj_id=db_obj.model, obj_type=db_obj.model_type)
        db.delete(db_obj)
        db.commit()
        return db_obj

    def remove(
        self,
        db: Session,
        *,
        id: UUID | str,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
        remove_history: bool = False,
    ) -> ReferenceTemplate | None:
        # If `remove_history`, only goes back, not forward
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if not db_obj:
            raise ValueError("Reference does not exist or insufficient permissions for the task.")
        if db_obj.newer and db_obj.older and not remove_history:
            # This is a problem, and we're not going to mess with it
            raise ValueError(
                "You can't strand a reference history. If you want to remove a reference, which isn't the latest, also remove its history."
            )
        return self._remove(
            db=db,
            db_obj=db_obj,
            user=user,
            responsibility=responsibility,
            remove_history=remove_history,
        )

    # def has_role(self, db: Session, *, user: User, responsibility: RoleType, db_obj: ReferenceTemplate) -> bool:
    #     if super().has_role(db=db, user=user, responsibility=responsibility, db_obj=db_obj):
    #         return True
    #     if db_obj.task:
    #         return crud_task.has_role(db=db, user=user, db_obj=db_obj.crud_task)
    #     return False

    ###################################################################################################
    # TEMPLATE UTILITIES
    ###################################################################################################
    def get_crosswalk_definition(
        self,
        *,
        schema_in: SchemaModel,
    ) -> ReferenceTemplate:
        crosswalk = qd.CrosswalkDefinition()
        # We need it to validate, but aren't especially worried about much else
        crosswalk.set(schema_source=schema_in, schema_destination=schema_in)
        return crosswalk

    def create_crosswalk(
        self,
        db: Session,
        *,
        user: User,
        crosswalk_in: CrosswalkModel,
        schema_id: UUID | str,
        schema_hash: str,
    ) -> ReferenceTemplate:
        template_in = {
            "name": crosswalk_in.name,
            "title": crosswalk_in.title,
            "description": crosswalk_in.description,
            "schemaObject": schema_id,
            "schemaHash": schema_hash,
            "actions": crosswalk_in.actions,
        }
        template_in = CrosswalkTemplateModel(**template_in)
        return self.create(db=db, user=user, template_in=template_in, reference_type=ReferenceType.CROSSWALK)

    ###################################################################################################
    # UTILITIES
    ###################################################################################################
    def _get_query(self, *, db_query: Query, user: User, responsibilities: list[RoleType]) -> Query:
        resource_alias = aliased(Resource)
        task_alias = aliased(Task)
        project_alias = aliased(Project)
        db_filter = (
            ~(self.model.is_private)
            | (self._get_filter(db_model=self.model, user=user, responsibilities=responsibilities))
            | (self._get_filter(db_model=resource_alias, user=user, responsibilities=responsibilities))
            | (self._get_filter(db_model=task_alias, user=user, responsibilities=responsibilities))
            | (self._get_filter(db_model=project_alias, user=user, responsibilities=responsibilities))
        )
        return db_query.filter(db_filter)

    def get_by_model(
        self, db: Session, *, model_id: UUID | str, user: User, responsibility: RoleType = RoleType.SEEKER
    ) -> ReferenceTemplate | None:
        db_obj = db.query(self.model).filter(self.model.model == model_id)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_obj = self._get_query(db_query=db_obj, user=user, responsibilities=responsibilities)
        return db_obj.first()

    def get_model(
        self,
        db: Session,
        *,
        id: UUID | str,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
    ) -> DataSourceAttributeModel | CrosswalkTemplateModel | None:
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if db_obj:
            return crud_files.get(obj_id=db_obj.model, obj_type=db_obj.model_type, is_template=True)
        return None

    def get_model_from_task(
        self,
        *,
        task: Task,
        obj_type: ReferenceType | None = ReferenceType.DATASOURCE,
    ) -> DataSourceAttributeModel | CrosswalkTemplateModel | None:
        db_obj = task.crosswalk
        if obj_type == ReferenceType.DATASOURCE:
            db_obj = task.datasource
        if db_obj:
            return crud_files.get(obj_id=db_obj.model, obj_type=obj_type, is_template=True)
        return None


referencetemplate = CRUDReferenceTemplate(ReferenceTemplate)
