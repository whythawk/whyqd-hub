from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401
    from app.models.resource import Resource  # noqa: F401
    from app.models.task import Task  # noqa: F401
    from app.models.project import Project  # noqa: F401


class Activity(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # MESSAGE CONTENT
    message: Mapped[str] = mapped_column(nullable=False)
    custodians_only: Mapped[bool] = mapped_column(default=False)
    alert: Mapped[bool] = mapped_column(default=False)
    # WHO
    researcher_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    researcher: Mapped["User"] = relationship(back_populates="activities", foreign_keys=[researcher_id])
    # SOURCE OF ACTIVITY
    resource_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resource.id"), nullable=True)
    resource: Mapped["Resource"] = relationship(back_populates="activities", foreign_keys=[resource_id])
    task_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("task.id"), nullable=True)
    task: Mapped["Task"] = relationship(back_populates="activities", foreign_keys=[task_id])
    project_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("project.id"), nullable=True)
    project: Mapped["Project"] = relationship(back_populates="activities", foreign_keys=[project_id])
