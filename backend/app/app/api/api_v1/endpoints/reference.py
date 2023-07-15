from __future__ import annotations
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from whyqd.parsers.datasource import DataSourceParser

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=list[schemas.Reference])
def read_all_references(
    *,
    db: Session = Depends(deps.get_db),
    reference_type: Optional[schema_types.ReferenceType] = None,
    mime_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    skip: int = 0,
    limit: Optional[int] = settings.MULTI_MAX,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all schemas available for this researcher.
    """
    if mime_type:
        reader = DataSourceParser()
        try:
            mime_type = reader.get_mimetype(mimetype=mime_type)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=e,
            )
    return crud.reference.get_multi(
        db=db,
        user=current_user,
        reference_type=reference_type,
        mime_type=mime_type,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        skip=skip,
        limit=limit,
    )


@router.delete("/{id}", response_model=schemas.Reference)
def remove_reference(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a reference. Researcher must be a CUSTODIAN.
    """
    return crud.reference.remove(db=db, id=id, user=current_user)