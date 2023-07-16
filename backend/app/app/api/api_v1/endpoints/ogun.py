from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas, schema_types
from app.api import deps
from app.core import security

router = APIRouter()

"""
Ogun users and API token are issued by specific researchers for programmatic use:
  - Requires user to have a password enabled
  - Ogun users can be created or deleted, but not updated, and must have a maximum Role limit (never Custodian)
  - Ogun's issue API tokens and can rotate them - these perpetual tokens can be used to perform tasks
  - Dashboard to delete tasks
  - User must be active for Ogun user to operate
"""


@router.get("/", response_model=List[schemas.OgunUser])
def read_all_terms(
    *,
    page: int = 0,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve all current ogun users for a user.
    """
    return crud.ogun.get_multi(user=current_user, page=page)


@router.post("/create/{role}", response_model=schemas.OgunUserCreate)
def create_ogun_user(
    *,
    db: Session = Depends(deps.get_db),
    role: str,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new Ogun user.
    """
    if not crud.user.has_password(user=current_user):
        raise HTTPException(status_code=400, detail="Creation failed. User must have an account password.")
    try:
        role = schema_types.RoleType(role)
        if role == schema_types.RoleType.CUSTODIAN:
            raise ValueError
    except ValueError:
        raise HTTPException(status_code=400, detail="Creation failed. Ogun must have a valid role.")
    obj_in = schemas.OgunUserCreate(**{"authorises_id": current_user.id, "responsibility": role})
    crud.ogun.create(db=db, obj_in=obj_in)
    return obj_in


@router.delete("/{id}", response_model=schemas.Msg)
def remove_ogun_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    """
    Remove an Ogun. Researcher must be a CUSTODIAN.
    """
    crud.ogun.remove(db=db, user=current_user, access_key=id)
    return {"msg": "Key has been successfully removed."}


@router.post("/oauth", response_model=schemas.Token)
def login_with_oauth2(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    First step with OAuth2 compatible token login, get an access token for future requests.
    """
    print(form_data.username, form_data.password)
    ogun = crud.ogun.authenticate(db, access_key=form_data.username, password=form_data.password)
    if not ogun or not crud.user.is_active(ogun.authorises):
        raise HTTPException(status_code=400, detail="Login failed; incorrect access key or password")
    refresh_token = security.create_ogun_token(subject=ogun.authorises.id)
    crud.oguntoken.create(db=db, obj_in=refresh_token, user_obj=ogun.authorises, responsibility=ogun.responsibility)
    return {
        "access_token": refresh_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(
    db: Session = Depends(deps.get_db),
    ogun_token: models.OgunToken = Depends(deps.get_ogun_token),
) -> Any:
    """
    Refresh tokens for future requests
    """
    new_token = security.create_ogun_token(subject=ogun_token.authenticates.id)
    crud.oguntoken.create(
        db=db, obj_in=new_token, user_obj=ogun_token.authenticates, responsibility=ogun_token.responsibility
    )
    crud.oguntoken.remove(db=db, db_obj=ogun_token)
    return {
        "access_token": new_token,
        "refresh_token": new_token,
        "token_type": "bearer",
    }


@router.post("/revoke", response_model=schemas.Msg)
def revoke_token(
    db: Session = Depends(deps.get_db),
    ogun_token: models.OgunToken = Depends(deps.get_ogun_token),
) -> Any:
    """
    Revoke an ogun token
    """
    crud.oguntoken.remove(db=db, db_obj=ogun_token)
    return {"msg": "Token revoked"}
