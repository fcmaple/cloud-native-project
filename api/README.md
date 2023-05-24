# cloud-native-project-api


## How to use
### Docker

1. `docker build -t fast:v0.1 .`
2. `docker-compose up -d`

### Process
1. create a virtual environment to api
2. `pip install -r requirements.txt`
3. `uvicorn main:app --host 0.0.0.0 --port 8888`

Then connect `[ip]:8888/docs`, you could see the FastAPI

