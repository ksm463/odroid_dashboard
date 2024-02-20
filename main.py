from fastapi import FastAPI, HTTPException
import uvicorn
from sqlmodel import SQLModel, Field, create_engine, Session

from loguru import logger
import adafruit_dht
import board
import datetime
import os
import sys
import asyncio
import httpx

from utils.dht import DHTSensor


app = FastAPI()

DATABASE_URL = "sqlite:///./temp_humid.db"
database_file_path = os.path.join(os.getcwd(), "temp_humid.db")
engine = create_engine(DATABASE_URL, echo=True)

dht_sensor = DHTSensor(board.D13)

class SensorData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    temperature: float
    humidity: float

# loguru를 사용하여 로그 파일 설정
logger.remove()
logger.add("temperature_humidity.log", rotation="10 MB")
logger.add(sys.stderr, level="INFO")

def create_tables():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def startup_event():
    db_file_exists = os.path.exists("./temp_humid.db")
    if not db_file_exists:
        # DB 파일이 없을 경우, 테이블 생성
        create_tables()
    asyncio.create_task(sensor_data_collection_loop())

@app.post("/sensor_data/")
def create_sensor_data(sensor_data: SensorData):
    with Session(engine) as session:
        session.add(sensor_data)
        session.commit()
        session.refresh(sensor_data)
        return sensor_data

async def post_sensor_data(temperature, humidity):
    data = {
        "temperature": temperature,
        "humidity": humidity
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/sensor_data/", json=data)
        return response.json()

async def sensor_data_collection_loop():
    while True:
        temperature, humidity = await dht_sensor.get_temperature_humidity()
        if temperature is not None and humidity is not None:
            # 데이터베이스에 저장
            await post_sensor_data(temperature, humidity)
        await asyncio.sleep(3)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(sensor_data_collection_loop())
    uvicorn.run(app, host="0.0.0.0", port=8000)