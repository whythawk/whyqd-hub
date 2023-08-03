from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from uuid import UUID, uuid4
from sqlalchemy.orm import Session, Query  # , aliased
import hashlib
import whyqd as qd
from whyqd.parsers import CoreParser
from whyqd.models import (
    DataSourceModel,
    SchemaModel,
    CrosswalkModel,
    TransformModel,
    FieldModel,
    ColumnModel,
    ActionScriptModel,
)

from app.crud.whyqd_base import CRUDWhyqdBase
from app.models.reference import Reference
from app.models.resource import Resource
from app.models.task import Task
from app.models.project import Project
from app.schemas.task import TaskCreate
from app.schemas.crosswalk import ActionModel
from app.schemas.reference import ReferenceCreate, ReferenceUpdate
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceModelLinks,
    ResourceManager,
    ResourceDataReference,
    ResourceSchemaReference,
    ResourceCrosswalkManager,
    ResourceCrosswalkReference,
)
from app.schemas.templates import DataSourceTemplateModel
from app.schema_types import ReferenceType, RoleType, StateType, MimeType
from app.crud.crud_resource import resource as crud_resource

# from app.crud.crud_project import project as crud_project
from app.crud.crud_task import task as crud_task
from app.crud.crud_activity import activity as crud_activity
from app.crud.crud_files import files as crud_files
from app.crud.crud_subscription import subscription as crud_subscription
from app.crud.crud_role import role as crud_role
from app.crud.crud_referencetemplate import referencetemplate as crud_referencetemplate
from app.core.config import settings

if TYPE_CHECKING:
    from app.models.user import User


class CRUDReference(CRUDWhyqdBase[Reference, ReferenceCreate, ReferenceUpdate]):
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
        mime_type: MimeType | None = None,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        descending: bool = True,
        page: int = 0,
        page_break: bool = False,
    ) -> list[Reference]:
        db_objs = db.query(self.model)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_objs = self._get_query(db_query=db_objs, user=user, responsibilities=responsibilities)
        if reference_type:
            db_objs = db_objs.filter(self.model.model_type == reference_type)
        else:
            db_objs = db_objs.filter(self.model.model_type != ReferenceType.DATASOURCE)
        if reference_type in [ReferenceType.DATA, ReferenceType.DATASOURCE] and mime_type:
            db_objs = db_objs.filter(self.model.mime_type == mime_type)
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

    def create(
        self,
        db: Session,
        *,
        user: User,
        reference_in: DataSourceModel | SchemaModel | CrosswalkModel | TransformModel,
        reference_type: ReferenceType,
        branch: bool = False,
    ) -> Reference:
        reference_in = crud_files.create_or_update(
            user=user, obj_in=reference_in, obj_type=reference_type, branch=branch
        )
        obj_in = {
            "name": reference_in.name,
            "title": reference_in.title,
            "description": reference_in.description,
            "model": reference_in.uuid,
            "model_type": reference_type,
        }
        if "version" in reference_in.dict() and reference_in.version:
            obj_in["version"] = reference_in.version[-1].updated
        for term in ["hash", "index"]:
            if term in reference_in.dict():
                obj_in[term] = reference_in.dict()[term]
        if "mime" in reference_in.dict() and reference_in.mime:
            obj_in["mime_type"] = reference_in.mime
        if reference_type == ReferenceType.SCHEMA:
            obj_in["hash"] = self.get_term_hash(terms=reference_in.fields)
        if reference_type == ReferenceType.CROSSWALK:
            obj_in["hash"] = self.get_term_hash(terms=reference_in.actions)
        obj_in = ReferenceCreate(**obj_in)
        db_obj = super().create(db=db, obj_in=obj_in, user=user)
        if reference_type == ReferenceType.DATASOURCE:
            # Because we need the id
            crud_files.save_data_summary(obj_id=db_obj.id, obj_in=reference_in)
        return db_obj

    def create_multi_tasks_from_project(
        self,
        db: Session,
        *,
        user: User,
        project_obj: Project,
        tasks_in: list[TaskCreate],
        field_name: str | None = None,
    ):
        # If project_obj.schema and field_name, we're creating a crosswalk template
        # If only a schema, then Task has a schema template
        schema_model = None
        if project_obj.schema:
            schema_model = self.get_model(db_obj=project_obj.schema)
            schema_dfn = qd.SchemaDefinition(source=schema_model)
            if field_name:
                field_name = schema_dfn.fields.get(name=UUID(field_name))
            if not field_name:
                schema_model = None
            else:
                field_name = field_name.name
        for task_in in tasks_in:
            task_in.project_id = project_obj.id
            # 1. Create the crosswalk or schema templates
            if schema_model:
                script = f"NEW > '{field_name}' < ['{task_in.name}']"
                crosswalk_dfn = crud_referencetemplate.get_crosswalk_definition(schema_in=schema_model)
                crosswalk_dfn.actions.add(term=script)
                crosswalk_dfn.get.name = task_in.name
                crosswalk_dfn.get.title = task_in.title
                crosswalk_dfn.get.description = task_in.description
                template_obj = crud_referencetemplate.create_crosswalk(
                    db=db,
                    user=user,
                    crosswalk_in=crosswalk_dfn.get,
                    schema_id=project_obj.schema.id,
                    schema_hash=project_obj.schema.hash,
                )
                task_in.crosswalk_id = template_obj.id
                task_in.schema_id = project_obj.schema.id
            if not schema_model and project_obj.schema:
                task_in.schema_id = project_obj.schema.id
            # 2. Create the task
            crud_task.create(db=db, obj_in=task_in, user=user)

    def update(
        self,
        db: Session,
        *,
        id: UUID | str,
        user: User,
        reference_in: DataSourceModel | SchemaModel | CrosswalkModel | TransformModel,
        reference_type: ReferenceType,
        responsibility: RoleType = RoleType.CURATOR,
        branch: bool = False,
        enforce_hash_consistency: bool = False,
    ) -> Reference | None:
        # `enforce_hash_consistency` requires that the updated hash must be the same as the original, unless this is being
        # branched - this is mostly used for `schema_subject` where the source data cannot change for a `resource`
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if not branch and (
            db_obj.model != reference_in.uuid or not crud_files.get(obj_id=reference_in.uuid, obj_type=reference_type)
        ):
            raise ValueError(f"{reference_type.name} mismatch. Did you intend to branch this reference?")
        if branch:
            # If it's a branch, then it's effectively creating a new reference
            new_obj = self.create(
                db=db,
                user=user,
                reference_in=reference_in,
                reference_type=reference_type,
                branch=branch,
            )
            crud_role.extend(db=db, user=user, old_obj=db_obj, new_obj=new_obj)
            new_obj.older_id = db_obj.id
            db.add(new_obj)
            db.commit()
            db.refresh(new_obj)
            # Note, the new reference isn't tied to a resource ...
            return new_obj
        # Check hash consistency and update reference and model
        hash = None
        if reference_type == ReferenceType.SCHEMA:
            hash = self.get_term_hash(terms=reference_in.fields)
        if reference_type == ReferenceType.CROSSWALK:
            hash = self.get_term_hash(terms=reference_in.actions)
        if reference_type == ReferenceType.DATASOURCE:
            crud_files.save_data_summary(obj_id=db_obj.id, obj_in=reference_in)
        if enforce_hash_consistency:
            if not hash and "hash" in reference_in.dict():
                hash = reference_in.hash
            if not hash or hash != db_obj.hash:
                raise ValueError("Hash failed `enforce_hash_consistency`. Updated hash is different.")
        reference_in = crud_files.create_or_update(user=user, obj_in=reference_in, obj_type=reference_type)
        obj_in = ReferenceUpdate.from_orm(db_obj).dict()
        obj_in["name"] = reference_in.name
        obj_in["title"] = reference_in.title
        obj_in["description"] = reference_in.description
        if "version" in reference_in.dict() and reference_in.version:
            obj_in["version"] = reference_in.version[-1].updated
        for term in ["hash", "index", "mimetype"]:
            if term in reference_in.dict():
                obj_in[term] = reference_in.dict()[term]
        if hash:
            obj_in["hash"] = hash
        obj_in = ReferenceUpdate(**obj_in)
        return super().update(db=db, id=db_obj.id, obj_in=obj_in, user=user, responsibility=responsibility)

    def _remove(
        self,
        db: Session,
        *,
        db_obj: Reference,
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
        remove_history: bool = False,
    ) -> Reference | None:
        if remove_history and db_obj.older:
            self._remove(
                db=db,
                db_obj=db_obj.older,
                user=user,
                responsibility=responsibility,
                remove_history=remove_history,
            )
        if db_obj.model_type == ReferenceType.DATASOURCE:
            crud_files.delete_source(obj_id=db_obj.model, mimetype=db_obj.mime_type)
            crud_files.delete_data_summary(obj_id=db_obj.id)
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
    ) -> Reference | None:
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

    def remove_resource_transform(
        self,
        db: Session,
        *,
        db_obj: Resource,
        user: User,
        responsibility: RoleType = RoleType.WRANGLER,
    ) -> Resource | None:
        if not (db_obj.transform_id and db_obj.transformdata_id and db_obj.transformdatasource_id):
            return None
        self.remove(db=db, id=db_obj.transform_id, user=user)
        self.remove(db=db, id=db_obj.transformdata_id, user=user)
        self.remove(db=db, id=db_obj.transformdatasource_id, user=user)
        return crud_resource.update_state(
            db=db,
            db_obj=db_obj,
            user=user,
            state=StateType.TRANSFORM_READY,
            responsibility=responsibility,
        )

    def remove_resource_crosswalk(
        self,
        db: Session,
        *,
        db_obj: Resource,
        user: User,
        responsibility: RoleType = RoleType.WRANGLER,
    ) -> Resource | None:
        if not (db_obj.crosswalk_id):
            return None
        if db_obj.transform_id and db_obj.transformdata_id and db_obj.transformdatasource_id:
            db_obj = self.remove_resource_transform(db=db, db_obj=db_obj, user=user, responsibility=responsibility)
        db_obj.crosswalk.crosswalks.remove(db_obj)
        db.commit()
        db.refresh(db_obj)
        return self.add_new_resource_crosswalk(db=db, db_obj=db_obj, user=user)

    def remove_resource_schema_object(
        self,
        db: Session,
        *,
        db_obj: Resource,
        user: User,
        responsibility: RoleType = RoleType.WRANGLER,
    ) -> Resource | None:
        if not (db_obj.schema_object_id):
            return None
        if db_obj.crosswalk_id:
            db_obj = self.remove_resource_crosswalk(db=db, db_obj=db_obj, user=user, responsibility=responsibility)
        db_obj.schema_object.schema_objects.remove(db_obj)
        db.commit()
        db.refresh(db_obj)
        return crud_resource.update_state(
            db=db,
            db_obj=db_obj,
            user=user,
            state=StateType.SCHEMA_READY,
            responsibility=responsibility,
        )

    def add_resource_schema_object(
        self,
        db: Session,
        *,
        db_obj: Resource,
        schema_obj: Reference,
        user: User,
        responsibility: RoleType = RoleType.WRANGLER,
    ) -> Resource | None:
        if db_obj.schema_object_id:
            db_obj = self.remove_resource_schema_object(db=db, db_obj=db_obj, user=user, responsibility=responsibility)
        schema_obj.schema_objects.append(db_obj)
        state = StateType.CROSSWALK_READY
        if db_obj.schema_object_id and db_obj.schema_subject_id:
            crosswalk_prospects = self.find_crosswalk_prospects(
                db=db,
                schema_subject=db_obj.schema_subject,
                schema_object=db_obj.schema_object,
                user=user,
                responsibility=responsibility,
            )
            if crosswalk_prospects:
                # Just pick the first for now
                crosswalk_obj = next(iter(crosswalk_prospects))
                crosswalk_obj.crosswalks.append(db_obj)
                state = StateType.TRANSFORM_READY
        db.commit()
        db.refresh(db_obj)
        return crud_resource.update_state(
            db=db,
            db_obj=db_obj,
            user=user,
            state=state,
            responsibility=responsibility,
        )

    def add_new_resource_crosswalk(
        self,
        db: Session,
        *,
        db_obj: Resource,
        user: User,
        responsibility: RoleType = RoleType.WRANGLER,
    ) -> Resource | None:
        crosswalk_dfn = self.get_crosswalk_definition(db_obj=db_obj)
        if not crosswalk_dfn:
            return db_obj
        crosswalk_obj = self.create(
            db=db,
            user=user,
            reference_in=crosswalk_dfn.get,
            reference_type=ReferenceType.CROSSWALK,
        )
        crosswalk_obj.crosswalks.append(db_obj)
        db.commit()
        db.refresh(db_obj)
        return crud_resource.update_state(
            db=db,
            db_obj=db_obj,
            user=user,
            state=StateType.CROSSWALK_READY,
            responsibility=responsibility,
        )

    def get_resource_manager(
        self, db: Session, *, id: UUID | str, user: User, responsibility: RoleType = RoleType.WRANGLER
    ) -> ResourceManager | None:
        db_obj = crud_resource.get(db=db, id=id, user=user, responsibility=responsibility)
        if not db_obj:
            return None
        db_model = ResourceManager.from_orm(db_obj)
        # GET EACH REFERENCE MODEL
        # 1. Data source
        if db_obj.datasource and db_obj.data:
            reference_model = self.get_model(db=db, id=db_obj.data.id, user=user, responsibility=responsibility)
            reference_in = ResourceDataReference.from_orm(db_obj.data)
            reference_in.links = [
                ResourceModelLinks(
                    **{
                        "id": db_obj.datasource.id,
                        "model_type": db_obj.datasource.model_type,
                    }
                ),
                ResourceModelLinks(
                    **{
                        "id": db_obj.data.id,
                        "model_type": db_obj.data.model_type,
                    }
                ),
            ]
            reference_in.sheet_name = reference_model.sheet_name
            reference_in.mimeType = reference_model.mime
            reference_in.summarykeys = [c.name for c in reference_model.columns]
            reference_in.summary = crud_files.get_data_summary(
                obj_id=db_obj.datasource.id, sheet_name=reference_in.sheet_name
            )
            db_model.data = reference_in
        # 2. Schema subject
        if db_obj.schema_subject:
            reference_model = self.get_model(
                db=db, id=db_obj.schema_subject.id, user=user, responsibility=responsibility
            )
            reference_in = ResourceSchemaReference.from_orm(db_obj.schema_subject)
            reference_in.links = [
                ResourceModelLinks(
                    **{
                        "id": db_obj.schema_subject.id,
                        "model_type": db_obj.schema_subject.model_type,
                    }
                )
            ]
            reference_in.fields = reference_model.fields
            db_model.schema_subject = reference_in
        # 3. Transformed data
        if db_obj.transform and db_obj.transformdatasource and db_obj.transformdata:
            reference_model = self.get_model(
                db=db, id=db_obj.transformdata.id, user=user, responsibility=responsibility
            )
            reference_in = ResourceDataReference.from_orm(db_obj.transformdata)
            # Note, providing the transform model here, not the data model
            reference_in.links = [
                ResourceModelLinks(
                    **{
                        "id": db_obj.transformdatasource.id,
                        "model_type": db_obj.transformdatasource.model_type,
                    }
                ),
                ResourceModelLinks(
                    **{
                        "id": db_obj.transform.id,
                        "model_type": db_obj.transform.model_type,
                    }
                ),
            ]
            reference_in.name = db_obj.transform.name
            reference_in.title = db_obj.transform.title
            reference_in.description = db_obj.transform.description
            reference_in.sheet_name = reference_model.sheet_name
            reference_in.mimeType = reference_model.mime
            reference_in.summarykeys = [c.name for c in reference_model.columns]
            reference_in.summary = crud_files.get_data_summary(
                obj_id=db_obj.transformdatasource.id, sheet_name=reference_in.sheet_name
            )
            db_model.transformdata = reference_in
        return db_model

    def get_resource_crosswalk_manager(
        self, db: Session, *, db_obj: Resource, user: User, responsibility: RoleType = RoleType.WRANGLER
    ) -> ResourceCrosswalkManager | None:
        obj_dfn = self.get_crosswalk_definition(db_obj=db_obj)
        if not obj_dfn:
            return None
        db_model = ResourceCrosswalkManager.from_orm(db_obj)
        # GET EACH REFERENCE MODEL
        # 1. Data source
        if db_obj.datasource and db_obj.data:
            reference_model = self.get_model(db=db, id=db_obj.data.id, user=user, responsibility=responsibility)
            reference_in = ResourceDataReference.from_orm(db_obj.data)
            reference_in.links = [
                ResourceModelLinks(
                    **{
                        "id": db_obj.datasource.id,
                        "model_type": db_obj.datasource.model_type,
                    }
                ),
                ResourceModelLinks(
                    **{
                        "id": db_obj.data.id,
                        "model_type": db_obj.data.model_type,
                    }
                ),
            ]
            reference_in.sheet_name = reference_model.sheet_name
            reference_in.mimeType = reference_model.mime
            reference_in.summarykeys = [c.name for c in reference_model.columns]
            reference_in.summary = crud_files.get_data_summary(
                obj_id=db_obj.datasource.id, sheet_name=reference_in.sheet_name
            )
            db_model.data = reference_in
        # 2. Schema subject
        if db_obj.schema_subject:
            reference_model = self.get_model(
                db=db, id=db_obj.schema_subject.id, user=user, responsibility=responsibility
            )
            reference_in = ResourceSchemaReference.from_orm(db_obj.schema_subject)
            reference_in.links = [
                ResourceModelLinks(
                    **{
                        "id": db_obj.schema_subject.id,
                        "model_type": db_obj.schema_subject.model_type,
                    }
                )
            ]
            reference_in.fields = reference_model.fields
            db_model.schema_subject = reference_in
        # 3. Schema object
        if db_obj.schema_object:
            reference_model = self.get_model(
                db=db, id=db_obj.schema_object.id, user=user, responsibility=responsibility
            )
            reference_in = ResourceSchemaReference.from_orm(db_obj.schema_object)
            reference_in.links = [
                ResourceModelLinks(
                    **{
                        "id": db_obj.schema_object.id,
                        "model_type": db_obj.schema_object.model_type,
                    }
                )
            ]
            reference_in.fields = reference_model.fields
            db_model.schema_object = reference_in
        # 4. Crosswalk object
        reference_in = ResourceCrosswalkReference(**{"created": datetime.now()})
        if db_obj.crosswalk:
            reference_in = ResourceCrosswalkReference.from_orm(db_obj.crosswalk)
            reference_in.links = [
                ResourceModelLinks(
                    **{
                        "id": db_obj.crosswalk.id,
                        "model_type": db_obj.crosswalk.model_type,
                    }
                )
            ]
        reference_in.actions = []
        for action in obj_dfn.actions.get_all():
            uuid = action.uuid
            action = obj_dfn.actions.parse(script=action.script)
            reference_in.actions.append(self.parse_action_model(uuid=uuid, term=action))
        db_model.crosswalk = reference_in
        return db_model

    ###################################################################################################
    # ROLES AND RIGHTS
    ###################################################################################################
    def _get_query(self, *, db_query: Query, user: User, responsibilities: list[RoleType]) -> Query:
        db_filter = (
            ~(self.model.is_private)
            | (self._get_filter(db_model=self.model, user=user, responsibilities=responsibilities))
            | (
                self.model.datasource.any(Resource.datasource)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.data.any(Resource.data)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.schema_subjects.any(Resource.schema_subject)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.crosswalks.any(Resource.crosswalk)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.schema_objects.any(Resource.schema_object)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.transforms.any(Resource.transform)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.transformdata.any(Resource.transformdata)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.transformdatasource.any(Resource.transformdatasource)
                & self._get_filter(db_model=Resource, user=user, responsibilities=responsibilities)
            )
            | (
                self.model.task_schema.any(Task.schema).where(
                    self._get_filter(db_model=Task, user=user, responsibilities=responsibilities)
                )
            )
            | (
                self.model.project_schema.any(Project.schema).where(
                    self._get_filter(db_model=Project, user=user, responsibilities=responsibilities)
                )
            )
        )
        return db_query.filter(db_filter)

    # def _has_role(self, db: Session, *, user: User, responsibility: RoleType, resource_objs: list[Resource]) -> bool:
    #     for db_obj in resource_objs:
    #         if crud_resource.has_role(db=db, user=user, responsibility=responsibility, db_obj=db_obj):
    #             return True
    #     return False

    # def has_role(self, db: Session, *, user: User, responsibility: RoleType, db_obj: Reference) -> bool:
    #     # 1. Check self
    #     if super().has_role(db=db, user=user, responsibility=responsibility, db_obj=db_obj):
    #         return True
    #     # 2. If of `SCHEMA` type
    #     if db_obj.model_type == ReferenceType.SCHEMA:
    #         if db_obj.task_schema.all():
    #             for task_obj in db_obj.task_schema.all():
    #                 if crud_task.has_role(db=db, user=user, responsibility=responsibility, db_obj=task_obj):
    #                     return True
    #         if db_obj.project_schema.all():
    #             for project_obj in db_obj.project_schema.all():
    #                 if crud_project.has_role(db=db, user=user, responsibility=responsibility, db_obj=project_obj):
    #                     return True
    #         if self._has_role(
    #             db=db, user=user, responsibility=responsibility, resource_objs=db_obj.schema_subjects.all()
    #         ):
    #             return True
    #         return self._has_role(
    #             db=db, user=user, responsibility=responsibility, resource_objs=db_obj.schema_objects.all()
    #         )
    #     # 3. If of `DATASOURCE` type
    #     if db_obj.model_type == ReferenceType.DATASOURCE:
    #         if self._has_role(db=db, user=user, responsibility=responsibility, resource_objs=db_obj.datasource.all()):
    #             return True
    #         return self._has_role(
    #             user=user, responsibility=responsibility, resource_objs=db_obj.transformdatasource.all()
    #         )
    #     # 4. If of `DATA` type
    #     if db_obj.model_type == ReferenceType.DATA:
    #         if self._has_role(db=db, user=user, responsibility=responsibility, resource_objs=db_obj.data.all()):
    #             return True
    #         return self._has_role(
    #             db=db, user=user, responsibility=responsibility, resource_objs=db_obj.transformdata.all()
    #         )
    #     # 5. If of `CROSSWALK` type
    #     if db_obj.model_type == ReferenceType.CROSSWALK:
    #         return self._has_role(
    #             db=db, user=user, responsibility=responsibility, resource_objs=db_obj.crosswalks.all()
    #         )
    #     # 6. If of `TRANSFORM` type
    #     if db_obj.model_type == ReferenceType.TRANSFORM:
    #         return self._has_role(
    #             db=db, user=user, responsibility=responsibility, resource_objs=db_obj.transforms.all()
    #         )
    #     return False

    ###################################################################################################
    # WHYQD WORKFLOW
    ###################################################################################################
    def import_source(
        self,
        *,
        db: Session,
        user: User,
        datasource_in: DataSourceTemplateModel,
        task: Task | None = None,
    ) -> None:
        # ASSUMES ALREADY RUN CRUD.FILES.IMPORT_SOURCE #################################################################
        # 1. Import source data from temporary path, process, and delete from temporary path ###########################
        #    1.4 Update Activities with link to RESOURCE and resource state
        #    1.5 Delete temporary source
        # Set resource metadata ########################################################################################
        if task and task.name:
            resource_in = {
                "name": task.name,
                "title": task.title,
                "description": task.description,
            }
        else:
            resource_in = {
                "name": datasource_in.name,
                "title": datasource_in.title,
                "description": datasource_in.description,
            }
        resource_in = ResourceCreate(**resource_in)
        # Check of a schema object is specified ########################################################################
        schema_object_in = None
        if task:
            resource_in.task_id = task.id
            if task.schema:
                schema_object_in = task.schema
            elif task.project and task.project.schema:
                schema_object_in = task.project.schema
            elif task.crosswalk:
                crosswalk = crud_referencetemplate.get_model_from_task(task=task, obj_type=ReferenceType.CROSSWALK)
                if crosswalk and crosswalk.schemaObject:
                    schema_object_in = self.get_by_model(db=db, model_id=crosswalk.schemaObject, user=user)
                    if schema_object_in and schema_object_in.hash != crosswalk.schemaHash:
                        schema_object_in = None
        if schema_object_in:
            resource_in.schema_object_id = schema_object_in.id
        # Import source and derive data model, or identify duplicate ###################################################
        datasource = qd.DataSourceDefinition()
        source_path = crud_files.get_source_path(
            obj_id=datasource_in.uuid, mimetype=datasource_in.mime, is_temporary=True
        )
        # This seems to crash under weird circumstances
        attributes = datasource_in.attributes
        if not isinstance(attributes, dict):
            attributes = attributes.terms
        if datasource_in.header == 0:
            datasource.derive_model(source=source_path, mimetype=datasource_in.mime, **attributes)
        else:
            datasource.derive_model(
                source=source_path,
                mimetype=datasource_in.mime,
                header=datasource_in.header,
                **attributes,
            )
        # Check HASH duplicate AND User subscription row limit #########################################################
        data_models = []
        if isinstance(datasource.model, list):
            for dsm in datasource.model:
                existing_sources = self.get_multi_by_hash(
                    db=db, hash=dsm.checksum, user=user, responsibility=RoleType.WRANGLER
                )
                if not self.record_existing_source(
                    db=db,
                    user=user,
                    source_name=datasource_in.name,
                    source_sheet=dsm.sheet_name,
                    sources=existing_sources,
                ) and not self.record_exceeds_limits(
                    db=db,
                    user=user,
                    source_name=datasource_in.name,
                    source_sheet=dsm.sheet_name,
                    source_count=dsm.index,
                    source_import=True,
                ):
                    data_models.append(dsm)
        else:
            existing_sources = self.get_multi_by_hash(
                db=db, hash=datasource.model.checksum, user=user, responsibility=RoleType.WRANGLER
            )
            if not self.record_existing_source(
                db=db, user=user, source_name=datasource_in.name, sources=existing_sources
            ) and not self.record_exceeds_limits(
                db=db,
                user=user,
                source_name=datasource_in.name,
                source_count=datasource.model.index,
                source_import=True,
            ):
                data_models.append(datasource.model)
        # Save the data models, data source models and data source #####################################################
        if not data_models:
            # delete the source file from temp
            return crud_files.delete_source(obj_id=datasource_in.uuid, mimetype=datasource_in.mime, is_temporary=True)
        source_path = crud_files.save_source(obj_id=datasource_in.uuid, mimetype=datasource_in.mime)
        datasource_obj = self.create(
            db=db, user=user, reference_in=datasource_in, reference_type=ReferenceType.DATASOURCE
        )
        resource_in.state = StateType.DATA_READY
        resource_in.datasource_id = datasource_obj.id
        for data_in in data_models:
            # Each data model requires its own resource, even if there is a single source file (multi-sheet excel)
            resource_in.id = uuid4()
            if datasource_in.path:
                data_in.path = str(datasource_in.path)  # maintain original path in storage
            else:
                data_in.path = f"{datasource_in.uuid}.{datasource_in.mime.name}"
            data_in.title = resource_in.title
            data_in.description = resource_in.description
            data_obj = self.create(db=db, user=user, reference_in=data_in, reference_type=ReferenceType.DATA)
            resource_in.data_id = data_obj.id
            # Check for a unique schema subject, or derive one #########################################################
            hash = self.get_term_hash(terms=data_in.columns)
            schema_prospects = self.get_multi_by_hash(db=db, hash=hash, user=user)
            schema_subject_in = None
            if len(schema_prospects) == 1:
                schema_subject_in = next(iter(schema_prospects))
            if not schema_prospects:
                data_in.path = str(source_path)  # use local path for operations
                schema_subject = qd.SchemaDefinition()
                schema_in: qd.models.SchemaModel = {
                    "name": resource_in.name,
                    "title": resource_in.title,
                    "description": resource_in.description,
                }
                schema_subject.set(schema=schema_in)
                schema_subject.derive_model(data=data_in)
                schema_subject_in = self.create(
                    db=db,
                    user=user,
                    reference_in=schema_subject.get,
                    reference_type=ReferenceType.SCHEMA,
                )
            if schema_subject_in:
                resource_in.schema_subject_id = schema_subject_in.id
                resource_in.state = StateType.SCHEMA_READY
            if resource_in.schema_object_id and resource_in.schema_subject_id:
                resource_in.state = StateType.CROSSWALK_READY
                # See if there is a crosswalk
                db_schema_subject = self.get(db=db, id=resource_in.schema_subject_id, user=user)
                db_schema_object = self.get(db=db, id=resource_in.schema_object_id, user=user)
                crosswalk_prospects = self.find_crosswalk_prospects(
                    db=db,
                    schema_subject=db_schema_subject,
                    schema_object=db_schema_object,
                    user=user,
                    responsibility=RoleType.SEEKER,
                )
                if crosswalk_prospects:
                    # Just pick the first for now
                    crosswalk_obj = next(iter(crosswalk_prospects))
                    resource_in.crosswalk_id = crosswalk_obj.id
                    resource_in.state = StateType.TRANSFORM_READY
            # And create the resource ##################################################################################
            resource_obj = crud_resource.create(db=db, obj_in=resource_in, user=user)
            if not resource_obj.crosswalk_id:
                resource_obj = self.add_new_resource_crosswalk(db=db, db_obj=resource_obj, user=user)
            message = f"Imported data source ({datasource_in.name}) successfully imported and ready for processing."
            if data_in.sheet_name:
                message = f"Data source ({datasource_in.name}, {data_in.sheet_name}) successfully imported and ready for processing."
            self._record_activity(db=db, user=user, db_obj=resource_obj, message=message)

    def derive_schema_subject(self, *, resource_obj: Resource) -> SchemaModel | None:
        data_in = self.get_data_model(resource_obj=resource_obj)
        if not data_in:
            return None
        schema_subject = qd.SchemaDefinition()
        schema_subject.derive_model(data=data_in)
        return schema_subject.get

    def derive_schema_categories(
        self, *, db: Session, resource_obj: Resource, user: User, field_name: str, as_bool: bool = False
    ) -> None:
        data_in = self.get_data_model(resource_obj=resource_obj)
        if not data_in or not resource_obj.schema_subject:
            message = f"Schema subject for field ({field_name}) categorisation is not found."
            self._record_activity(db=db, user=user, db_obj=resource_obj, message=message, alert=True)
            return None
        datasource = qd.DataSourceDefinition(source=data_in)
        schema_in = crud_files.get(
            obj_id=resource_obj.schema_subject.model,
            obj_type=resource_obj.schema_subject.model_type,
        )
        schema_subject = qd.SchemaDefinition(source=schema_in)
        try:
            schema_subject.fields.set_categories(name=field_name, terms=datasource.get_data(), as_bool=as_bool)
        except ValueError as e:
            message = e
            self._record_activity(db=db, user=user, db_obj=resource_obj, message=message, alert=True)
            return None
        self.update(
            db=db,
            id=resource_obj.schema_subject.id,
            user=user,
            reference_in=schema_subject.get,
            reference_type=ReferenceType.SCHEMA,
            responsibility=RoleType.WRANGLER,
        )
        message = f"Schema subject field ({field_name}) successfully categorised."
        self._record_activity(db=db, user=user, db_obj=resource_obj, message=message)

    def get_schema_definition(
        self, *, resource_obj: Resource | None = None, as_subject: bool = True
    ) -> qd.SchemaDefinition | None:
        # For websocket use, for interactive schema development
        if resource_obj:
            reference_obj = resource_obj.schema_subject
            if not as_subject:
                reference_obj = resource_obj.schema_object
            if reference_obj:
                schema = self.get_model(db_obj=reference_obj)
                return qd.SchemaDefinition(source=schema)
        if not as_subject:
            return qd.SchemaDefinition()
        return None

    def parse_action_chunks(self, *, terms: list, n: int) -> list:
        CORE = CoreParser()
        parsed = []
        for chunk in CORE.chunks(lst=terms, n=n):
            parsed.append([c.name for c in chunk])
        return parsed

    def parse_action_model(self, *, uuid: UUID | str, term: dict) -> ActionModel:
        # Summarised version of the action tree to present in the UI
        am = ActionModel(**{"uuid": str(uuid), "action": term["action"].name})
        if term.get("destination"):
            if isinstance(term["destination"], list):
                am.destinationField = [t.name for t in term["destination"]]
            else:
                am.destinationField = term["destination"].name
            if am.action == "NEW":
                am.sourceTerm = term["destination"].constraints.default.name
        if term.get("source"):
            if isinstance(term["source"], list):
                if am.action in ["CALCULATE", "SELECT_NEWEST", "SELECT_OLDEST"]:
                    n = 3
                    if am.action == "CALCULATE":
                        n = 2
                    am.sourceField = self.parse_action_chunks(terms=term["source"], n=n)
                else:
                    am.sourceField = [t.name for t in term["source"]]
            else:
                am.sourceField = term["source"].name
        if am.action == "CATEGORISE":
            # It already parsed, so it has to exist
            am.destinationTerm = term["category"].name
            am.sourceTerm = [t.name for t in term["assigned"]]
        if am.action == "PIVOT_CATEGORIES":
            am.rows = term["assigned"]
        if term.get("rows"):
            am.rows = term["rows"]
        if am.action in ["SEPARATE", "UNITE"] and term.get("source_param"):
            am.sourceTerm = term["source_param"]
        return am

    def get_crosswalk_definition(self, *, db_obj: Resource | Task) -> qd.CrosswalkDefinition | None:
        # For websocket use, for interactive crosswalk development
        if db_obj.crosswalk:
            crosswalk = self.get_model(db_obj=db_obj.crosswalk)
            return qd.CrosswalkDefinition(crosswalk=crosswalk)
        if isinstance(db_obj, Task) and db_obj.schema_object:
            # Setting up task template crosswalk for first time
            schema_object = self.get_model(db_obj=db_obj.schema_object)
            crosswalk = qd.CrosswalkDefinition(schema_source=schema_object, schema_destination=schema_object)
            crosswalk.model.name = db_obj.name
            if db_obj.title:
                crosswalk.model.title = db_obj.title
            if db_obj.description:
                crosswalk.model.description = db_obj.description
            return crosswalk
        if isinstance(db_obj, Resource) and db_obj.schema_subject and db_obj.schema_object:
            # Setting up resource crosswalk for first time
            schema_subject = self.get_model(db_obj=db_obj.schema_subject)
            schema_object = self.get_model(db_obj=db_obj.schema_object)
            crosswalk = qd.CrosswalkDefinition(schema_source=schema_subject, schema_destination=schema_object)
            if db_obj.task and db_obj.task.crosswalk:
                crosswalk_model = self.get_model(db_obj=db_obj.task.crosswalk)
                if crosswalk_model.actions:
                    crosswalk.actions.add_multi(terms=crosswalk_model.actions)
            crosswalk.model.name = db_obj.name
            if db_obj.title:
                crosswalk.model.title = db_obj.title
            if db_obj.description:
                crosswalk.model.description = db_obj.description
            return crosswalk
        # This isn't the place to define a schema
        return None

    def perform_transform(
        self,
        db: Session,
        *,
        resource_obj: Resource,
        mimetype: MimeType | None = None,
        user: User,
    ) -> bool:
        data_in = self.get_data_model(resource_obj=resource_obj)
        if not data_in or not resource_obj.crosswalk:
            # if already has a transform, this is forcing it again - like a validation
            return False
        crosswalk_in = crud_files.get(
            obj_id=resource_obj.crosswalk.model,
            obj_type=resource_obj.crosswalk.model_type,
        )
        transform = qd.TransformDefinition(crosswalk=crosswalk_in, data_source=data_in)
        try:
            transform.process()
            transform.data.empty
        except Exception as e:
            resource_obj = crud_resource.update_state(
                db=db, db_obj=resource_obj, user=user, state=StateType.TRANSFORM_ERROR, responsibility=RoleType.WRANGLER
            )
            self.record_error(db=db, user=user, db_obj=resource_obj, error=e, state=StateType.TRANSFORM_ERROR)
            return False
        if not transform.data.empty:
            # Schema models
            transformdatasource_in = crud_files.import_transform(data=transform.data, mimetype=mimetype)
            transformdatasource_in.title = resource_obj.title
            transformdatasource_in.description = resource_obj.description
            transformdata_in = crud_files.get_transform_datamodel(
                data=transform.data, datasource_in=transformdatasource_in
            )
            transformdata_in.title = resource_obj.title
            transformdata_in.description = resource_obj.description
            transform_in = transform.get
            transform_in.title = resource_obj.title
            transform_in.description = resource_obj.description
            # Create model objects
            transformdatasource_obj = self.create(
                db=db,
                user=user,
                reference_in=transformdatasource_in,
                reference_type=ReferenceType.DATASOURCE,
            )
            transformdata_obj = self.create(
                db=db,
                user=user,
                reference_in=transformdata_in,
                reference_type=ReferenceType.DATA,
            )
            transform_obj = self.create(
                db=db,
                user=user,
                reference_in=transform_in,
                reference_type=ReferenceType.TRANSFORM,
            )
            # Update Resource
            resource_in = ResourceUpdate.from_orm(resource_obj)
            resource_in.transformdatasource_id = transformdatasource_obj.id
            resource_in.transformdata_id = transformdata_obj.id
            resource_in.transform_id = transform_obj.id
            resource_in.state = StateType.COMPLETE
            resource_obj = crud_resource.update(
                db=db,
                id=resource_obj.id,
                user=user,
                obj_in=resource_in.dict(),
                responsibility=RoleType.WRANGLER,
            )
            self._record_activity(
                db=db,
                user=user,
                db_obj=resource_obj,
                message=f"Transform `{resource_obj.name}` is complete and data are ready for export.",
            )
            return True
        resource_obj = crud_resource.update_state(
            db=db, db_obj=resource_obj, user=user, state=StateType.TRANSFORM_ERROR, responsibility=RoleType.WRANGLER
        )
        self._record_activity(
            db=db,
            user=user,
            db_obj=resource_obj,
            message=f"Transform `{resource_obj.name}` failed. Please review the source data, schemas and crosswalk.",
        )
        return False

    ###################################################################################################
    # UTILITIES AND HASHING
    ###################################################################################################
    def get_by_model(
        self, db: Session, *, model_id: UUID | str, user: User, responsibility: RoleType = RoleType.SEEKER
    ) -> Reference | None:
        db_obj = db.query(self.model).filter(self.model.model == model_id)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_obj = self._get_query(db_query=db_obj, user=user, responsibilities=responsibilities)
        return db_obj.first()

    def get_model(
        self,
        db: Session | None = None,
        *,
        id: UUID | str | None = None,
        db_obj: Reference | None = None,
        user: User | None = None,
        responsibility: RoleType = RoleType.SEEKER,
    ) -> DataSourceModel | SchemaModel | CrosswalkModel | TransformModel | None:
        if not db_obj and id and db and user:
            db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if db_obj:
            return crud_files.get(obj_id=db_obj.model, obj_type=db_obj.model_type)
        return None

    def get_data_model(self, *, resource_obj: Resource) -> DataSourceModel | None:
        if not resource_obj.datasource and not resource_obj.data:
            return None
        datasource_in = crud_files.get(
            obj_id=resource_obj.datasource.model, obj_type=resource_obj.datasource.model_type
        )
        datasource_path = crud_files.get_source_path(obj_id=datasource_in.uuid, mimetype=datasource_in.mime)
        data_in = crud_files.get(obj_id=resource_obj.data.model, obj_type=resource_obj.data.model_type)
        data_in.path = str(datasource_path)
        return data_in

    def get_term_hash(self, *, terms: list[FieldModel] | list[ColumnModel] | list[ActionScriptModel]) -> str:
        # Used to match data models to schema models - only on fields/columns/actions
        # further matching required for constraints
        if not terms:
            return None
        if isinstance(terms[0], ActionScriptModel):
            terms = str(sorted([term.script for term in terms])).encode("utf-8")
        else:
            terms = str(sorted([term.name for term in terms])).encode("utf-8")
        return hashlib.blake2b(terms).hexdigest()

    def get_multi_by_hash(
        self, db: Session, *, hash: str, user: User, responsibility: RoleType = RoleType.SEEKER
    ) -> set[Reference]:
        db_objs = db.query(self.model).filter(self.model.hash == hash)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_objs = self._get_query(db_query=db_objs, user=user, responsibilities=responsibilities)
        return db_objs.all()

    def find_crosswalk_prospects(
        self,
        db: Session,
        *,
        schema_subject: Reference,
        schema_object: Reference,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
    ) -> set[Reference]:
        db_objs = db.query(Resource).filter(
            (Resource.schema_subject_id == schema_subject.id) & (Resource.schema_object_id == schema_object.id)
        )
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_objs = self._get_query(db_query=db_objs, user=user, responsibilities=responsibilities)
        return {db_obj.crosswalk for db_obj in db_objs.all()}

    def find_schema_prospects(
        self,
        db: Session,
        *,
        data_obj: Reference,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
    ) -> set[Reference]:
        schema_prospects = {}
        data_model = crud_files.get(obj_id=data_obj.model, obj_type=data_obj.model_type)
        if data_model:
            hash = self.get_term_hash(terms=data_model.columns)
            schema_prospects = self.get_multi_by_hash(db=db, hash=hash, user=user, responsibility=responsibility)
        return schema_prospects

    ###################################################################################################
    # RECORD ACTIVITIES
    ###################################################################################################
    def _record_activity(
        self,
        db: Session,
        *,
        user: User,
        db_obj: Resource | None = None,
        custodians_only: bool = False,
        alert: bool = False,
        message: str = "",
    ) -> bool:
        obj_in = {
            "custodians_only": custodians_only,
            "alert": alert,
            "message": message,
            "researcher_id": user.id,
        }
        if db_obj:
            obj_in["task_id"] = db_obj.task_id
            obj_in["resource_id"] = db_obj.id
            if db_obj.task:
                obj_in["project_id"] = db_obj.task.project_id
        return crud_activity.create(db=db, obj_in=obj_in)

    def record_existing_source(
        self, db: Session, *, user: User, sources: list[Resource], source_name: str, source_sheet: str | None = None
    ) -> bool:
        if not sources:
            return False
        message = f"Imported data source ({source_name}) already exists."
        if source_sheet:
            message = f"Imported data source ({source_name}, {source_sheet}) already exists."
        self._record_activity(db=db, user=user, db_obj=sources[0], alert=True, message=message)
        return True

    def record_exceeds_limits(
        self,
        db: Session,
        *,
        user: User,
        source_name: str,
        source_sheet: str | None = None,
        source_count: int,
        source_import: bool = True,
    ) -> bool:
        try:
            if crud_subscription.within_limits(db=db, user=user, row_count=source_count, data_import=True):
                return False
        except ValueError as e:
            if source_import:
                message = f"For data import ({source_name}): - {e}"
                if source_sheet:
                    message = f"For data import ({source_name}, {source_sheet}): - {e}"
            else:
                message = f"For data transform ({source_name}): - {e}"
            self._record_activity(db=db, user=user, alert=True, message=message)
            return True

    def record_error(
        self, db: Session, *, user: User, db_obj: Resource | None = None, error: str, state: StateType
    ) -> bool:
        message = f"{state.value} `{db_obj.name}`: {error}"
        self._record_activity(db=db, user=user, db_obj=db_obj, alert=True, message=message)
        return True


reference = CRUDReference(Reference)
