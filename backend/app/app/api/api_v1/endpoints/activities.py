from __future__ import annotations
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/project/{project_id}", response_model=list[schemas.ResourceActivitySummary])
def read_all_project_resource_activities(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    match: Optional[str] = None,
    state: Optional[schema_types.StateType] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    alert: bool = False,
    excludeComplete: bool = True,
    prioritised: bool = True,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all resources and activity messages for a project available for this researcher.
    """
    project_obj = crud.project.get(db=db, id=project_id, user=current_user)
    if not project_obj:
        raise HTTPException(
            status_code=400,
            detail="Either project does not exist, or user does not have the rights for this request.",
        )
    return crud.resource.get_multi(
        db=db,
        user=current_user,
        project_obj=project_obj,
        match=match,
        state=state,
        date_from=date_from,
        date_to=date_to,
        alert=alert,
        excludeComplete=excludeComplete,
        prioritised=prioritised,
        page=page,
    )


@router.get("/task/{task_id}", response_model=list[schemas.ResourceActivitySummary])
def read_all_task_resource_activities(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    match: Optional[str] = None,
    state: Optional[schema_types.StateType] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    alert: bool = False,
    excludeComplete: bool = True,
    prioritised: bool = True,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all resources and activity messages for a task available for this researcher.
    """
    task_obj = crud.task.get(db=db, id=task_id, user=current_user)
    if not task_obj:
        raise HTTPException(
            status_code=400,
            detail="Either task does not exist, or user does not have the rights for this request.",
        )
    return crud.resource.get_multi(
        db=db,
        user=current_user,
        task_obj=task_obj,
        match=match,
        state=state,
        date_from=date_from,
        date_to=date_to,
        alert=alert,
        excludeComplete=excludeComplete,
        prioritised=prioritised,
        page=page,
    )


@router.get("/report", response_model=schemas.ReportData)
def read_report(
    *,
    db: Session = Depends(deps.get_db),
    project_id: Optional[str] = None,
    task_id: Optional[str] = None,
    frequency: Optional[schema_types.FrequencyType] = schema_types.FrequencyType.MONTH,
    state: Optional[schema_types.StateType] = schema_types.StateType.COMPLETE,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get activity report.
    """
    if not project_id and not task_id:
        raise HTTPException(
            status_code=400,
            detail="Either of Task or Project must be provided.",
        )
    task_obj = None
    project_obj = None
    if task_id:
        task_obj = crud.task.get(db=db, id=task_id, user=current_user)
        if not task_obj:
            raise HTTPException(
                status_code=400,
                detail="Either task does not exist, or user does not have the rights for this request.",
            )
    if project_id:
        project_obj = crud.project.get(db=db, id=project_id, user=current_user)
        if not project_obj:
            raise HTTPException(
                status_code=400,
                detail="Either project does not exist, or user does not have the rights for this request.",
            )
    return crud.resource.get_report(
        db=db,
        user=current_user,
        project_obj=project_obj,
        task_obj=task_obj,
        frequency=frequency,
        state=state,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/", response_model=list[schemas.ResourceActivitySummary])
def read_all_resource_activities(
    *,
    db: Session = Depends(deps.get_db),
    match: Optional[str] = None,
    state: Optional[schema_types.StateType] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    alert: bool = False,
    excludeComplete: bool = True,
    prioritised: bool = True,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all resources and activity messages for this researcher.
    """
    return crud.resource.get_multi(
        db=db,
        user=current_user,
        match=match,
        state=state,
        date_from=date_from,
        date_to=date_to,
        alert=alert,
        excludeComplete=excludeComplete,
        prioritised=prioritised,
        page=page,
    )
