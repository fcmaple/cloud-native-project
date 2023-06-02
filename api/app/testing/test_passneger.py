from fastapi.testclient import TestClient
from ..main import app
import pytest
from fastapi import status 
from .oauth  import oauth_header
from .test_trip import test_search_trips
client = TestClient(app)

def test_reserve_trip(oauth_header):
    url = "/passenger/trip"
    test_search_trips(oauth_header)
    body ={
        "trip_id": pytest.trip_id,
        "departure": "NYCU",
        "destination":"TSMC",
    }
    response = client.post(url=url,headers=oauth_header,json=body)
    assert response.status_code == status.HTTP_201_CREATED
def test_reserved_trip_info(oauth_header):
    url = "/passenger/trip"
    response = client.get(url=url,headers=oauth_header)
    assert response.status_code == status.HTTP_200_OK
    for trip in response.json():
        assert isinstance(trip["trip_id"],int)
        assert isinstance(trip["driver_name"],str) 
        assert isinstance(trip["departure"]["location"],str)  and isinstance(trip["departure"]["time"],str) 
        assert isinstance(trip["destination"]["location"],str)  and isinstance(trip["destination"]["time"],str)
        assert isinstance(trip["payment"],int)
        assert isinstance(trip["available_seats"],int) 
def test_driver_position(oauth_header):
    url = "/passenger/trip/position"
    body = {
        "trip_id" : pytest.trip_id,
    }
    response = client.get(url=url,headers=oauth_header,params=body)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json()['position'],str)
def test_remove_reserved_trip(oauth_header):
    url = f"/passenger/trip/{pytest.trip_id}"

    response = client.delete(url=url,headers=oauth_header)
    assert response.status_code == status.HTTP_200_OK


