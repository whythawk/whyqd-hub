from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ENUM
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import RoleType

if TYPE_CHECKING:
    from app.models.token import Token, OgunToken  # noqa: F401
    from app.models.invitation import Invitation  # noqa: F401
    from app.models.role import Role  # noqa: F401
    from app.models.activity import Activity  # noqa: F401
    from app.models.order import Order  # noqa: F401
    from app.models.subscription import Subscription  # noqa: F401


class User(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    modified: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
        nullable=False,
    )
    # METADATA
    full_name: Mapped[Optional[str]] = mapped_column(index=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[Optional[str]] = mapped_column(nullable=True)
    # AUTHENTICATION AND PERSISTENCE
    totp_secret: Mapped[Optional[str]] = mapped_column(nullable=True)
    totp_counter: Mapped[Optional[int]] = mapped_column(nullable=True)
    email_validated: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    refresh_tokens: Mapped[list["Token"]] = relationship(
        foreign_keys="[Token.authenticates_id]", back_populates="authenticates", lazy="dynamic"
    )
    # API MANAGEMENT
    ogun_tokens: Mapped[list["OgunToken"]] = relationship(
        foreign_keys="[OgunToken.authenticates_id]", back_populates="authenticates", lazy="dynamic"
    )
    ogun_users: Mapped[list["OgunUser"]] = relationship(
        foreign_keys="[OgunUser.authorises_id]", back_populates="authorises", lazy="dynamic"
    )
    # https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#handling-multiple-join-paths
    # PROJECT MANAGEMENT AND RESPONSIBILITIES
    roles: Mapped[list["Role"]] = relationship(back_populates="researcher", cascade="all, delete", lazy="dynamic")
    invitations: Mapped[list["Invitation"]] = relationship(
        back_populates="sender", cascade="all, delete", lazy="dynamic"
    )
    activities: Mapped[list["Activity"]] = relationship(back_populates="researcher", lazy="dynamic")
    # SUBSCRIPTIONS AND PAYMENTS
    customer_id: Mapped[str] = mapped_column(unique=True, index=True, nullable=True)
    orders: Mapped[list["Order"]] = relationship(foreign_keys="Order.payer_id", back_populates="payer", lazy="dynamic")
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="subscriber", cascade="all, delete", lazy="dynamic"
    )


class OgunUser(Base):
    # API access for ogun-token CRUD operations
    # Limited by the maximum responsibility it can assign
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    access_key: Mapped[UUID] = mapped_column(UUID(as_uuid=True), unique=True, index=True, nullable=False)
    secret_key: Mapped[str] = mapped_column(nullable=False)
    authorises_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    authorises: Mapped["User"] = relationship(back_populates="ogun_users")
    # HAS RESPONSIBILITY - CAN ONLY CREATE OGUN TOKENS OF THIS RESPONSIBILITY
    responsibility: Mapped[ENUM[RoleType]] = mapped_column(ENUM(RoleType), nullable=False, default=RoleType.SEEKER)
