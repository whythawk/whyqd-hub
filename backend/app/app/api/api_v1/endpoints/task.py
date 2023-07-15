from __future__ import annotations
from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/", response_model=List[schemas.Task])
def read_all_tasks(
    *,
    db: Session = Depends(deps.get_db),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    skip: int = 0,
    limit: Optional[int] = settings.MULTI_MAX,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all tasks available for this researcher.
    """
    return crud.task.get_multi(
        db=db,
        user=current_user,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        skip=skip,
        limit=limit,
    )


@router.get("/project/{project_id}", response_model=List[schemas.Task])
def read_all_project_tasks(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    skip: int = 0,
    limit: Optional[int] = settings.MULTI_MAX,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all tasks associated with a project available for this researcher.
    """
    project_obj = crud.project.get(db=db, id=project_id, user=current_user)
    if not project_obj:
        raise HTTPException(
            status_code=400,
            detail="Either project does not exist, or user does not have the rights for this request.",
        )
    return crud.task.get_multi(
        db=db,
        user=current_user,
        project_obj=project_obj,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        skip=skip,
        limit=limit,
    )


@router.post("/multi", response_model=List[schemas.Task])
def create_multiple_tasks(
    *,
    db: Session = Depends(deps.get_db),
    objs_in: List[schemas.TaskCreate],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create multiple tasks.
    """
    return crud.task.create_multi(db=db, objs_in=objs_in, user=current_user)


@router.get("/{id}", response_model=schemas.Task)
def get_task(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a task.
    """
    return crud.task.get(db=db, id=id, user=current_user)


@router.post("/", response_model=schemas.Task)
def create_task(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.TaskCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a task.
    """
    return crud.task.create(db=db, obj_in=obj_in, user=current_user)


@router.put("/{id}", response_model=schemas.Task)
def update_task(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.TaskUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a task.
    """
    return crud.task.update(db=db, id=id, obj_in=obj_in, user=current_user)


@router.delete("/{id}", response_model=schemas.Msg)
def remove_task(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    """
    Remove a task. Researcher must be a CUSTODIAN.
    """
    crud.task.remove(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.CUSTODIAN)
    return {"msg": "Task has been successfully removed."}


# @router.post("/{task_id}/resource/{resource_id}", response_model=schemas.Task)
# def add_resource(
#     *,
#     db: Session = Depends(deps.get_db),
#     task_id: str,
#     resource_id: str,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Add a resource to a task.
#     """
#     task_obj = crud.task.get(db=db, id=task_id, user=current_user, responsibility=schema_types.RoleType.CURATOR)
#     resource_obj = crud.resource.get(
#         db=db, id=resource_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
#     )
#     if not resource_obj or not task_obj:
#         raise HTTPException(
#             status_code=400,
#             detail="Either of task or resource do not exist, or user does not have the rights for this request.",
#         )
#     return crud.task.add_resource(db=db, db_obj=task_obj, resource_obj=resource_obj)


# @router.delete("/{task_id}/resource/{resource_id}", response_model=schemas.Task)
# def remove_resource(
#     *,
#     db: Session = Depends(deps.get_db),
#     task_id: str,
#     resource_id: str,
#     current_user: models.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """
#     Remove a resource from a task.
#     """
#     task_obj = crud.task.get(db=db, id=task_id, user=current_user, responsibility=schema_types.RoleType.CURATOR)
#     resource_obj = crud.resource.get(
#         db=db, id=resource_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
#     )
#     if not resource_obj or not task_obj:
#         raise HTTPException(
#             status_code=400,
#             detail="Either of task or resource do not exist, or user does not have the rights for this request.",
#         )
#     return crud.task.remove_resource(db=db, db_obj=task_obj, resource_obj=resource_obj)


@router.post("/{task_id}/template/{template_id}", response_model=schemas.Task)
def add_template(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    template_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a reference template to a task.
    """
    template_obj = crud.reference.get(
        db=db, id=template_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )  # Schema
    if not template_obj:
        template_obj = crud.referencetemplate.get(db=db, id=template_id, user=current_user)  # Crosswalk / DataSource
    if not template_obj:
        raise HTTPException(
            status_code=400,
            detail="Reference template does not exist, or user does not have the rights for this request.",
        )
    return crud.task.add_template(db=db, id=task_id, template_obj=template_obj, user=current_user)


@router.delete("/{task_id}/template/{template_id}", response_model=schemas.Task)
def remove_template(
    *,
    db: Session = Depends(deps.get_db),
    task_id: str,
    template_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a reference template from a task.
    """
    template_obj = crud.reference.get(
        db=db, id=template_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )  # Schema
    if not template_obj:
        template_obj = crud.referencetemplate.get(db=db, id=template_id, user=current_user)  # Crosswalk / DataSource
    if not template_obj:
        raise HTTPException(
            status_code=400,
            detail="Reference template does not exist, or user does not have the rights for this request.",
        )
    return crud.task.remove_template(db=db, id=task_id, template_type=template_obj.model_type, user=current_user)