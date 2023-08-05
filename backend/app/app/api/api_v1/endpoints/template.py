from __future__ import annotations
from typing import Any, Optional, List, Union

from fastapi import APIRouter, Depends  # , HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.ReferenceTemplate])
def read_all_templates(
    *,
    db: Session = Depends(deps.get_db),
    template_type: Optional[schema_types.ReferenceType] = None,
    descending: bool = True,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all templates available for this researcher.
    """
    return crud.referencetemplate.get_multi(
        db=db,
        user=current_user,
        reference_type=template_type,
        descending=descending,
        page=page,
    )


@router.get("/{id}", response_model=Union[schemas.DataSourceTemplateModel, schemas.CrosswalkTemplateModel])
def get_template_model(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get a template model.
    """
    return crud.referencetemplate.get_model(db=db, id=id, user=current_user)


@router.post("/{template_type}", response_model=schemas.ReferenceTemplate)
def create_template(
    *,
    db: Session = Depends(deps.get_db),
    template_in: Union[schemas.DataSourceTemplateModel, schemas.CrosswalkTemplateModel],
    template_type: schema_types.ReferenceType,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a template.
    """
    return crud.referencetemplate.create(
        db=db, template_in=template_in, reference_type=template_type, user=current_user
    )


@router.put("/{id}", response_model=schemas.ReferenceTemplate)
def update_template(
    *,
    db: Session = Depends(deps.get_db),
    id: str,
    template_in: Union[schemas.DataSourceTemplateModel, schemas.CrosswalkTemplateModel],
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a template.
    """
    return crud.referencetemplate.update(db=db, id=id, template_in=template_in, user=current_user)


@router.delete("/{id}", response_model=schemas.ReferenceTemplate)
def remove_template(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    """
    Remove a template. Researcher must be a CUSTODIAN.
    """
    return crud.referencetemplate.remove(
        db=db, id=id, user=current_user, responsibility=schema_types.RoleType.CUSTODIAN
    )
