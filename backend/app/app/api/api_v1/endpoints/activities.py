from __future__ import annotations
from typing import Any, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=list[schemas.Activity])
def read_all_researcher_activities(
    *,
    db: Session = Depends(deps.get_db),
    state: Optional[schema_types.StateType] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    alert: bool = False,
    custodian: bool = False,
    descending: bool = True,
    skip: int = 0,
    limit: Optional[int] = settings.MULTI_MAX,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all activity messages for this researcher.
    """
    return crud.activity.get_for_researcher(
        db=db,
        user=current_user,
        state=state,
        date_from=date_from,
        date_to=date_to,
        alert=alert,
        custodian=custodian,
        descending=descending,
        skip=skip,
        limit=limit,
    )
