from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.trip import ReservedTrip
from ..models.user import UserIn
from ..dependencies import get_current_user

router = APIRouter(
    prefix="/trip",
    tags=["trip"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Could not validate credentials"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"}
    }
)


@router.get(
    "",
    response_model=List[ReservedTrip],
)
def search_trips(
    departure: str,
    destination: str,
    boarding_time: str,
    _: Annotated[UserIn, Depends(get_current_user)]
):
    info = {
        "trip_id" : 12,
        "driver_name":"Dave",
        "departure":{
            "location" : departure,
            "time" : "2023/6/1 18:00",
        },
        "destination":{
            "location" : destination,
            "time" : "2023/6/1 19:00",
        },
        "payment" : 120,
        "available_seats": 4,
    }
    return [info,info]
