from fastapi.testclient import TestClient
from ..main import app
import pytest
from fastapi import status 
from datetime import datetime,timedelta
from .oauth  import oauth_header

client = TestClient(app)



def test_new_trip(oauth_header):
    url = f"/driver/trip"

    body = {
        "boarding_time": datetime.strftime(datetime.now()+timedelta(days=10),'%Y-%m-%d %H:%M:%S'),
        "available_seats": 4,
        "path": [
            "NYCU",
            "NTHU",
            "TSMC",
        ]
    }
    response = client.post(url=url,headers=oauth_header,json=body)
    assert response.status_code == status.HTTP_201_CREATED
def test_trip_info(oauth_header):
    url = "/driver/trip"

    response = client.get(url=url,headers=oauth_header)
    assert response.status_code==status.HTTP_200_OK
    for trip in response.json():
        assert isinstance(trip["trip_id"],int)
        pytest.trip_id = trip["trip_id"]
        assert isinstance(trip["driver_name"],str)
        assert isinstance(trip["available_seats"],int)
        assert isinstance(trip["departure"]["location"],str) and isinstance(trip["departure"]["time"],str)
        assert isinstance(trip["destination"]["location"],str)and isinstance(trip["destination"]["time"],str)

def test_reserve_trip_info(oauth_header):
    url = f"/driver/trip/{pytest.trip_id}"

    response = client.get(url=url,headers=oauth_header)
    assert response.status_code== status.HTTP_200_OK
    for trip in response.json():
        assert isinstance(trip["point"]["location"],str) and isinstance(trip["point"]["time"],str)
        assert [isinstance(p,str) for p in trip["boarding"]] or len(trip["boarding"]) >= 0
        assert [isinstance(p,str) for p in trip["Alighting"]] or len(trip["Alighting"]) >= 0


def test_remove_trip(oauth_header):
    test_new_trip(oauth_header)
    test_trip_info(oauth_header)
    url = f"/driver/trip/{pytest.trip_id}"
    response = client.delete(url=url,headers=oauth_header)
    assert response.status_code == status.HTTP_200_OK



