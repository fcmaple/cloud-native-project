from sqlalchemy import ForeignKey, TIMESTAMP, Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base, engine
from datetime import datetime

class users_table(Base):
    __tablename__ = "users"

    # renew
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(55), primary_key=True, unique=True)
    realname = Column(String(55), nullable=False)
    password = Column(String(300), nullable=False)
    phone = Column(String(55), nullable=False)
    car = Column(String(55))

    def __str__(self):
        return f"users<id={self.user_id}, name={self.username}, password={self.password}, phone={self.phone}, car={self.car}>"

class trips_table(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    departure = Column(Integer)
    destination = Column(Integer)
    available_seats = Column(Integer, nullable=False)
    # renew search (seats)
    # time format - '05/25/2023 17:56:00'
    boarding_time = Column(TIMESTAMP, default=datetime.utcnow)
    alighting_time = Column(TIMESTAMP)
    

    
    def __str__(self):
        return f"trips<trip_id={self.trip_id}, user_id={self.user_id}, path={self.path}, available_seats={self.available_seats}, broading_time={self.broading_time}>"

class passengers_table(Base):
    __tablename__ = "passengers"

    passenger_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    departure = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    # renew
    # cost
    cost = Column(Integer, nullable=False)

    def __str__(self):
        return f"passengers<passenger_id={self.passenger_id}, trip_id={self.trip_id}, driver_id={self.driver_id}, departure={self.departure}, destination={self.destination}>"

class locations_table(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"))
    name = Column(String(55), nullable=False)
    time = Column(TIMESTAMP, default=datetime.utcnow)

    def __str__(self):
        return f"locations<location_id={self.location_id}, trip_id={self.trip_id}, name={self.name}, time={self.time}>"


    # def create_table():
    #     Base.metadata.create_all(engine)

    # def drop_table():
    #     Base.metadata.drop_all(engine)