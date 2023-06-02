from typing import List
from datetime import datetime
from pydantic import BaseModel

def calPayment(distance:int):
    return 10*distance

class PosTime(BaseModel):
    location: str
    time: datetime


class ReservedTrip(BaseModel):
    trip_id: int
    driver_name: str
    departure: PosTime
    destination: PosTime
    payment: int
    available_seats: int


class ReservedIn(BaseModel):
    trip_id: int
    departure: str
    destination: str


class NewTrip(BaseModel):
    boarding_time: datetime
    available_seats: int
    path: List[str]

class FullTrip(BaseModel):
    trip_id: int
    driver_name: str
    departure: PosTime
    destination: PosTime
    available_seats: int

class mapData(BaseModel):
    location: str
    lat: float
    lng: float