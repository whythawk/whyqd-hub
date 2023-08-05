from __future__ import annotations
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=list[schemas.ProductPricingView])
def read_products(*, db: Session = Depends(deps.get_db), code: schemas.IPCode) -> Any:
    """
    Retrieve products.
    """
    products = crud.price.get_by_ip(db=db, code=code)
    return products


@router.get("/all", response_model=list[schemas.Product])
def read_all_products(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get all products.
    """
    return crud.product.get_all(db=db)


@router.put("/all", response_model=list[schemas.Product])
def update_all_products(
    *,
    db: Session = Depends(deps.get_db),
    products_in: list[schemas.ProductUpdate],
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update the product list.
    """
    return crud.product.update_all(db=db, obj_list_in=products_in)
