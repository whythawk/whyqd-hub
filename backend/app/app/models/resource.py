from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Computed, Index
from sqlalchemy_utils import TSVectorType
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ENUM
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import StateType

if TYPE_CHECKING:
    from app.models.reference import Reference  # noqa: F401
    from app.models.task import Task  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.activity import Activity  # noqa: F401


class Resource(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    is_private: Mapped[bool] = mapped_column(default=True)
    # METADATA
    name: Mapped[Optional[str]] = mapped_column(index=True, nullable=True)
    name_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("name", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"name\")", persisted=True),
    )
    title: Mapped[Optional[str]] = mapped_column(index=True, nullable=True)
    title_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("title", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"title\")", persisted=True),
        nullable=True,
    )
    description: Mapped[Optional[str]] = mapped_column(index=True, nullable=True)
    description_vector: Mapped[TSVectorType] = mapped_column(
        TSVectorType("description", regconfig="pg_catalog.simple"),
        Computed("to_tsvector('pg_catalog.simple', \"description\")", persisted=True),
        nullable=True,
    )
    sourceURL: Mapped[Optional[str]] = mapped_column(nullable=True)
    state: Mapped[ENUM[StateType]] = mapped_column(ENUM(StateType), nullable=False)
    # REFERENCE WORKFLOW
    # 1. source
    datasource_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True)
    datasource: Mapped[Optional["Reference"]] = relationship(back_populates="datasource", foreign_keys=[datasource_id])
    data_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True)
    data: Mapped[Optional["Reference"]] = relationship(back_populates="data", foreign_keys=[data_id])
    # 2. crosswalk
    schema_subject_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True
    )
    schema_subject: Mapped[Optional["Reference"]] = relationship(
        back_populates="schema_subjects", foreign_keys=[schema_subject_id]
    )
    crosswalk_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True)
    crosswalk: Mapped[Optional["Reference"]] = relationship(back_populates="crosswalks", foreign_keys=[crosswalk_id])
    schema_object_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True
    )
    schema_object: Mapped[Optional["Reference"]] = relationship(
        back_populates="schema_objects", foreign_keys=[schema_object_id]
    )
    # 3. destination
    transform_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True)
    transform: Mapped[Optional["Reference"]] = relationship(back_populates="transforms", foreign_keys=[transform_id])
    transformdata_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True
    )
    transformdata: Mapped[Optional["Reference"]] = relationship(
        back_populates="transformdata", foreign_keys=[transformdata_id]
    )
    transformdatasource_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True
    )
    transformdatasource: Mapped[Optional["Reference"]] = relationship(
        back_populates="transformdatasource", foreign_keys=[transformdatasource_id]
    )
    # TASK
    task_id: Mapped[Optional[UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey("task.id"), nullable=True)
    task: Mapped[Optional["Task"]] = relationship(back_populates="resources", foreign_keys=[task_id])
    # ACTIVITIES
    activities: Mapped[list["Activity"]] = relationship(
        back_populates="resource", cascade="all, delete", lazy="dynamic"
    )
    # MEMBERS AND MEMBERSHIP MANAGEMENT
    auths: Mapped[list["Role"]] = relationship(back_populates="resource", cascade="all, delete", lazy="dynamic")

    __table_args__ = (
        # Indexing the TSVector column
        Index("ix_resource_name_vector", name_vector, postgresql_using="gin"),
        Index("ix_resource_title_vector", title_vector, postgresql_using="gin"),
        Index("ix_resource_description_vector", description_vector, postgresql_using="gin"),
    )
