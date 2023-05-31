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
        assert type(trip["trip_id"]) == int
        assert type(trip["driver_name"]) == str
        assert type(trip["departure"]["location"]) == str and type(trip["departure"]["time"]) == str
        assert type(trip["destination"]["location"]) == str and type(trip["destination"]["time"]) == str
        assert type(trip["payment"]) == int
        assert type(trip["available_seats"]) == int

def test_remove_reserved_trip(oauth_header):
    url = f"/passenger/trip/{pytest.trip_id}"

    response = client.delete(url=url,headers=oauth_header)
    assert response.status_code == status.HTTP_200_OK


