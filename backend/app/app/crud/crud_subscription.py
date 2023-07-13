from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
import stripe

from app.crud.base import CRUDBase
from app.models import User, Subscription
from app.schemas import SubscriptionCreate, SubscriptionUpdate
from app.schema_types import SubscriptionType
from app.core.config import settings

stripe.api_key = settings.STRIPE_API_KEY


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    def current(self, user: User) -> Subscription:
        expires = datetime.utcnow() - timedelta(days=1)  # 1 day grace
        return (
            user.subscriptions.filter(or_(self.model.ends > expires, self.model.override.is_(True)))
            .order_by(self.model.created.desc())
            .first()
        )

    def within_row_limit(self, *, user: User, row_count: int, raise_error: bool = False) -> bool:
        if user.is_superuser or not settings.USE_STRIPE:
            return True
        response = False
        subscription = self.current(user)
        if subscription:
            response = subscription.row_limit >= row_count
        if not response and raise_error:
            e = f"Subscription row-limit exceeded (uploaded {row_count} rows)."
            if subscription:
                e = f"Subscription row-limit ({subscription.row_limit}) exceeded (uploaded {row_count} rows)."
            raise ValueError(e)
        return response

    def has_appropriate_membership(
        self, user: User, membership_in: List[SubscriptionType], raise_error: bool = False
    ) -> bool:
        if user.is_superuser:
            return True
        response = False
        subscription = self.current(user)
        if subscription.subscription_type in membership_in:
            response = True
        if not response and raise_error:
            e = f"Subscription membership is {subscription.subscription_type} and needs to be higher."
            raise ValueError(e)
        return response

    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Subscription]:
        # https://stackoverflow.com/questions/41079196/using-sqlalchemy-how-do-i-get-last-inventory-entry-with-distinct-values-for-prod
        subquery = (
            db.query(self.model.subscriber_id, func.max(self.model.created).label("created")).group_by(
                self.model.subscriber_id,
            )
        ).subquery("subquery")
        return (
            db.query(self.model)
            .join(
                subquery,
                and_(
                    subquery.c.subscriber_id == self.model.subscriber_id,
                    subquery.c.created == self.model.created,
                ),
            )
            .order_by(self.model.created.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


subscription = CRUDSubscription(Subscription)
