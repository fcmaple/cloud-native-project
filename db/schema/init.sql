\c cloudb

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(55) NOT NULL UNIQUE,
  realname VARCHAR(55) NOT NULL,
  password VARCHAR(300) NOT NULL,
  phone VARCHAR(55) NOT NULL,
  car VARCHAR(55)
);

CREATE TABLE trips (
  trip_id SERIAL PRIMARY KEY,
  user_id INT REFERENCES users(user_id),
  departure INT,
  destination INT,
  boarding_time TIMESTAMP NOT NULL,
  alighting_time TIMESTAMP,
  available_seats INT NOT NULL,
  UNIQUE (user_id, boarding_time)
);

CREATE TABLE passengers (
  passenger_id SERIAL PRIMARY KEY,
  trip_id INT REFERENCES trips(trip_id),
  user_id INT REFERENCES users(user_id),
  departure VARCHAR(300) NOT NULL,
  destination VARCHAR(300) NOT NULL,
  cost INT NOT NULL
);


CREATE TABLE locations (
  location_id SERIAL PRIMARY KEY,
  trip_id INT REFERENCES trips(trip_id),
  name VARCHAR(55) NOT NULL,
  time TIMESTAMP NOT NULL
);