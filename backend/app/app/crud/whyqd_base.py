from __future__ import annotations
from typing import Generic, Type, TypeVar, Sequence

from fastapi.encoders import jsonable_encoder
from sqlalchemy import inspect
from sqlalchemy.orm import ONETOMANY
from pydantic import BaseModel
from sqlalchemy.orm import Session, Query
from uuid import UUID
from datetime import datetime

from app.db.base_class import Base
from app.schema_types import RoleType
from app.models import User, Role

# from app.crud.crud_user import user as crud_user
from app.crud.crud_role import role as crud_role
from app.core.config import settings

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDWhyqdBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], joins: list[tuple[Type[ModelType], Type[ModelType]]] = []):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.joins = joins

    def get(
        self, db: Session, *, id: UUID | str, user: User, responsibility: RoleType = RoleType.SEEKER
    ) -> ModelType | None:
        db_obj = db.query(self.model).filter(self.model.id == id)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_obj = self._get_query(db_query=db_obj, user=user, responsibilities=responsibilities)
        return db_obj.first()

    def get_multi(
        self,
        db: Session,
        *,
        user: User,
        responsibility: RoleType = RoleType.SEEKER,
        match: str | None = None,
        date_from: datetime | str | None = None,
        date_to: datetime | str | None = None,
        descending: bool = True,
        page: int = 0,
        page_break: bool = False,
    ) -> list[ModelType]:
        db_objs = db.query(self.model)
        if not user.is_superuser:
            responsibilities = crud_role._get_responsibility(responsibility=responsibility)
            db_objs = self._get_query(db_query=db_objs, user=user, responsibilities=responsibilities)
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

    def create(self, db: Session, *, obj_in: CreateSchemaType, user: User) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        crud_role.create(db=db, user=user, responsibility=RoleType.CUSTODIAN, db_obj=db_obj, is_validated=True)
        db.refresh(db_obj)
        message = f"{self.model.__name__} created."
        if db_obj.name:
            message = f"{self.model.__name__} created `{db_obj.name}`."
        self.record_activity(db=db, user=user, db_obj=db_obj, message=message)
        db.refresh(db_obj)
        return db_obj

    def create_multi(self, db: Session, *, objs_in: list[CreateSchemaType], user: User) -> list[ModelType]:
        db_objs = []
        for obj_in in objs_in:
            db_objs.append(self.create(db=db, obj_in=obj_in, user=user))
        return db_objs

    def update(
        self,
        db: Session,
        *,
        id: UUID | str,
        obj_in: UpdateSchemaType | dict[str, any],
        user: User,
        responsibility: RoleType = RoleType.CURATOR,
    ) -> ModelType | None:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if not db_obj or not (update_data.get("id") and db_obj.id == update_data["id"]):
            raise ValueError("Reference does not exist or insufficient permissions for the task.")
        obj_data = self.model_encoder(db_obj)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        message = f"{self.model.__name__} updated."
        if db_obj.name:
            message = f"{self.model.__name__} updated `{db_obj.name}`."
        self.record_activity(db=db, user=user, db_obj=db_obj, message=message)
        db.refresh(db_obj)
        return db_obj

    def remove(
        self, db: Session, *, id: UUID | str, user: User, responsibility: RoleType = RoleType.CURATOR
    ) -> ModelType | None:
        db_obj = self.get(db=db, id=id, user=user, responsibility=responsibility)
        if not db_obj:
            raise ValueError("Reference does not exist or insufficient permissions for the task.")
        db.delete(db_obj)
        db.commit()
        return None

    ###################################################################################################
    # UTILITIES
    ###################################################################################################

    # def has_role(self, db: Session, *, user: User, responsibility: RoleType, db_obj: ModelType) -> bool:
    #     return crud_role.has_responsibility(db=db, user=user, responsibility=responsibility, db_obj=db_obj)

    def record_activity(
        self,
        db: Session,
        *,
        user: User,
        db_obj: ModelType,
        custodians_only: bool = False,
        alert: bool = False,
        message: str = "",
    ) -> bool:
        return True

    def _get_filter(self, *, db_model: ModelType, user: User, responsibilities: list[RoleType]) -> Query:
        filter = (Role.researcher_id == user.id) & (Role.responsibility.in_(responsibilities)) & (Role.is_validated)
        return db_model.auths.any(filter)

    def _get_query(self, *, db_query: Query, user: User, responsibilities: list[RoleType]) -> Query:
        db_filter = ~(self.model.is_private) | (
            self._get_filter(db_model=self.model, user=user, responsibilities=responsibilities)
        )
        for dbj, dbq in self.joins:
            db_query = db_query.join(dbj)
            db_filter = db_filter | (self._get_filter(db_model=dbq, user=user, responsibilities=responsibilities))
        return db_query.filter(db_filter)

    def model_encoder(self, model: ModelType, **kwargs) -> dict:
        """
        Safely converts a model instance into a dict, so it can be JSON-encoded.

        :param model: Model instance, but for convenience will accept any value.
        :param kwargs: Additional kwargs to pass to :py:func:`jsonable_encoder`.

        :see: https://github.com/tiangolo/fastapi/discussions/9026
        :see: https://github.com/sqlalchemy/sqlalchemy/issues/9785
        https://github.com/fastapi/fastapi/discussions/9026#discussioncomment-7493716
        Note: Doesn't account for one-to-one and many-to-many relationships, mostly because OP hadn't yet worked out how best to do this
        """
        if isinstance(model, Base):
            mapper = inspect(model).mapper

            # Add non-relationship values.
            cleaned = {key: getattr(model, key) for key in mapper.columns.keys()}

            # Add "parent" (one-to-many) relations.
            cleaned.update(
                {
                    key: [self.model_encoder(value) for value in getattr(model, key)]
                    for key, relationship in mapper.relationships.items()
                    if relationship.direction == ONETOMANY
                }
            )
        elif isinstance(model, Sequence):
            cleaned = [self.model_encoder(value) for value in model]
        else:
            cleaned = model

        return jsonable_encoder(cleaned, **kwargs)
