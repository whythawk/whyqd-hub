from enum import auto

from app.schema_types import BaseEnum


class RoleType(BaseEnum):
    CUSTODIAN = auto()
    CURATOR = auto()
    WRANGLER = auto()
    SEEKER = auto()

    def describe(self):
        description = {
            "CUSTODIAN": "A person with administrative and management responsibility for a resource. Can create and manage teams and resources.",
            "CURATOR": "A person with architecture and quality responsibility for a resource.",
            "WRANGLER": "A person with responsibility for implementing a data wrangling process.",
            "SEEKER": "A person, or process, which can view, but not modify, existing resources.",
        }
        return description[self.value]
