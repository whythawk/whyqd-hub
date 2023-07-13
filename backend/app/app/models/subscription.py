from typing import TYPE_CHECKING, Optional
from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import SubscriptionType, SubscriptionEventType

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Subscription(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    # SUBSCRIPTION
    subscription_id: Mapped[str] = mapped_column(index=True)
    subscription_event_type: Mapped[ENUM[SubscriptionEventType]] = mapped_column(
        ENUM(SubscriptionEventType), nullable=False
    )
    subscription_type: Mapped[ENUM[SubscriptionType]] = mapped_column(ENUM(SubscriptionType), nullable=False)
    # DURATION
    started: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    ends: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    override: Mapped[bool] = mapped_column(default=False)  # admin-only, gives a member a perpetual membership
    # SUBSCRIBER
    subscriber_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    subscriber: Mapped["User"] = relationship(back_populates="subscriptions")
