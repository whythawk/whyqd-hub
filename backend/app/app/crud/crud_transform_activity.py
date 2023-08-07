from __future__ import annotations
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder

from app.crud.base import CRUDBase
from app.models import User, Subscription, TransformActivity
from app.schemas import TransformActivityCreate, TransformActivityUpdate
from app.crud.crud_product import product as crud_product
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
        if settings.USE_STRIPE and not user.is_superuser and not subscription.override:
            product = crud_product.get_by_subscription_type(db=db, subscription_type=subscription.subscription_type)
            # Will blow up if subscription is None
            if row_count > product.rows:
                e = f"Subscription row-limit ({product.rows}) exceeded (uploaded {row_count} rows)."
                raise ValueError(e)
            date_to = datetime.utcnow()
            date_from = date_to - timedelta(days=30)
            transform_count = user.transform_activities.filter(
                (TransformActivity.created >= date_from) & (TransformActivity.created <= date_to)
            ).count()
            if transform_count > product.transforms:
                e = f"Subscription transform-limit ({product.transforms}) exceeded."
                raise ValueError(e)
        obj_in = TransformActivityCreate(**{"rows": row_count, "data_import": data_import, "researcher_id": user.id})
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


transform_activity = CRUDTransformActivity(TransformActivity)
