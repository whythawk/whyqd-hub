from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.schema_types import SubscriptionType, CurrencyType


class Product(Base):
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    subscription: Mapped[ENUM[SubscriptionType]] = mapped_column(ENUM(SubscriptionType), nullable=False)
    prices: Mapped["Price"] = relationship(back_populates="product", cascade="all, delete, delete-orphan")


class Price(Base):
    id: Mapped[str] = mapped_column(primary_key=True, index=True)
    currency: Mapped[ENUM[CurrencyType]] = mapped_column(ENUM(CurrencyType), nullable=False)
    per_annum: Mapped[int]
    per_month: Mapped[int]
    product_id: Mapped[str] = mapped_column(String, ForeignKey("product.id"), nullable=True)
    product: Mapped["Product"] = relationship(back_populates="prices", passive_deletes=True)
