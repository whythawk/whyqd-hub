from app.schema_types.base import BaseEnum


class DCFrequencyType(BaseEnum):
    TRIENNIAL = "triennial"
    BIENNIAL = "biennial"
    ANNUAL = "annual"
    SEMIANNUAL = "semiannual"
    THREETIMESAYEAR = "threeTimesAYear"
    QUARTERLY = "quarterly"
    BIMONTHLY = "bimonthly"
    MONTHLY = "monthly"
    SEMIMONTHLY = "semimonthly"
    BIWEEKLY = "biweekly"
    THREETIMESAMONTH = "threeTimesAMonth"
    WEEKLY = "weekly"
    SEMIWEEKLY = "semiweekly"
    THREETIMESAWEEK = "threeTimesAWeek"
    DAILY = "daily"
    CONTINUOUS = "continuous"
    IRREGULAR = "irregular"

    def describe(self):
        description = {
            "triennial": "Triennial",
            "biennial": "Biennial",
            "annual": "Annual",
            "semiannual": "Semiannual",
            "threeTimesAYear": "Three times a year",
            "quarterly": "Quarterly",
            "bimonthly": "Bimonthly",
            "monthly": "Monthly",
            "semimonthly": "Semimonthly",
            "biweekly": "Biweekly",
            "threeTimesAMonth": "Three times a month",
            "weekly": "Weekly",
            "semiweekly": "Semiweekly",
            "threeTimesAWeek": "Three times a week",
            "daily": "Daily",
            "continuous": "Continuous",
            "irregular": "Irregular",
        }
        return description[self.value]
