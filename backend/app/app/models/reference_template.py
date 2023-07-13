from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import ForeignKey, Computed, Index
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy_utils import TSVectorType
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import ReferenceType, MimeType

if TYPE_CHECKING:
    from app.models.task import Task  # noqa: F401
    from app.models.role import Role  # noqa: F401


class ReferenceTemplate(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_private: Mapped[bool] = mapped_column(default=True)
    # METADATA
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
    # OF RESOURCE TYPE
    model: Mapped[UUID] = mapped_column(UUID(as_uuid=True), unique=True, nullable=False, index=True)
    model_type: Mapped[ENUM[ReferenceType]] = mapped_column(ENUM(ReferenceType), nullable=False, index=True)
    # OF DATA SOURCE MIME TYPE
    mime_type: Mapped[Optional[ENUM[MimeType]]] = mapped_column(ENUM(MimeType), nullable=True)
    # VERSION HISTORY
    older_id: Mapped[UUID] = mapped_column(ForeignKey("referencetemplate.id"), nullable=True)
    newer: Mapped["ReferenceTemplate"] = relationship(uselist=False, backref=backref("older", remote_side=[id]))
    version: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    # TASK RELATIONSHIPS
    datasource: Mapped[list["Task"]] = relationship(
        foreign_keys="[Task.datasource_id]", back_populates="datasource", lazy="dynamic"
    )
    crosswalk: Mapped[list["Task"]] = relationship(
        foreign_keys="[Task.crosswalk_id]", back_populates="crosswalk", lazy="dynamic"
    )
    # MEMBERS AND MEMBERSHIP MANAGEMENT
    auths: Mapped[list["Role"]] = relationship(
        back_populates="referencetemplate", cascade="all, delete", lazy="dynamic"
    )

    __table_args__ = (
        # Indexing the TSVector column
        Index("ix_referencetemplate_name_vector", name_vector, postgresql_using="gin"),
        Index("ix_referencetemplate_title_vector", title_vector, postgresql_using="gin"),
        Index("ix_referencetemplatek_description_vector", description_vector, postgresql_using="gin"),
    )
