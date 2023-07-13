from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Computed, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy_utils import TSVectorType
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import DCAccrualType, DCFrequencyType, DCAccrualPolicyType

if TYPE_CHECKING:
    from app.models.reference import Reference  # noqa: F401
    from app.models.reference_template import ReferenceTemplate  # noqa: F401
    from app.models.resource import Resource  # noqa: F401
    from app.models.project import Project  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.activity import Activity  # noqa: F401


class Task(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    is_private: Mapped[bool] = mapped_column(default=True)
    # SEARCH FIELDS
    name: Mapped[str] = mapped_column(index=True, nullable=False)
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
    # DUBLIN CORE
    frequency: Mapped[Optional[str]] = mapped_column(nullable=True)
    spatial: Mapped[Optional[str]] = mapped_column(nullable=True)
    temporalStart: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    temporalEnd: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    language: Mapped[str] = mapped_column(String(64), nullable=True)
    creator: Mapped[Optional[str]] = mapped_column(nullable=True)
    contributor: Mapped[Optional[str]] = mapped_column(nullable=True)
    publisher: Mapped[Optional[str]] = mapped_column(nullable=True)
    rights: Mapped[Optional[str]] = mapped_column(nullable=True)
    source: Mapped[Optional[str]] = mapped_column(nullable=True)
    accessRights: Mapped[Optional[str]] = mapped_column(nullable=True)
    accrualMethod: Mapped[ENUM[DCAccrualType]] = mapped_column(ENUM(DCAccrualType), nullable=True)
    accrualPeriodicity: Mapped[ENUM[DCFrequencyType]] = mapped_column(ENUM(DCFrequencyType), nullable=True)
    accrualPriority: Mapped[Optional[int]] = mapped_column(nullable=True)
    accrualPolicy: Mapped[ENUM[DCAccrualPolicyType]] = mapped_column(ENUM(DCAccrualPolicyType), nullable=True)
    bibliographicCitation: Mapped[Optional[str]] = mapped_column(nullable=True)
    conformsTo: Mapped[Optional[str]] = mapped_column(nullable=True)
    # TEMPLATES
    datasource_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("referencetemplate.id"), nullable=True
    )
    datasource: Mapped[Optional["ReferenceTemplate"]] = relationship(
        back_populates="datasource", foreign_keys=[datasource_id]
    )
    crosswalk_id: Mapped[Optional[UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("referencetemplate.id"), nullable=True
    )
    crosswalk: Mapped[Optional["ReferenceTemplate"]] = relationship(
        back_populates="crosswalk", foreign_keys=[crosswalk_id]
    )
    schema_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True)
    schema: Mapped["Reference"] = relationship(back_populates="task_schema", foreign_keys=[schema_id])
    # PROJECT
    project_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=True)
    project: Mapped["Project"] = relationship(back_populates="tasks", foreign_keys=[project_id])
    # RESOURCES AND ACTIVITIES
    resources: Mapped[list["Resource"]] = relationship(back_populates="task", lazy="dynamic")
    activities: Mapped[list["Activity"]] = relationship(back_populates="task", cascade="all, delete", lazy="dynamic")
    # MEMBERS AND MEMBERSHIP MANAGEMENT
    auths: Mapped[list["Role"]] = relationship(back_populates="task", cascade="all, delete", lazy="dynamic")

    __table_args__ = (
        # Indexing the TSVector column
        # https://stackoverflow.com/questions/13361161/sqlalchemy-with-postgresql-and-full-text-search/73999486#73999486
        # https://sqlalchemy-utils.readthedocs.io/en/latest/data_types.html#module-sqlalchemy_utils.types.ts_vector
        # https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#full-text-search
        Index("ix_task_name_vector", name_vector, postgresql_using="gin"),
        Index("ix_task_title_vector", title_vector, postgresql_using="gin"),
        Index("ix_task_description_vector", description_vector, postgresql_using="gin"),
    )
