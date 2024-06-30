from fastapi import FastAPI
import uvicorn
from sqlmodel import SQLModel, create_engine
import os
import time

from utils import ConfigManager, DBManager, setup_logger
from router import post_router, get_router, start_sensor_data_collection


os.environ['TZ'] = 'Asia/Seoul'
time.tzset()

app = FastAPI()

app.include_router(post_router)
app.include_router(get_router)


async def startup_event():
    ini_path = "/home/odroid/workspace/odroid_dashboard/src/config.ini"
    config = ConfigManager(ini_path)
    ini_dict = config.get_config_dict()
    logger = setup_logger(ini_dict)
    
    DB_PATH = ini_dict['DB']['DB_PATH']
    DB_NAME = ini_dict['DB']['DB_NAME']

    DATABASE_URL = f"sqlite:///{DB_PATH}/{DB_NAME}"
    connect_args = {"check_same_thread": False}
    engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)
    db_manager = DBManager(engine)
    
    SQLModel.metadata.create_all(engine)
    
    app.state.logger = logger
    app.state.db_manager = db_manager
    app.state.ini_dict = ini_dict
    # app.state.sensor_state = sensor_state

    start_sensor_data_collection(app)


app.on_event("startup")(startup_event)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
