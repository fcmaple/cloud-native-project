from typing import Annotated, List
from datetime import datetime , timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel

from ..models.user import UserIn
from ..models.trip import FullTrip, PosTime, NewTrip
from ..dependencies import get_current_user
from ..config import settings
from ..db.crud import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/driver",
    tags=["driver"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Could not validate credentials"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"}
    }
)

@router.get(
    "/trip",
    response_model=List[FullTrip],
    responses={
        status.HTTP_200_OK: {"context": None},
    }

)
def read_trip_info(
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    ret = db.get_data_trips_by_userid(user.user_id)
    trips = []
    if isinstance(ret,str):
        return trips
    for trip in ret:
        # print(trip)
        single_trip = {
            'trip_id': trip['trip_id'],
            'driver_name': user.username,
            'available_seats': trip['available_seats'],
            'departure': {
                'location': trip['departure'],
                'time': trip['boarding_time'],
            },
            'destination': {
                'location': trip['destination'],
                'time':  trip['alighting_time'],
            }
        }
        trips.append(single_trip)
    return sorted(trips,key=lambda x:x['trip_id'])

class ReservedLocation(BaseModel):
    point: PosTime
    boarding: List[str]
    Alighting: List[str]


@router.get(
    "/trip/{trip_id}",
    response_model=List[ReservedLocation],
    responses={
        status.HTTP_200_OK: {"context": None},
        status.HTTP_404_NOT_FOUND: {"description": "There is no such trip."},
    }
)
def read_reserved_trip_info(
    trip_id:int,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    locations = db.get_data_locations(trip_id)
    if isinstance(locations,str):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    passengers = db.get_data_passengers(trip_id)

    info = []
    for location in locations:
        dic = {
            'point':  {
                'location' : location['name'],
                'time' : location["time"],
            },
            'boarding' : [],
            'Alighting' : [],
        }
        if isinstance(passengers,str):
            info.append(dic)
            continue
        for passenger in passengers:
            data = db.get_data_users_byid(passenger['user_id'])
            if passenger['departure'] == location['name']:
                dic["boarding"].append(data['username'])
            if passenger['destination'] == location['name']:
                dic["Alighting"].append(data['username'])
        info.append(dic)
    return info
@router.put(
    "/trip/position",
    responses = {
        status.HTTP_404_NOT_FOUND: {"description": "The trip is no exist"},
    }
)
def update_trip_position(
    trip_id: int,
    position: str,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    req = {
        'position' : position
    }

    if db.update_data_trips(trip_id,req) != 'SUCCESS':
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_200_OK)
    
@router.post(
    "/trip",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "new trip is created"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"},
        status.HTTP_406_NOT_ACCEPTABLE: {"description": "Invalid parameters"},
        status.HTTP_405_METHOD_NOT_ALLOWED: {"description": "USER_ID or BOARDING_TIME already exists"}
    }
)
def new_trip(
    query: NewTrip,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    req = {
        'user_id' : user.user_id,
        'available_seats' : query.available_seats,
        'boarding_time' : query.boarding_time
    }
    if query.path == [] or '' in query.path:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    res = db.insert_data_trips(req)
    if not isinstance(res,str):
        return Response(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    trip_id = db.get_data_tripid(req)
    for idx,p in enumerate(query.path):
        req = {
            'trip_id' : trip_id['trip_id'],
            'name' : p,
            'time' : query.boarding_time + timedelta(minutes=settings.POINT_MINUTES*idx)
        }
        db.insert_data_locations(req)
    first_location = db.get_data_locationsid(trip_id['trip_id'],query.path[0]) 
    last_location = db.get_data_locationsid(trip_id['trip_id'],query.path[-1])
    dic = {
        'departure' : first_location['location_id'],
        'destination' : last_location['location_id'],
        'alighting_time' : last_location['time'],
    }
    db.update_data_trips(trip_id['trip_id'],dic)

    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/trip/{trip_id}",
    responses={
        status.HTTP_200_OK: {"content": None},
        status.HTTP_404_NOT_FOUND: {"description": "There is no such trip."},
        status.HTTP_403_FORBIDDEN: {"description": "passenger or location remove error"}
    }
)
def remove_trip(
    trip_id:int,
    _: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):

    db.delete_data_passengers(trip_id)
    if db.delete_data_locations(trip_id) != "SUCCESS":
        return Response(status_code=status.HTTP_403_FORBIDDEN)
    if db.delete_data_trips(trip_id) != "SUCCESS":
        return Response(status_code=status.HTTP_404_NOT_FOUND)
     
    return Response(status_code=status.HTTP_200_OK)