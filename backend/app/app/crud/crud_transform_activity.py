from __future__ import annotations
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models import User, Subscription, TransformActivity
from app.schemas import TransformActivityCreate, TransformActivityUpdate
from app.core.config import settings


class CRUDTransformActivity(CRUDBase[TransformActivity, TransformActivityCreate, TransformActivityUpdate]):
    def create(
        self,
        db: Session,
        *,
        user: User,
        row_count: int,
        data_import: bool = True,
        subscription: Subscription | None = None,
    ) -> TransformActivity:
        if settings.USE_STRIPE and not user.is_superuser:
            # Will blow up if subscription is None
            if subscription.rows >= row_count:
                e = f"Subscription row-limit ({subscription.rows}) exceeded (uploaded {row_count} rows)."
                raise ValueError(e)
            date_to = datetime.utcnow()
            date_from = date_to - timedelta(days=30)
            transform_count = user.transform_activities.filter(
                (TransformActivity.created >= date_from) & (TransformActivity.created <= date_to)
            ).count()
            if subscription.transforms >= transform_count:
                e = f"Subscription transform-limit ({subscription.transforms}) exceeded."
                raise ValueError(e)
        obj_in = TransformActivityCreate(**{"rows": row_count, "data_import": data_import, "researcher_id": user.id})
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


transform_activity = CRUDTransformActivity(TransformActivity)
