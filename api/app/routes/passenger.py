from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from ..models.user import UserIn
from ..models.trip import ReservedTrip, ReservedIn
from ..dependencies import get_current_user
from ..db.crud import get_db
from sqlalchemy.orm import Session
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
    userdata: Annotated[UserIn, Depends(get_current_user)]
):
    info = {
            "trip_id": 123,
            "driver_name": "Dave",
            "departure": {
                "location": "NYCU",
                "time": "2023/6/1 17:00",
            },
            "destination": {
                "location": "TSMC",
                "time": "2023/6/1 18:00",
            },
            "payment" : 120,
            "available_seats": 4,
        }
    return [info, info]


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
    cost = 1234
    trip_status = db.get_data_trips(query.trip_id)
    print(trip_status)
    if trip_status[0]['available_seats'] <= 0:
        return Response(status_code=status.HTTP_409_CONFLICT)
    if isinstance(trip_status,str):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    dic = {
        'trip_id' : query.trip_id,
        'user_id' : user.user_id,
        'departure' : query.departure,
        'destination' : query.destination,
        'cost':cost
    }
    _ = db.insert_data_passengers(dic)
    for trip in trip_status:
        trip['available_seats'] -= 1
        dic = {'available_seats':trip['available_seats']}
        db.update_data_trips(trip['trip_id'],dic)
        print(trip)
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/trip/{trip_id}",
    responses={
        status.HTTP_200_OK: {"content": None},
        status.HTTP_404_NOT_FOUND: {"description": "There is no such trip."},
    }
)
def remove_reserved_trip(
    trip_id: int,
    _: Annotated[UserIn, Depends(get_current_user)]
): 
    return Response(status_code=status.HTTP_200_OK)
