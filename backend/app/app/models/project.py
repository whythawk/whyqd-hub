from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Final
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.associationproxy import AssociationProxy
from sqlalchemy import ForeignKey, String, Table, Column, Computed, Index
from sqlalchemy_utils import TSVectorType
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import DCAccrualType, DCFrequencyType, DCAccrualPolicyType

if TYPE_CHECKING:
    from app.models.reference import Reference  # noqa: F401
    from app.models.task import Task  # noqa: F401
    from app.models.invitation import Invitation  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.activity import Activity  # noqa: F401


class Project(Base):
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
    subject: Mapped[list[Subject]] = relationship(secondary=lambda: project_subject_table)
    subjects: AssociationProxy[list[str]] = association_proxy("subject", "term")
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
    accrualPolicy: Mapped[ENUM[DCAccrualPolicyType]] = mapped_column(ENUM(DCAccrualPolicyType), nullable=True)
    bibliographicCitation: Mapped[Optional[str]] = mapped_column(nullable=True)
    conformsTo: Mapped[Optional[str]] = mapped_column(nullable=True)
    # TEMPLATES
    schema_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True)
    schema: Mapped["Reference"] = relationship(back_populates="project_schema", foreign_keys=[schema_id])
    # TASKS AND ACTIVITIES
    tasks: Mapped[list["Task"]] = relationship(back_populates="project", lazy="dynamic")
    activities: Mapped[list["Activity"]] = relationship(back_populates="project", cascade="all, delete", lazy="dynamic")
    # MEMBERS AND MEMBERSHIP MANAGEMENT
    invitations: Mapped[list["Invitation"]] = relationship(
        back_populates="project", cascade="all, delete", lazy="dynamic"
    )
    auths: Mapped[list["Role"]] = relationship(back_populates="project", cascade="all, delete", lazy="dynamic")

    __table_args__ = (
        # Indexing the TSVector column
        Index("ix_project_name_vector", name_vector, postgresql_using="gin"),
        Index("ix_project_title_vector", title_vector, postgresql_using="gin"),
        Index("ix_project_description_vector", description_vector, postgresql_using="gin"),
    )


class Subject(Base):
    # Sort of but not quite: https://docs.sqlalchemy.org/en/20/_modules/examples/graphs/directed_graph.html
    # https://docs.sqlalchemy.org/en/20/orm/extensions/associationproxy.html
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    term: Mapped[str] = mapped_column(String(64))

    def __init__(self, term: str):
        self.term = term


project_subject_table: Final[Table] = Table(
    "project_subject",
    Base.metadata,
    Column("project_id", UUID(as_uuid=True), ForeignKey("project.id"), primary_key=True),
    Column("subject_id", UUID(as_uuid=True), ForeignKey("subject.id"), primary_key=True),
)
