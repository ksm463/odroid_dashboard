from sqlmodel import SQLModel, Field
from typing import Optional


class DataStruct(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]
