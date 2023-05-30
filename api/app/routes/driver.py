from typing import Annotated, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Response
from pydantic import BaseModel

from ..models.user import UserIn
from ..models.trip import FullTrip, PosTime, NewTrip
from ..dependencies import get_current_user

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
)
def read_trip_info(
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    ret = db.get_data_trips(user.user_id)
    trip_set = set([trip['trip_id'] for trip in ret])
    trips = []
    for trip_id in trip_set:
        t = dict()
        t['path'] = []
        for trip in ret:
            if trip_id != trip['trip_id']:
                continue
            t['trip_id'] = trip_id
            t["driver_name"] = trip['driver_name']
            t['available_seats'] = trip['available_seats']
            boarding_time = datetime.strftime(trip['boarding_time'],'%Y-%m-%d %H:%M:%S')
            t['path'].append({'location':trip['path'],'time':boarding_time})
        trips.append(t)
    return trips

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
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    locations = db.get_data_locations(trip_id)
    if isinstance(locations,str):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    passengers = db.get_data_passengers(trip_id)
    print(f'-----------------------------')
    print(passengers)
    print(f'-----------------------------')

    print(f'-----------------------------')

    print(locations)
    print(f'-----------------------------')

    # name : str , time : str , trip_id
    info = []
    for location in locations:
        dic = {"point":{"location":location["name"],"time":datetime.strftime(location["time"],'%Y-%m-%d %H:%M:%S')},"boarding":[],"Alighting":[]}
        if isinstance(passengers,str):
            info.append(dic)
            continue
        for passenger in passengers:
            data = db.get_data_users_byid(passenger['user_id'])
            if passenger['departure'] == location['name']:
                dic["boarding"].append(data['username'])
            if passenger['destionation'] == location['name']:
                dic["Alighting"].append(data['username'])
        info.append(dic)
    print(info)
    return info


    # info = {
    #     "point": {
    #         "location" : "NYCU",
    #         "time" : "2023/6/2 17:00"
    #     },
    #     "boarding":[
    #         "AAA",
    #         "BBB",
    #         "CCC",
    #     ],
    #     "Alighting":[
    #         "AAA",
    #         "BBB",
    #         "CCC",
    #     ]
    # }
    # return [info,info]


@router.post(
    "/trip",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "new trip is created"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "API or Database Server Error"},
        status.HTTP_406_NOT_ACCEPTABLE: {"description": "Invalid parameters"}
    }
)
def new_trip(
    query: NewTrip,
    user: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    #2011-11-04T00:05:23
    query.boarding_time = datetime.fromisoformat(query.boarding_time)
    req = {}
    req['user_id'] = user.user_id
    req['available_seats'] = query.available_seats
    req['boarding_time'] = query.boarding_time
    res = db.insert_data_trips(req)
    trip_id = db.get_data_tripid(req)
    if res != "SUCCESS":
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    if query.path == []:
        return Response(status_code=status.HTTP_406_NOT_ACCEPTABLE)
    for p in query.path:
        req = {}
        req['trip_id'] = trip_id['trip_id']
        req['name'] = p
        req['time'] = query.boarding_time
        db.insert_data_locations(req)
    first_location = db.get_data_locationsid(trip_id['trip_id'],query.path[0]) 
    last_location = db.get_data_locationsid(trip_id['trip_id'],query.path[-1])
    dic = {"departure":first_location["location_id"],"destination":last_location["location_id"]}
    db.update_data_trips(trip_id['trip_id'],dic)

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
    _: Annotated[UserIn, Depends(get_current_user)],
    db: Annotated[Session,Depends(get_db)],
):
    if db.delete_data_trips(trip_id) != "SUCCESS":
        return Response(status_code=status.HTTP_404_NOT_FOUND)
     
    return Response(status_code=status.HTTP_200_OK)