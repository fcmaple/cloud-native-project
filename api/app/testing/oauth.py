from ..main import app
from fastapi.testclient import TestClient
import pytest


username="a"
password="a"
client = TestClient(app)
@pytest.fixture
def oauth_header():
    client_id = None
    client_secret = None
    url = "/user"
    body = {
        "username": username,
        "realname": "b",
        "phone": "b",
        "car": "b",
        "password": password,
        "user_id": 0
    }
    response = client.post(url=url,json=body)
    token_url = "/user/login"
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