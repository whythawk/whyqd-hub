from enum import auto

from app.schema_types.base import BaseEnum


class DCAccrualPolicyType(BaseEnum):
    CLOSED = auto()
    PASSIVE = auto()
    ACTIVE = auto()
    PARTIAL = auto()

    def describe(self):
        description = {
            "CLOSED": "A policy that items are no longer added to the collection.",
            "PASSIVE": "A policy that items are added to the collection only in response to the initiative of an external agent.",
            "ACTIVE": "A policy that items are actively sought for addition to the collection.",
            "PARTIAL": "A policy that items are actively sought for addition to a specific part of the collection.",
        }
        return description[self.value]
