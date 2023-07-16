from __future__ import annotations
from typing import Any, Optional, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import json
import whyqd as qd

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.get("/", response_model=List[schemas.Project])
def read_all_projects(
    *,
    db: Session = Depends(deps.get_db),
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    descending: bool = True,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all projects available for this researcher.
    """
    return crud.project.get_multi(
        db=db,
        user=current_user,
        date_from=date_from,
        date_to=date_to,
        descending=descending,
        page=page,
    )


@router.post("/multi", response_model=List[schemas.Project])
def create_multiple_projects(
    *,
    db: Session = Depends(deps.get_db),
    objs_in: List[schemas.ProjectCreate],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create multiple projects.
    """
    return crud.project.create_multi(db=db, objs_in=objs_in, user=current_user)


@router.get("/{id}", response_model=schemas.Project)
def get_project(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a project.
    """
    return crud.project.get(db=db, id=id, user=current_user)


@router.post("/", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    obj_in: schemas.ProjectCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a project.
    """
    return crud.project.create(db=db, obj_in=obj_in, user=current_user)


@router.put("/{id}", response_model=schemas.Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    obj_in: schemas.ProjectUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a project.
    """
    return crud.project.update(db=db, id=id, obj_in=obj_in, user=current_user)


@router.delete("/{id}", response_model=schemas.Msg)
def remove_project(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    """
    Remove a project. Researcher must be a CUSTODIAN.
    """
    crud.project.remove(db=db, id=id, user=current_user, responsibility=schema_types.RoleType.CUSTODIAN)
    return {"msg": "Project has been successfully removed."}


@router.post("/{project_id}/task/{task_id}", response_model=schemas.Project)
def add_task(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    task_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a task to a project.
    """
    project_obj = crud.project.get(
        db=db, id=project_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )
    task_obj = crud.task.get(db=db, id=task_id, user=current_user, responsibility=schema_types.RoleType.CURATOR)
    if not project_obj or not task_obj:
        raise HTTPException(
            status_code=400,
            detail="Either of project or task do not exist, or user does not have the rights for this request.",
        )
    return crud.project.add_task(db=db, db_obj=project_obj, task_obj=task_obj)


@router.post("/{project_id}/multi/{field_id}", response_model=schemas.Msg)
def create_multi_tasks_with_project(
    *,
    db: Session = Depends(deps.get_db),
    models_in: list[schemas.TaskCreate],
    project_id: str,
    field_id: str,
    ogun_token: models.User = Depends(deps.get_ogun_token),
) -> Any:
    """
    Create multiple tasks for a project, with a template crosswalk. This is an ogun task.
    """
    field_name = None
    if ogun_token.responsibility == schema_types.RoleType.CURATOR:
        project_obj = crud.project.get(
            db=db, id=project_id, user=ogun_token.authenticates, responsibility=schema_types.RoleType.CURATOR
        )
        if project_obj and project_obj.schema:
            schema_model = crud.reference.get_model(db_obj=project_obj.schema)
            schema_dfn = qd.SchemaDefinition(source=schema_model)
            field_name = schema_dfn.fields.get(name=UUID(field_id))
        if not project_obj or not field_name:
            raise HTTPException(
                status_code=400,
                detail="Either of project or field name, or user does not have the rights for this request.",
            )
    models_in = [json.loads(model_in.json(by_alias=True)) for model_in in models_in]
    celery_app.send_task(
        "app.worker.process_create_multi_tasks_from_project",
        args=[ogun_token.authenticates.id, project_id, models_in, field_id],
    )
    return {
        "msg": "New task list successfully imported. Check your activity log to see when they're ready to process further."
    }


@router.delete("/{project_id}/task/{task_id}", response_model=schemas.Project)
def remove_task(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    task_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a task from a project.
    """
    project_obj = crud.project.get(
        db=db, id=project_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )
    task_obj = crud.task.get(db=db, id=task_id, user=current_user, responsibility=schema_types.RoleType.CURATOR)
    if not project_obj or not task_obj:
        raise HTTPException(
            status_code=400,
            detail="Either of project or task do not exist, or user does not have the rights for this request.",
        )
    return crud.project.remove_task(db=db, db_obj=project_obj, task_obj=task_obj)


@router.post("/{project_id}/schema/{schema_id}", response_model=schemas.Project)
def add_schema(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    schema_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add a schema to a project.
    """
    project_obj = crud.project.get(
        db=db, id=project_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )
    schema_obj = crud.reference.get(
        db=db, id=schema_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )
    if not project_obj or not schema_obj or not schema_obj.model_type == schema_types.ReferenceType.SCHEMA:
        raise HTTPException(
            status_code=400,
            detail="Either of project or schema do not exist, or user does not have the rights for this request.",
        )
    return crud.project.add_schema(db=db, db_obj=project_obj, schema_obj=schema_obj, user=current_user)


@router.delete("/{project_id}/schema/{schema_id}", response_model=schemas.Project)
def remove_schema(
    *,
    db: Session = Depends(deps.get_db),
    project_id: str,
    schema_id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Remove a schema from a project.
    """
    project_obj = crud.project.get(
        db=db, id=project_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )
    schema_obj = crud.reference.get(
        db=db, id=schema_id, user=current_user, responsibility=schema_types.RoleType.CURATOR
    )
    if not project_obj or not schema_obj or not schema_obj.id == project_obj.schema.id:
        raise HTTPException(
            status_code=400,
            detail="Either of project or schema do not exist, or user does not have the rights for this request.",
        )
    return crud.project.remove_schema(db=db, db_obj=project_obj)
