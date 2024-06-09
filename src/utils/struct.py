from sqlmodel import SQLModel, Field
from typing import Optional


class DataStruct(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]

class SensorState:
    def __init__(self):
        self.very_high_temp_alert_sent = False
        self.high_temp_alert_sent = False
        self.low_humidity_alert_sent = False
        self.high_humidity_alert_sent = False