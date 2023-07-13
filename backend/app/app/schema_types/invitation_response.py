from enum import auto

from app.schema_types.base import BaseEnum


class InvitationResponseType(BaseEnum):
    WAITING = auto()
    ACCEPTED = auto()
    REFUSED = auto()
