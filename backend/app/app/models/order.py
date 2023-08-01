from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, DateTime, String
from sqlalchemy.dialects.postgresql import UUID, ENUM
from sqlalchemy.sql import func
from uuid import uuid4

from app.db.base_class import Base
from app.schema_types import SubscriptionType, SubscriptionEventType, CurrencyType

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class Order(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    subscription_event_type: Mapped[ENUM[SubscriptionEventType]] = mapped_column(
        ENUM(SubscriptionEventType), nullable=False
    )
    subscription_type: Mapped[ENUM[SubscriptionType]] = mapped_column(ENUM(SubscriptionType), nullable=False)
    currency: Mapped[ENUM[CurrencyType]] = mapped_column(ENUM(CurrencyType), nullable=False)
    amount: Mapped[int]
    checkout_id: Mapped[str] = mapped_column(index=True, nullable=True)
    subscription_id: Mapped[str] = mapped_column(index=True, nullable=True)
    charge_id: Mapped[str] = mapped_column(nullable=True)
    invoice_url: Mapped[str] = mapped_column(nullable=True)
    country_code: Mapped[str] = mapped_column(String(3), nullable=True)
    country_name: Mapped[str] = mapped_column(nullable=True)
    product_id: Mapped[str] = mapped_column(index=True)
    price_id: Mapped[str]
    # https://docs.sqlalchemy.org/en/14/orm/join_conditions.html#handling-multiple-join-paths
    payer_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"))
    payer: Mapped["User"] = relationship(back_populates="orders")
