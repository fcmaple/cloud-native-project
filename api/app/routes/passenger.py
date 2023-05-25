from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Response

from ..models.user import UserIn
from ..models.trip import ReservedTrip, ReservedIn
from ..dependencies import get_current_user

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
    userdata: Annotated[UserIn, Depends(get_current_user)]
):
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
