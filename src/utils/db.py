from sqlmodel import Session, select
from utils.struct import DataStruct


class DBManager:
    def __init__(self, engine):
        self.engine = engine

    def add_sensor_data(self, sensor_data):
        with Session(self.engine) as session:
            session.add(sensor_data)
            session.commit()
            session.refresh(sensor_data)
    
    def get_all_sensor_data(self):
        with Session(self.engine) as session:
            sensor_data = session.exec(select(DataStruct)).all()
            return sensor_data
    
    def get_recent_sensor_data(self, ini_dict):
        RECENY_LENGTH = ini_dict['DB']['RECENT_LENGTH']
        with Session(self.engine) as session:
            sensor_data = session.exec(
                select(DataStruct).order_by(DataStruct.timestamp.desc()).limit(RECENY_LENGTH)
            ).all()
            return sensor_data
