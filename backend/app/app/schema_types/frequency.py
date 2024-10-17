from enum import auto
import pandas as pd

from app.schema_types.base import BaseEnum


class FrequencyType(BaseEnum):
    MONTH = auto()
    QUARTER = auto()
    YEAR = auto()

    def describe(self):
        description = {
            "MONTH": "Data aggregated to monthly update frequence.",
            "QUARTER": "Data aggregated to quarterly update frequence.",
            "YEAR": "Data aggregated to annual update frequence.",
        }
        return description[self.value]

    def drange(self):
        description = {
            "MONTH": "MS",
            "QUARTER": "QS",
            "YEAR": "YS",
        }
        return description[self.value]

    def offset(self):
        description = {
            "MONTH": pd.tseries.offsets.MonthEnd(),
            "QUARTER": pd.tseries.offsets.QuarterEnd(startingMonth=0),
            "YEAR": pd.tseries.offsets.YearEnd(),
        }
        return description[self.value]
