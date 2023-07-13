from __future__ import annotations
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy.sql import func

from app.db.base_class import Base
from app.schema_types import RoleType

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Token(Base):
    token: Mapped[str] = mapped_column(primary_key=True, index=True)
    authenticates_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    authenticates: Mapped["User"] = relationship(back_populates="refresh_tokens")


class OgunToken(Base):
    # Specifically for automated tasks ... managed independently by the user
    # Valid indefinitely, but can be revoked anytime
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    token: Mapped[str] = mapped_column(primary_key=True, index=True)
    authenticates_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    authenticates: Mapped["User"] = relationship(back_populates="ogun_tokens")
    # HAS RESPONSIBILITY
    responsibility: Mapped[ENUM[RoleType]] = mapped_column(ENUM(RoleType), nullable=False, default=RoleType.SEEKER)
