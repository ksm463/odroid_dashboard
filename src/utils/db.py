from sqlmodel import Session


class DBManager:
    def __init__(self, engine):
        self.engine = engine

    def add_sensor_data(self, sensor_data):
        with Session(self.engine) as session:
            session.add(sensor_data)
            session.commit()
            session.refresh(sensor_data)
