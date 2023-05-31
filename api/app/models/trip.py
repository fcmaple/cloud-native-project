from typing import List

from pydantic import BaseModel


class PosTime(BaseModel):
    location: str
    time: str


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
    boarding_time: str
    available_seats: int
    path: List[str]

class FullTrip(BaseModel):
    trip_id: int
    driver_name: str
    # path: List[PosTime]
    departure: PosTime
    destination: PosTime
    available_seats: int