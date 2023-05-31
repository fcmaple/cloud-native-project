from fastapi.testclient import TestClient
from ..main import app
from fastapi import status 
from .oauth  import oauth_header

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "It works"
    
# def test_register_user(oauth_header):
#     url = "/user"
#     body = {
#         "username": "NYCUSER",
#         "realname": "Dave",
#         "phone": "0912345678",
#         "car": "BMW",
#         "password" : "green446b",
#     }
#     response = client.post(url=url,headers=oauth_header,json=body)
#     assert response.status_code == status.HTTP_201_CREATED

def test_read_user_info(oauth_header):
    url = "/user"
    response = client.get(url=url,headers=oauth_header)
    assert response.status_code == status.HTTP_200_OK
    info = response.json()
    assert type(info["username"]) == str
    assert type(info["realname"]) == str
    assert type(info["phone"]) == str
    assert type(info["car"]) == str