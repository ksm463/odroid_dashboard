from fastapi import FastAPI, HTTPException
import uvicorn
from sqlmodel import SQLModel, Field, create_engine, Session

import board
import datetime
import os
import sys
import time
import requests
import threading

from sensor import DHTSensor
from utils import config_mng, logger, send_telegram

ini_dict = config_mng.get_config_dict()

app = FastAPI()

DATABASE_URL = "sqlite:///./temp_humid.db"
engine = create_engine(DATABASE_URL, echo=True)

dht_sensor = DHTSensor(board.D13)

class SensorData(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    temperature: float
    humidity: float


def create_tables():
    SQLModel.metadata.create_all(engine)

def start_sensor_data_collection():
    sensor_thread = threading.Thread(target=sensor_data_collection_loop, daemon=True)
    sensor_thread.start()

@app.on_event("startup")
async def startup_event():
    create_tables()
    start_sensor_data_collection()

@app.post("/sensor_data/")
def create_sensor_data(sensor_data: SensorData):
    with Session(engine) as session:
        session.add(sensor_data)
        session.commit()
        session.refresh(sensor_data)
        return sensor_data

def post_sensor_data(temperature, humidity):
    data = {
        "temperature": temperature,
        "humidity": humidity
    }
    try:
        response = requests.post("http://127.0.0.1:8000/sensor_data/", json=data)
        return response.json()
    except requests.exceptions.ConnectionError as e:
        logger.error(f"Failed to post sensor data: {e}")

def sensor_data_collection_loop():
    while True:
        temperature, humidity = dht_sensor.get_temperature_humidity()
        if temperature is not None and humidity is not None:
            post_sensor_data(temperature, humidity)
            # 주의 메시지 조건: 온도가 30도 이상이거나 습도가 20% 이하 또는 80% 이상일 경우
            if temperature >= 30 or humidity <= 20 or humidity >= 50:
                send_telegram(f"주의: 온도 {temperature}°C 또는 습도 {humidity}%가 비정상 범위에 진입했습니다.")
            # 경고 메시지 조건: 온도가 35도 이상일 경우
            if temperature >= 35:
                send_telegram(f"경고: 온도 {temperature}°C가 매우 높습니다.")
        time.sleep(10)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)