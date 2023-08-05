from __future__ import annotations
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta

from app.crud.base import CRUDBase
from app.models import User, Subscription
from app.schemas import SubscriptionCreate, SubscriptionUpdate
from app.schema_types import SubscriptionType
from app.crud.crud_transform_activity import transform_activity as crud_transform_activity
from app.core.config import settings


class CRUDSubscription(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    def current(self, user: User) -> Subscription:
        expires = datetime.utcnow() - timedelta(days=1)  # 1 day grace
        return (
            user.subscriptions.filter(or_(self.model.ends > expires, self.model.override.is_(True)))
            .order_by(self.model.created.desc())
            .first()
        )

    def within_limits(self, db: Session, *, user: User, row_count: int, data_import: bool = True) -> bool:
        # create a transform record
        subscription = self.current(user)
        crud_transform_activity.create(
            db=db, user=user, row_count=row_count, data_import=data_import, subscription=subscription
        )
        # Will raise a ValueError if creation fails
        return True

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

    def get_multi(self, db: Session, *, page: int = 0, page_break: bool = False) -> List[Subscription]:
        # https://stackoverflow.com/questions/41079196/using-sqlalchemy-how-do-i-get-last-inventory-entry-with-distinct-values-for-prod
        subquery = (
            db.query(self.model.subscriber_id, func.max(self.model.created).label("created")).group_by(
                self.model.subscriber_id,
            )
        ).subquery("subquery")
        db_objs = (
            db.query(self.model)
            .join(
                subquery,
                and_(
                    subquery.c.subscriber_id == self.model.subscriber_id,
                    subquery.c.created == self.model.created,
                ),
            )
            .order_by(self.model.created.desc())
        )
        if not page_break:
            if page > 0:
                db_objs = db_objs.offset(page * settings.MULTI_MAX)
            db_objs = db_objs.limit(settings.MULTI_MAX)
        return db_objs.all()


subscription = CRUDSubscription(Subscription)
