from typing import Annotated, List

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
        return Response(status_code=status.HTTP_409_CONFLICT)
    if isinstance(trip_status,str):
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
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    return Response(status_code=status.HTTP_200_OK)
