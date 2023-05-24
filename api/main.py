from typing import Union,List

from fastapi import FastAPI
from pydantic import BaseModel
tags_metadata = [
    {
        "name": "passenger",
        "description": "Operations with passenger",
    },
    {
        "name": "driver",
        "description": "Operations with driver",
    },
    {
        "name": "user",
        "description": "Operations with user",
    }
]
app = FastAPI(openapi_tags=tags_metadata)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/passenger/{user_id}",tags=["passenger"])
def read_trip_info(user_id: int):
    """
    Get the information of reserved trips
    
    Args:

        user_id (int) : The ID of the user
    
    Returns:

        list of trip information (list) : 
            driver_name (str) : The driver name in the trip
            passenger_id (int) : The passenger id in the trip
            departure (str,str):  When and Where the passenger will get on
            destination (str,str): When and Where the passenger will get off
    """
    info = {
            "driver_name": "Dave",
            "passenger_id": 123,
            "departure": {
                "location": "NYCU",
                "time": "2023/6/1 17:00",
            },
            "destination": {
                "location": "TSMC",
                "time": "2023/6/1 18:00",
            },
        }
    return [info,info]


@app.get("/trip/passenger/",tags=["passenger"])
def search_trips(departure:str,destination:str,datetime:str):
    """
    Display all trip info that meets the specified criteria
    
    Args:

        departure (str):  Where the passenger will get on
        destination (str): Where the passenger will get off
        datetime (str): The time want to boarding
    
    Returns:

        list of matched trip information (list): 
            driver_name (str) : The driver name in the trip
            departure (str,str):  When and Where the passenger will get on
            destination (str,str): When and Where the passenger will get off
            payment (int) : The fee in the trip
            trip_id (int) : The ID of the trip
    """
    trip_info = {
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
        "trip_id" : 12,
    }
    return [trip_info,trip_info]

@app.post("/trip/passenger/",tags=["passenger"])
def reserve_trip(user_id:int,trip_id:int,departure:str , destination:str):
    """
    Reserve the trip

    Args:

        user_id (int) : The ID of the user
        trip_id (int) : The ID of the trip
        departure (str):  Where the passenger will get on
        destination (str): Where the passenger will get off
    
    Returns:

    """
    return {}

@app.delete("/passenger/{passenger_id}",tags=["passenger"])
def remove_passenger(passenger_id: int): 
    """
    Remove the passenger in the trip

    Args:

        passenger_id (int) : The ID of the passenger in the trip
    
    Returns:

    """
    return {}

@app.get("/driver/{user_id}",tags=["driver"])
def read_trip_info(user_id:int):
    """
    Display the upcoming shifts the driver will drive next

    Args:

        user_id (int) : The ID of the user
    
    Returns:

        departure (str,str):  When and Where the passenger will get on
        destination (str,str): When and Where the passenger will get off
        available_seats (int): Seats are available for passengers to
        trip_id (int) : The ID of the trip
    """
    # get all driver trip info
    info = {
        "departure":{
            "location" : "NYCU",
            "time" : "2023/6/1 17:00",
        },
        "destination":{
            "location" : "TSMC",
            "time" : "2023/6/1 18:00",
        },
        "available_seats" : 4,
        "trip_id" : 12,
    }
    return [info,info]

@app.get("/driver/{trip_id}",tags=["driver"])
def read_trip_detail(trip_id:int):
    """
    Display the detail information of the trip

    Args:

        trip_id (int) : The ID of the trip
    
    Returns:

        list of trip detail information (list):
            location (str): The name of the trip point
            time (str): When should the driver arrive
            boarding (list[str]): The list of boarding passengers
            alighting (list[str]): The list of alighting passengers
    """
    info = {
        "location" : "NYCU",
        "time" : "2023/6/2 17:00",
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

@app.post("/trip/driver/",tags=["driver"])
def new_trip(datetime:str,available_seats:int,path:list):
    """
    Create a new trip

    Args:

        datetime (str): The start time
        available_seats (int): Seats are available for passengers to
        path (list[str]): The following points
    
    Returns:

    """
    return {}

@app.delete("/driver/{trip_id}",tags=["driver"])
def remove_trip(trip_id:int):
    """
    Remove the trip and all passenger in the trip

    Args:

        trip_id (int) : The ID of the trip
    
    Returns:

    """
    return {}

@app.get("/user/{user_id}",tags=["user"])
def read_user_info(user_id:int):
    """
    Get the personal information
    
    Args:

        user_id (int): The ID of the user

    Returns:

        name (str): the real name of user
        phone (str): the phone number
        car (str|none): the name of car 
    """
    info = {
        "name" : "AAA",
        "phone" : "0912345678",
        "car" : "BMW",
    }
    return info

@app.post("/user/",tags=["user"])
def new_user(name:str,phone:str,user_name:str,password:str,car: Union[str , None]=None):
    """
    Register 

    Args:

        name (str): the real name of user
        phone (str): the phone number
        car (str|none): the name of car 
   
    Returns:

        user_id (int): The ID of the user
    
    """
    user_id = 1234
    return {"user_id":user_id}