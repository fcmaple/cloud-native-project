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

def test_search_trips(oauth_header):
    url = "/trip"
    body = {
        "departure" : "NYCU",
        "destination" : "TSMC",
        "boarding_time" : "2023/6/10 17:00",
    }
    response = client.get(url=url,headers=oauth_header,params=body)
    assert response.status_code == status.HTTP_200_OK
    for trip in response.json():
        assert type(trip["trip_id"]) == int
        assert type(trip["driver_name"]) == str
        assert type(trip["departure"]["location"]) == str and type(trip["departure"]["time"]) == str
        assert type(trip["destination"]["location"]) == str and type(trip["destination"]["time"]) == str
        assert type(trip["payment"]) == int
        assert type(trip["available_seats"]) == int