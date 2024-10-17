from __future__ import annotations
from pydantic import Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

from app.schemas.base_schema import BaseSchema
from app.schema_types import FrequencyType, StateType


class ChartData(BaseSchema):
    period: str
    value: int
    proportion: Optional[float] = Field(None)


class ReportData(BaseSchema):
    project_id: Optional[UUID] = Field(None, description="Project reference.")
    project_name: Optional[str] = Field(None, description="Project name.")
    task_id: Optional[UUID] = Field(None, description="Project reference.")
    task_name: Optional[str] = Field(None, description="Project name.")
    frequency: Optional[FrequencyType] = Field(default=FrequencyType.QUARTER, description="Frequency interval summary.")
    state: Optional[StateType] = Field(default=StateType.COMPLETE, description="Resource work state.")
    date_from: Optional[datetime] = Field(None, description="Start date for report period.")
    date_to: Optional[datetime] = Field(None, description="End date for report period.")
    count: int = Field(..., description="Number of Tasks in the data series.")
    data: Optional[List[ChartData]] = Field([], description="List of chart data.")
