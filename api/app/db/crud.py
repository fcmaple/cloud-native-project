from sqlalchemy.orm import Session
from .database import get_db_session
from .models import users_table, trips_table, passengers_table, locations_table
from typing import Annotated, List

def get_db():
    _db = next(get_db_session())
    try:
        yield process_data(_db)
    finally:
        _db.close()
class process_data():

    def __init__(self, db: Session):
        self.db = db
        
    # def get_trips_data_from_users_info(self, id: int):
    #     res = self.db.query(users_table, trips_table).join(trips_table, users_table.username==trips_table.username).filter_by(driver_id=id).all()
    #     self.db.commit()
    #     for s, t in res:
    #         print(t.trip_id, t.departure, t.destination, t.available_seats)
    
    '''
        Section of insert data
    '''
    
    def insert_data_users(self, input_data: dict) -> str:
        try:
            inserted_data = users_table(**input_data)
            self.db.add(inserted_data)
            self.db.commit()
            return "SUCCESS"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def insert_data_trips(self, input_data: dict) -> str:
        try:
            inserted_data = trips_table(**input_data)
            self.db.add(inserted_data)
            self.db.commit()
            return "SUCCESS"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def insert_data_passengers(self, input_data: dict) -> str:
        try:
            inserted_data = passengers_table(**input_data)
            self.db.add(inserted_data)
            self.db.commit()
            return "SUCCESS"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def insert_data_locations(self, input_data: dict) -> str:
        try:
            inserted_data = locations_table(**input_data)
            self.db.add(inserted_data)
            self.db.commit()
            return "SUCCESS"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    
    '''
        Section of get data
    '''
    def get_data_users_byid(self, id: int):
        try:
            data = self.db.query(users_table).filter_by(user_id=id)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table users" if len(_dict) == 0 else _dict[0] 
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    
    def get_data_users(self, user_name: str):
        try:
            data = self.db.query(users_table).filter_by(username=user_name)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table users" if len(_dict) == 0 else _dict[0] 
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def get_data_tripid(self, _data: dict):
        try:
            data = self.db.query(trips_table).filter_by(user_id=_data['user_id'], available_seats=_data['available_seats'], boarding_time=_data['boarding_time'])
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table trips" if len(_dict) == 0 else _dict[0]
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    
    def get_data_trips_by_userid(self, id: int):
        try:
            data = self.db.query(trips_table).filter_by(user_id=id)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table trips" if len(_dict) == 0 else _dict
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)

    def get_data_trips(self, id: int):
        try:
            data = self.db.query(trips_table).filter_by(trip_id=id)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table trips" if len(_dict) == 0 else _dict
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def get_data_passengers_userid(self, id: int):
        try:
            data = self.db.query(passengers_table).filter_by(user_id=id)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table passengers" if len(_dict) == 0 else _dict
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def get_data_passengers(self, id: int):
        try:
            data = self.db.query(passengers_table).filter_by(trip_id=id)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table passengers" if len(_dict) == 0 else _dict
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def get_data_locations_info_by_name(self, _name: str, _id: Annotated[int,None] = None):
        try:
            if _id == None:
                data = self.db.query(locations_table).filter_by(name=_name)
                self.db.commit()
            else:
                data = self.db.query(locations_table).filter_by(name=_name, trip_id=_id)
                self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table trips" if len(_dict) == 0 else _dict
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def get_data_locationsid(self, id: int, _name: str):
        try:
            data = self.db.query(locations_table).filter_by(trip_id=id, name=_name)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table trips" if len(_dict) == 0 else _dict[0]
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def get_data_locations(self, id: int):
        try:
            data = self.db.query(locations_table).filter_by(trip_id=id)
            self.db.commit()
            _dict = [d.__dict__ for d in data]
            return "ERROR: input id not in table locations" if len(_dict) == 0 else _dict
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    
    '''
        Section of update data
    '''
    
    def update_data_users(self, id: int, _update_data: dict) -> str:
        try:
            res = self.db.query(users_table).filter_by(user_id=id).update(_update_data)
            self.db.commit()
            return "SUCCESS" if res == 1 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    
    def update_data_trips(self, id: int, _update_data: dict) -> str:
        try:
            res = self.db.query(trips_table).filter_by(trip_id=id).update(_update_data)
            self.db.commit()
            return "SUCCESS" if res == 1 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    
    def update_data_passengers(self, id: int, _update_data: dict) -> str:
        try:
            res = r = self.db.query(passengers_table).filter_by(passenger_id=id).update(_update_data)
            self.db.commit()
            return "SUCCESS" if res == 1 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    
    def update_data_locations(self, id: int, _update_data: dict) -> str:
        try:
            res = self.db.query(locations_table).filter_by(location_id=id).update(_update_data)
            self.db.commit()
            return "SUCCESS" if res == 1 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    '''
        Section of update data
    '''
    
    def delete_data_users(self, id: int) -> str:
        try:
            res = self.db.query(users_table).filter_by(user_id=id).delete()
            self.db.commit()
            return "SUCCESS" if res == 1 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def delete_data_trips(self, id: int) -> str:
        try:
            res = self.db.query(trips_table).filter_by(trip_id=id).delete()
            self.db.commit()
            return "SUCCESS" if res >= 0 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def delete_data_passengers(self, _trip_id: int) -> str:
        try:
            res = self.db.query(passengers_table).filter_by(trip_id=_trip_id).delete()
            self.db.commit()
            return "SUCCESS" if res >= 0 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)

    def delete_data_passengers_by_trip_user_id(self, _trip_id: int, _user_id: int) -> str:
        try:
            res = self.db.query(passengers_table).filter_by(trip_id=_trip_id, user_id=_user_id).delete()
            self.db.commit()
            return "SUCCESS" if res >= 0 else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
        
    def delete_data_locations(self, id: int) -> str:
        try:
            res = self.db.query(locations_table).filter_by(trip_id=id).delete()
            print('-'*20)
            print(res)
            print('-'*20)

            self.db.commit()
            return "SUCCESS" if res >= 0  else "ERROR"
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)

if __name__ == '__main__':
    _db = next(get_db_session())
    sheng_db = process_data(_db)
    
    '''
        test
    '''
    data_user = {"username":"sheng", "password":"1229", "phone":"0979815546"}
    # a = sheng_db.insert_data_users(data_user)
    # print(a)
    # data["username"] = "sheng, chen"
    # a = sheng_db.update_data_users(311551038, data)
    # print(a)
    a = sheng_db.get_data_users("dave")
    print(a)
    # a = sheng_db.delete_data_users(311551038)
    # print(a)
    # a = sheng_db.get_data_users(311551038)
    # print(a)
    # data_trip_1 = {"driver_id":311551038, "departure":2, "destination":9, "available_seats":4}
    # data_trip_2 = {"driver_id":311551038, "departure":1, "destination":2, "available_seats":4}
    # a = sheng_db.insert_data_trips(data_trip_1)
    # a = sheng_db.insert_data_trips(data_trip_2)
    # print(a)
    # a = sheng_db.get_data_trips(1)
    # print(a)
    # sheng_db.get_trips_data_from_users_info(311551038)