from __future__ import annotations
from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.get("/", response_model=List[schemas.Resource])
def read_all_resources(
    *,
    db: Session = Depends(deps.get_db),
    match: Optional[str] = None,
    state: Optional[schema_types.StateType] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all resources available for this researcher.
    """
    return crud.resource.get_multi(
        db=db,
        user=current_user,
        match=match,
        state=state,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        page=page,
    )


@router.get("/task/{task_id}", response_model=List[schemas.Resource])
def read_all_task_resources(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    match: Optional[str] = None,
    state: Optional[schema_types.StateType] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all resources available for this researcher.
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
        descending=descending,
        page=page,
    )


@router.get("/{id}", response_model=schemas.ResourceManager)
def get_resource(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a resource.
    """
    return crud.reference.get_resource_manager(
        db=db, id=id, user=current_user, responsibility=schema_types.RoleType.SEEKER
    )


@router.get("/template/{id}", response_model=schemas.DataSourceTemplateModel)
def get_resource_source_template(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get the source template for a resource.
    """
    resource_obj = crud.resource.get(db=db, id=id, user=current_user)
    if not resource_obj:
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    return crud.reference.get_model(db_obj=resource_obj.datasource)


@router.post("/{id}/schema/{term_id}", response_model=schemas.ResourceManager)
def add_schema_object_to_resource(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    term_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a schema object to a resource and run a task to check for any potential crosswalks.
    """
    resource_obj = crud.resource.get(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.WRANGLER)
    schema_obj = crud.reference.get(db=db, id=term_id, user=current_user)
    if (
        not resource_obj
        or not resource_obj.schema_subject_id
        or not schema_obj
        or not schema_obj.model_type == schema_types.ReferenceType.SCHEMA
    ):
        raise HTTPException(
            status_code=400,
            detail="Either resource or schema do not exist, or user does not have the rights for this request.",
        )
    resource_obj = crud.reference.add_resource_schema_object(
        db=db, db_obj=resource_obj, schema_obj=schema_obj, user=current_user
    )
    if not resource_obj.crosswalk_id:
        resource_obj = crud.reference.add_new_resource_crosswalk(db=db, db_obj=resource_obj, user=current_user)
    return resource_obj


@router.post("/{id}/categorise/{field_id}/{term_type}", response_model=schemas.Msg)
def create_resource_schema_categorisation_as_terms(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    field_id: str,
    term_type: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Extract categories from source data as unique terms or as boolean Trues for a specific schema subject field.
    """
    resource_obj = crud.resource.get(db=db, id=id, user=current_user)
    if not resource_obj or term_type not in ["term", "boolean"]:
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    celery_app.send_task(
        "app.worker.process_schema_categorisation", args=[current_user.id, resource_obj.id, field_id, term_type]
    )
    return {"msg": "Field categorisation processing. Check your activity log to see when complete."}


@router.post("/{id}/transform/{mimetype}", response_model=schemas.Msg)
def process_resource_transform(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    mimetype: str,
    current_user: models.User = Depends(deps.get_subscribed_user),
) -> Any:
    """
    Process resource transform to complete a crosswalk.
    """
    resource_obj = crud.resource.get(db=db, id=id, user=current_user)
    if (
        not resource_obj
        or not resource_obj.state == schema_types.StateType.TRANSFORM_READY
        or not resource_obj.crosswalk_id
    ):
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    celery_app.send_task("app.worker.process_transform", args=[current_user.id, resource_obj.id, mimetype])
    return {"msg": "Transformation processing. Check your activity log to see when complete."}


@router.delete("/{id}", response_model=schemas.Msg)
def remove_resource(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    """
    Remove a resource. Researcher must be a CUSTODIAN.
    """
    crud.resource.remove(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.CUSTODIAN)
    return {"msg": "Resource has been successfully removed."}


@router.delete("/transform/{id}", response_model=schemas.ResourceManager)
def remove_resource_transform(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a transform and update a resource. Researcher must be a WRANGLER or more.
    """
    resource_obj = crud.resource.get(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.WRANGLER)
    if resource_obj:
        # Need to delete transform, transformdata and transformdatasource, and unreference the crosswalk (it may be
        # used elsewhere)
        resource_obj = crud.reference.remove_resource_transform(db=db, db_obj=resource_obj, user=current_user)
    if not resource_obj:
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    return crud.reference.get_resource_manager(db=db, id=id, user=current_user)


@router.delete("/crosswalk/{id}", response_model=schemas.ResourceManager)
def remove_resource_crosswalk(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a transform and update a resource. Researcher must be a WRANGLER or more.
    """
    resource_obj = crud.resource.get(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.WRANGLER)
    if resource_obj:
        resource_obj = crud.reference.remove_resource_crosswalk(db=db, db_obj=resource_obj, user=current_user)
    if not resource_obj:
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    return crud.reference.get_resource_manager(db=db, id=id, user=current_user)


@router.delete("/schema/{id}", response_model=schemas.ResourceManager)
def remove_resource_schema(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a transform and update a resource. Researcher must be a WRANGLER or more.
    """
    resource_obj = crud.resource.get(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.WRANGLER)
    if resource_obj:
        resource_obj = crud.reference.remove_resource_schema_object(db=db, db_obj=resource_obj, user=current_user)
    if not resource_obj:
        raise HTTPException(
            status_code=400,
            detail="Either resource does not exist, or user does not have the rights for this request.",
        )
    return crud.reference.get_resource_manager(db=db, id=id, user=current_user)
