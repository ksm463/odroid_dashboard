from sqlmodel import SQLModel, Field, create_engine, Session

import datetime

from utils import config_mng

ini_dict = config_mng.get_config_dict()
DB_PATH = ini_dict['DB']['db_path']
DB_NAME = ini_dict['DB']['db_name']

DATABASE_URL = "sqlite:///./db/temp_humid.db"
engine = create_engine(DATABASE_URL, echo=True)


class SensorData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    temperature: float
    humidity: float

def create_tables():
    SQLModel.metadata.create_all(engine)