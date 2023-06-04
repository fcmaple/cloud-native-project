from typing import Annotated, List
import json,logging

from fastapi import APIRouter, Depends, HTTPException, status

from ..models.trip import ReservedTrip, calPayment, mapData
from ..models.user import UserIn
from ..dependencies import get_current_user
from ..db.crud import get_db
from sqlalchemy.orm import Session
from datetime import datetime


router = APIRouter(
    prefix="/trip",
    tags=["trip"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Could not validate credentials"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"},
        
    }
)
@router.get(
    "",
    response_model=List[ReservedTrip],
    responses={
        status.HTTP_409_CONFLICT: {"description": "BOARDING_TIME invalid type"}
    }
)
def search_trips(
    departure: str,
    destination: str,
    boarding_time: datetime,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    res = []
    departure_info = db.get_data_locations_info_by_name(departure)
    if isinstance(departure_info,str):
        return res
    for trip in departure_info:
        single_trip = dict()
        single_trip['trip_id'] = trip['trip_id']
        destination_info = db.get_data_locations_info_by_name(destination, trip['trip_id'])
        if isinstance(destination_info, str):
            continue
        single_trip['departure'] = {
            'location' : departure, 
            'time': trip['time']
        }
        try:
            if single_trip['departure']['time'] > boarding_time:
                single_trip['destination'] = {
                    'location' : destination, 
                    'time': destination_info[0]['time']
                }
                dif_location = destination_info[0]['location_id']-trip['location_id']
                single_trip['payment'] = calPayment(dif_location)
                _trip_info = db.get_data_trips(trip['trip_id'])[0]
                _user_info = db.get_data_users_byid(_trip_info['user_id'])
                single_trip['available_seats'] = _trip_info['available_seats']
                single_trip['driver_name'] = _user_info['username']
                res.append(single_trip)
        except:
            logging.warning(f"API function: search_trips, Error: boarding_time invalid type")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"boarding_time invalid type , ex: 2023-05-01T08:51:41")
    logging.info(f"API function: search_trips ,Return {res}")
    return res


@router.get(
    "/maps",
    response_model=List[mapData],
)
def get_maps(
    user: Annotated[UserIn, Depends(get_current_user)],
):
    with open('app/map.json', 'r') as f:
        res = json.load(f)
    logging.info(f"API function: get_maps ")
    return res
