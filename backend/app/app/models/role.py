from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import RoleType

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.project import Project  # noqa: F401
    from app.models.task import Task  # noqa: F401
    from app.models.resource import Resource  # noqa: F401
    from app.models.reference import Reference  # noqa: F401
    from app.models.reference_template import ReferenceTemplate  # noqa: F401


class Role(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # WHO
    researcher_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    researcher: Mapped["User"] = relationship(back_populates="roles")
    is_validated: Mapped[bool] = mapped_column(default=False)
    # HAS RESPONSIBILITY
    responsibility: Mapped[ENUM[RoleType]] = mapped_column(ENUM(RoleType), nullable=False, default=RoleType.SEEKER)
    # FOR
    project_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=True)
    project: Mapped["Project"] = relationship(back_populates="auths")
    task_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("task.id"), nullable=True)
    task: Mapped["Task"] = relationship(back_populates="auths")
    resource_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resource.id"), nullable=True)
    resource: Mapped["Resource"] = relationship(back_populates="auths")
    reference_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("reference.id"), nullable=True)
    reference: Mapped["Reference"] = relationship(back_populates="auths")
    referencetemplate_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("referencetemplate.id"), nullable=True
    )
    referencetemplate: Mapped["ReferenceTemplate"] = relationship(back_populates="auths")
