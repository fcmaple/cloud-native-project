from typing import Annotated, List
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Response

from ..models.user import UserIn
from ..models.trip import ReservedTrip, ReservedIn , calPayment
from ..dependencies import get_current_user
from ..db.crud import get_db

from sqlalchemy.orm import Session
from datetime import datetime
router = APIRouter(
    prefix="/passenger",
    tags=["passenger"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Could not validate credentials"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"}
    }
)
@router.get(
    "/trip/position",
    status_code=status.HTTP_200_OK,
    responses = {
        status.HTTP_200_OK: {"context": None},
        status.HTTP_404_NOT_FOUND: {"description": "The trip is no exist."},
    }
)
def read_trip_position(
    trip_id:int,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    trips = db.get_data_trips(trip_id)
    if isinstance(trips,str):
        logging.warning(f"API function: read_trip_position, Error: The trip is no exist.")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    position = trips[0]['position']
    req = {
        'position': position if position is not None else '', 
    }
    logging.info(f"API function: read_trip_position, Return: {req}")
    return req

@router.get(
    "/trip",
    response_model=List[ReservedTrip]
)
def read_reserved_trip_info(
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    res = []
    trip_for_user = db.get_data_passengers_userid(user.user_id)
    if isinstance(trip_for_user,str):
        logging.info(f"API function: read_reserved_trip_info, Return: {res}")
        return res
    for trip in trip_for_user:
        trip_info = db.get_data_trips(trip['trip_id'])[0]
        driver_info = db.get_data_users_byid(trip_info['user_id'])
        departure_info = db.get_data_locationsid(trip['trip_id'], trip['departure'])
        destination_info = db.get_data_locationsid(trip['trip_id'], trip['destination'])
        single_trip = {
            'trip_id' : trip['trip_id'],
            'driver_name' : driver_info['username'],
            'departure' : {
                'location' : trip['departure'], 
                'time' : departure_info['time'],
            },
            'destination' : {
                "location":trip['destination'],
                'time':destination_info['time'],
            },
            'payment' : trip['cost'],
            'available_seats' : trip_info['available_seats'],
        }
        res.append(single_trip)
    logging.info(f"API function: read_reserved_trip_info, Return: {res}")
    return res


@router.post(
    "/trip",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"content": None},
        status.HTTP_404_NOT_FOUND: {"description": "There is no such trip."},
        status.HTTP_409_CONFLICT: {"description": "The trip has no available seats."}
    }
)
def reserve_trip(
    query: ReservedIn,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    trip_status = db.get_data_trips(query.trip_id)
    if trip_status[0]['available_seats'] <= 0:
        logging.warning(f"API function: reserve_trip, Error: The trip has no available seats.")
        return Response(status_code=status.HTTP_409_CONFLICT)
    if isinstance(trip_status,str):
        logging.warning(f"API function: reserve_trip, Error: There is no such trip.")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    first_location = db.get_data_locationsid(query.trip_id,query.departure) 
    last_location = db.get_data_locationsid(query.trip_id,query.destination)
    dif_location = last_location['location_id']-first_location['location_id']
    dic = {
        'trip_id' : query.trip_id,
        'user_id' : user.user_id,
        'departure' : query.departure,
        'destination' : query.destination,
        'cost': calPayment(dif_location)
    }
    _ = db.insert_data_passengers(dic)
    for trip in trip_status:
        trip['available_seats'] -= 1
        dic = { 
            'available_seats' : trip['available_seats']
        }
        db.update_data_trips(trip['trip_id'],dic)
    logging.info(f"API function: reserve_trip, Reserve trip_id:{query.trip_id}, departure: {query.departure}, destination: {query.destination}\
                  Success !")
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/trip/{trip_id}",
    responses={
        status.HTTP_200_OK: {"content": None},
        status.HTTP_404_NOT_FOUND: {"description": "There is no such trip or passenger in db."},
    }
)
def remove_reserved_trip(
    trip_id: int,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
): 

    delete_info = db.delete_data_passengers_by_trip_user_id(trip_id, user.user_id)
    if delete_info != "SUCCESS":
        logging.warning(f"API function: remove_reserved_trip, Remove trip_id: {trip_id} Fail")
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    logging.info(f"API function: remove_reserved_trip, Remove trip_id: {trip_id} Success")
    return Response(status_code=status.HTTP_200_OK)
