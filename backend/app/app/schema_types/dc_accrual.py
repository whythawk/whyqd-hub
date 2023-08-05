from enum import auto

from app.schema_types.base import BaseEnum


class DCAccrualType(BaseEnum):
    DEPOSIT = auto()
    DONATION = auto()
    PURCHASE = auto()
    LOAN = auto()
    LICENSE = auto()
    ITEMCREATION = auto()
