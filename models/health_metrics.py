from typing import List, Optional
from pydantic import BaseModel, validator
from datetime import datetime

class HealthMetricData(BaseModel):
    date: datetime
    qty: Optional[float] = None
    source: Optional[str] = None
    Min: Optional[float] = None
    Avg: Optional[float] = None
    Max: Optional[float] = None
    
    @validator("date", pre=True)
    def parse_date(cls, value):
        """
        Custom validator to parse date strings into datetime objects.
        """
        if isinstance(value, str):
            try:
                # Parse the date string with the expected format
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S %z")
            except ValueError:
                raise ValueError(f"Invalid date format: {value}")
        return value

class HealthMetric(BaseModel):
    name: str
    units: str
    data: List[HealthMetricData]

class HealthData(BaseModel):
    metrics: List[HealthMetric]

class HealthRootModel(BaseModel):
    data: HealthData