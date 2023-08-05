from enum import auto

from app.schema_types import BaseEnum


class SubscriptionType(BaseEnum):
    REVIEWER = auto()
    EXPLORER = auto()
    RESEARCHER = auto()
    INVESTIGATOR = auto()

    def describe(self):
        description = {
            "REVIEWER": "Perfect for those wanting to try us out.",
            "EXPLORER": "Formulate your data practice and develop your methods.",
            "RESEARCHER": "Deliver the foundation of your research data input.",
            "INVESTIGATOR": "Conduct repeated and long-term longitudinal studies.",
        }
        return description[self.value]
