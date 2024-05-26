from fastapi import FastAPI, APIRouter, status, HTTPException, Depends
from typing import List
from datetime import datetime
import time
import threading
import board
from utils import DataStruct, send_telegram
from utils.request import get_logger, get_db_manager
from sensor import DHTSensor


post_router = APIRouter()

dht_sensor = DHTSensor(board.D13)

@post_router.post("/sensor_data/", status_code=status.HTTP_200_OK)
def post_sensor_data(datas: List[DataStruct], db_manager=Depends(get_db_manager), logger=Depends(get_logger)):
    try:
        for sensor_data in datas:
            current_time = datetime.now().isoformat()
            
            data_struct = DataStruct(
                temperature=sensor_data.temperature,
                humidity=sensor_data.humidity,
                timestamp=current_time
            )

            db_manager.add_sensor_data(data_struct)
            
            if data_struct.temperature >= 30 or data_struct.humidity <= 20 or data_struct.humidity >= 60:
                send_telegram(f"주의: 온도 {data_struct.temperature}°C 또는 습도 {data_struct.humidity}%가 비정상 범위에 진입했습니다.")
            
            if data_struct.temperature >= 35:
                send_telegram(f"경고: 온도 {data_struct.temperature}°C가 매우 높습니다.")

        return {"status": "success"}
    except Exception as e:
        logger.error(f"Failed to post sensor data: {e}")
        raise HTTPException(status_code=500, detail="Failed to post sensor data")

def sensor_data_collection_loop(app: FastAPI):
    db_manager = app.state.db_manager
    logger = app.state.logger
    while True:
        try:
            temperature, humidity = dht_sensor.get_temperature_humidity()
            if temperature is not None and humidity is not None:
                data_struct = DataStruct(temperature=temperature, humidity=humidity)
                post_sensor_data([data_struct], db_manager=db_manager, logger=logger)
        except Exception as e:
            logger.error(f"Failed to collect sensor data: {e}")
        time.sleep(10)

def start_sensor_data_collection(app: FastAPI):
    sensor_thread = threading.Thread(target=sensor_data_collection_loop, args=(app,), daemon=True)
    sensor_thread.start()
