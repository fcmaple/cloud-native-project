from fastapi.testclient import TestClient
from ..main import app
import pytest
from fastapi import status 


client = TestClient(app)
trip_id = 123

@pytest.fixture
def oauth_header():
    client_id = None
    client_secret = None
    token_url = "/user/login"
    username="wnlab"
    password="wnlab"
    data = {
        "grant_type":"password",
        "username":username,
        "password":password,
        "client_id":client_id,
        "client_secret":client_secret
    }
    response = client.post(token_url, data=data)
    token_data = response.json()
    access_token = token_data['access_token']
    token_headers =  {
        "Authorization" : f"Bearer {access_token}",
        "Content-Type" : "application/json"
    }
    return token_headers


def test_trip_info(oauth_header):
    url = "/driver/trip"

    response = client.get(url=url,headers=oauth_header)
    assert response.status_code==status.HTTP_200_OK
    for trip in response.json():
        assert type(trip["trip_id"])==int
        assert type(trip["driver_name"])==str
        assert type(trip["available_seats"])==int
        assert [type(p["location"])==str and type(p["time"])==str for p in trip["path"]]

def test_reserve_trip_info(oauth_header):
    url = f"/driver/trip/{trip_id}"

    response = client.get(url=url,headers=oauth_header)
    assert response.status_code== status.HTTP_200_OK
    for trip in response.json():
        assert type(trip["point"]["location"])==str 
        assert type(trip["point"]["time"])==str 
        assert [type(p)==str for p in trip["boarding"]]
        assert [type(p)==str for p in trip["Alighting"]]

def test_new_trip(oauth_header):
    url = f"/driver/trip"

    body = {
        "boarding_time": "2023/6/1 17:00",
        "available_seats": 4,
        "path": [
            "NYCU",
            "NTHU",
            "TSMC",
        ]
    }
    
    response = client.post(url=url,headers=oauth_header,json=body)
    assert response.status_code == status.HTTP_201_CREATED
def test_remove_trip(oauth_header):
    url = f"/driver/trip/{trip_id}"

    response = client.delete(url=url,headers=oauth_header)
    assert response.status_code == status.HTTP_200_OK



