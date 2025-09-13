from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
import stripe

from app.crud.base import CRUDBase
from app.models import User, Order
from app.schemas import OrderCreate, OrderUpdate, OrderInDB
from app.schema_types import SubscriptionEventType
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY


"""
Order workflow:

1. Set customer id for purchaser

    crud.order.set_customer_id(db=db, user=current_user)

2. Generate individual PENDING orders for each subscriber (executed as a single checkout session by 'lines')

    for order_in in order_in_list:
        crud.order.create(db=db, obj_in=order_in)

3. If session completes: Convert checkout to subscription, and CREATED

    crud.order.set_pending_to_created(db=db, checkout_id=checkout_id, subscription_id=subscription_id)

4. If payment fails: Generate a 'FAILED' subscription (crud.subscription) but ONLY for the purchaser (customer id)

    crud.subscription.create(db=db, obj_in=subscription_in)

5. If payment succeeds:
    - Update order with charge id, and invoice url, and COMPLETED

    crud.order.set_created_to_completed(db=db, subscription_id=subscription_id, charge_id=charge_id, invoice_url=invoice_url)

    - Generate a 'RENEWED' subscription (crud.subscription)

        for subscription_in in subscription_in_list:
            crud.subscription.create(db=db, obj_in=subscription_in)
"""


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    def set_customer_id(self, db: Session, *, user: User) -> User:
        if user.customer_id:
            return user
        # If a member doesn't have a customer number, create one
        customer_id = stripe.Customer.create(
            email=user.email,
            name=user.full_name,
        )
        setattr(user, "customer_id", customer_id.id)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def set_pending_to_created(self, db: Session, *, checkout_id: str, subscription_id: str) -> Optional[Order]:
        db_obj = (
            db.query(self.model)
            .filter(
                and_(
                    self.model.checkout_id == checkout_id,
                    or_(
                        self.model.subscription_event_type == SubscriptionEventType.PENDING,
                        self.model.subscription_event_type == SubscriptionEventType.FAILED,
                    ),
                )
            )
            .first()
        )
        if not db_obj:
            return None
        setattr(db_obj, "subscription_id", subscription_id)
        setattr(db_obj, "subscription_event_type", SubscriptionEventType.CREATED)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_renewal_from_last_completed(
        self, db: Session, *, user: User, subscription_id: str, charge_id: str, invoice_url: str
    ) -> Optional[Order]:
        # This might be a renewal, so check if there are completed events for the same user
        db_obj = (
            user.orders.filter(self.model.subscription_event_type == SubscriptionEventType.COMPLETED)
            .order_by(self.model.created.desc())
            .first()
        )
        if not db_obj:
            return None
        # Rework the last order
        obj_in = OrderInDB.model_validate(db_obj).model_dump(exclude_unset=True)
        obj_in.pop("id", None)
        obj_in.pop("created", None)
        obj_in["subscription_id"] = subscription_id
        obj_in["subscription_event_type"] = SubscriptionEventType.CREATED
        obj_in = OrderCreate(**obj_in)
        # Create
        db_obj = self.create(db=db, obj_in=obj_in)
        # Update
        setattr(db_obj, "charge_id", charge_id)
        setattr(db_obj, "invoice_url", invoice_url)
        setattr(db_obj, "subscription_event_type", SubscriptionEventType.COMPLETED)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_created_to_completed(
        self, db: Session, *, subscription_id: str, charge_id: str, invoice_url: str
    ) -> Optional[Order]:
        db_obj = (
            db.query(self.model)
            .filter(
                and_(
                    self.model.subscription_id == subscription_id,
                    self.model.subscription_event_type == SubscriptionEventType.CREATED,
                )
            )
            .first()
        )
        if not db_obj:
            return None
        setattr(db_obj, "charge_id", charge_id)
        setattr(db_obj, "invoice_url", invoice_url)
        setattr(db_obj, "subscription_event_type", SubscriptionEventType.COMPLETED)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def set_pending_to_failed(self, db: Session, *, db_obj: Order, invoice_url: str) -> Order:
        setattr(db_obj, "subscription_event_type", SubscriptionEventType.FAILED)
        setattr(db_obj, "invoice_url", invoice_url)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_latest_pending_order_for_failed_payment(self, db: Session, *, user: User) -> Order:
        # For preference, we want the customer's own order. We only need one.
        db_obj = (
            db.query(self.model)
            .filter(
                and_(
                    self.model.payer_id == user.id,
                    self.model.subscription_event_type == SubscriptionEventType.PENDING,
                )
            )
            .order_by(desc("created"))
            .first()
        )
        return db_obj

    def get_latest_created_subscriptions(self, db: Session, *, id: str) -> Order:
        return (
            db.query(self.model)
            .filter(
                and_(self.model.checkout_id == id, self.model.subscription_event_type == SubscriptionEventType.CREATED)
            )
            .order_by(desc("created"))
            .first()
        )

    def get_multi_orders(self, db: Session, *, user: User, page: int = 0, page_break: bool = False) -> List[Order]:
        db_objs = user.orders.order_by(desc("created"), desc("subscription_type"))
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()


order = CRUDOrder(Order)
