from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel

from ..models.user import UserIn
from ..models.trip import FullTrip, PosTime, NewTrip
from ..dependencies import get_current_user

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
)
def read_trip_info(
    userdata: Annotated[UserIn, Depends(get_current_user)]
):
    info = {
        "trip_id" : 12,
        "driver_name": "Dave",
        "path": 
            [
                {
                    "location" : "NTHU",
                    "time" : "2023/6/1 17:00",
                },
                {   
                    "location" : "NYCU",
                    "time" : "2023/6/1 18:00",
                },
                {
                    "location" : "TSMC",
                    "time" : "2023/6/1 19:00",
                }
            ],
        "available_seats" : 4,
    }
    return [info,info]


class ReservedLocation(BaseModel):
    point: PosTime
    boarding: List[str]
    Alighting: List[str]


@router.get(
    "/trip/{trip_id}",
    response_model=List[ReservedLocation],
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "There is no such trip."},
    }
)
def read_reserved_trip_info(
    trip_id:int,
    _: Annotated[UserIn, Depends(get_current_user)]
):
    info = {
        "point": {
            "location" : "NYCU",
            "time" : "2023/6/2 17:00"
        },
        "boarding":[
            "AAA",
            "BBB",
            "CCC",
        ],
        "Alighting":[
            "AAA",
            "BBB",
            "CCC",
        ]
    }
    return [info,info]


@router.post(
    "/trip",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"content": None},
    }
)
def new_trip(
    query: NewTrip,
    _: Annotated[UserIn, Depends(get_current_user)]
):
    return Response(status_code=status.HTTP_201_CREATED)


@router.delete(
    "/trip/{trip_id}",
    responses={
        status.HTTP_200_OK: {"content": None},
        status.HTTP_404_NOT_FOUND: {"description": "There is no such trip."},
    }
)
def remove_trip(
    trip_id:int,
    _: Annotated[UserIn, Depends(get_current_user)]
):
    return Response(status_code=status.HTTP_200_OK)