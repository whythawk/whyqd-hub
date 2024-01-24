from __future__ import annotations
from typing import Any
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings

router = APIRouter()


class ByteSize(int):
    # https://stackoverflow.com/a/55659577
    _KB = 1024
    _suffixes = "B", "KB", "MB", "GB", "PB"

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        self.bytes = self.B = int(self)
        self.kilobytes = self.KB = self / self._KB**1
        self.megabytes = self.MB = self / self._KB**2
        self.gigabytes = self.GB = self / self._KB**3
        self.petabytes = self.PB = self / self._KB**4
        *suffixes, last = self._suffixes
        suffix = next((suffix for suffix in suffixes if 1 < getattr(self, suffix) < self._KB), last)
        self.readable = suffix, getattr(self, suffix)

        super().__init__()

    def __str__(self):
        return self.__format__(".2f")

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, super().__repr__())

    def __format__(self, format_spec):
        suffix, val = self.readable
        return "{val:{fmt}} {suf}".format(val=val, fmt=format_spec, suf=suffix)

    def __sub__(self, other):
        return self.__class__(super().__sub__(other))

    def __add__(self, other):
        return self.__class__(super().__add__(other))

    def __mul__(self, other):
        return self.__class__(super().__mul__(other))

    def __rsub__(self, other):
        return self.__class__(super().__sub__(other))

    def __radd__(self, other):
        return self.__class__(super().__add__(other))

    def __rmul__(self, other):
        return self.__class__(super().__rmul__(other))


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


@router.get("/working", response_model=schemas.Msg)
def read_working_directory_size(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get current working directory size.
    """
    working_size = ByteSize(sum(file.stat().st_size for file in Path(settings.WORKING_PATH).rglob("*")))
    return {"msg": str(working_size)}


@router.post("/working", response_model=schemas.Msg)
def clear_working_directory(
    *,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Clear current working directory.
    """
    crud.files.delete_working_directory()
    working_size = ByteSize(sum(file.stat().st_size for file in Path(settings.WORKING_PATH).rglob("*")))
    return {"msg": str(working_size)}
