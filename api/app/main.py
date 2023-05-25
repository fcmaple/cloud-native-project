from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes.user import router as user_router
from .routes.passenger import router as passenger_router
from .routes.driver import router as driver_router
from .routes.trip import router as trip_router

tags_metadata = [
    {
        "name": "passenger",
        "description": "Operations with specific passenger",
    },
    {
        "name": "driver",
        "description": "Operations with specific driver",
    },
    {
        "name": "user",
        "description": "Operations with specific user",
    },
    {
        "name": "trip",
        "description": "Operations with all trips",
    }
]

app = FastAPI(openapi_tags=tags_metadata)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(passenger_router)
app.include_router(driver_router)
app.include_router(trip_router)

@app.get("/")
def welcome():
    return "It works"
