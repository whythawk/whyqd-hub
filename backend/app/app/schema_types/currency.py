from enum import auto

from app.schema_types.base import BaseEnum


class CurrencyType(BaseEnum):
    USD = auto()
    GBP = auto()
    EUR = auto()

    def describe(self):
        description = {"USD": "$", "GBP": "£", "EUR": "€"}
        return description[self.value]
