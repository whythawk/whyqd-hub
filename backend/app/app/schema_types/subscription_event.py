from enum import auto

from app.schema_types import BaseEnum


class SubscriptionEventType(BaseEnum):
    PENDING = auto()
    CREATED = auto()
    COMPLETED = auto()
    RENEWED = auto()
    FAILED = auto()
    ENDED = auto()
