from enum import auto

from app.schema_types.base import BaseEnum


class ReferenceType(BaseEnum):
    DATASOURCE = auto()
    DATA = auto()
    SCHEMA = auto()
    CROSSWALK = auto()
    TRANSFORM = auto()

    def describe(self):
        description = {
            "DATASOURCE": "A tabular source data file of a specified MIMETYPE.",
            "DATA": "A data model defining a data source",
            "SCHEMA": "A schema model defining a data structure and its fields and field-constraints.",
            "CROSSWALK": "A crosswalk model defining the relationship between a source- and destination schema model.",
            "TRANSFORM": "A transformation model defining the crosswalk between source- and destination data models.",
        }
        return description[self.value]
