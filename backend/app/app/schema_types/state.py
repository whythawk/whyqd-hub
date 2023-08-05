from enum import auto

from app.schema_types.base import BaseEnum


class StateType(BaseEnum):
    BUSY = auto()
    READY = auto()
    DATA_READY = auto()
    SCHEMA_READY = auto()
    CROSSWALK_READY = auto()
    TRANSFORM_READY = auto()
    IMPORT_ERROR = auto()
    DATA_ERROR = auto()
    SCHEMA_ERROR = auto()
    CROSSWALK_ERROR = auto()
    TRANSFORM_ERROR = auto()
    ERROR = auto()
    COMPLETE = auto()

    def describe(self):
        description = {
            "BUSY": "Performing an assigned task.",
            "READY": "No specific state. Waiting for assignment.",
            "DATA_READY": "Source data imported and ready for modelling.",
            "SCHEMA_READY": "Schema model ready for application.",
            "CROSSWALK_READY": "Crosswalk validated and ready for application.",
            "TRANSFORM_READY": "Transform validated and ready for implementation.",
            "IMPORT_ERROR": "Source data import failed.",
            "DATA_ERROR": "Source data modelling failed.",
            "SCHEMA_ERROR": "Schema modelling failed.",
            "CROSSWALK_ERROR": "Crosswalk validation failed.",
            "TRANSFORM_ERROR": "Data transformation failed.",
            "ERROR": "An unclassified error occured.",
            "COMPLETE": "Data transformation complete.",
        }
        return description[self.value]
