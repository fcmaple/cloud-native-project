from fastapi.testclient import TestClient
from ..main import app
import pytest
from fastapi import status 
from .oauth  import oauth_header

client = TestClient(app)
def test_search_trips(oauth_header):
    url = "/trip"
    body = {
        "departure" : "NYCU",
        "destination" : "TSMC",
        "boarding_time" : "2022-11-04T00:05:23",
    }
    response = client.get(url=url,headers=oauth_header,params=body)
    assert response.status_code == status.HTTP_200_OK
    for trip in response.json():
        assert isinstance(trip["trip_id"],int) 
        pytest.trip_id = trip["trip_id"]
        assert isinstance(trip["driver_name"],str)
        assert isinstance(trip["departure"]["location"],str) and isinstance(trip["departure"]["time"],str)
        assert isinstance(trip["destination"]["location"],str) and isinstance(trip["destination"]["time"],str) 
        assert isinstance(trip["payment"],int) 
        assert isinstance(trip["available_seats"],int)