import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from ..db.models import trips_table,users_table
from ..config import settings
def args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--update_name','-n',type=str,required=True,help='item name')
    parser.add_argument('--id','-i',type=int,help='trip ID or user ID')
    parser.add_argument('--update_key','-k',type=str,required=True,help='key')
    parser.add_argument('--update_value','-v',type=str,required=True,help='value')
    return parser.parse_args()
def get_session():
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    return session

class SQLSession:
    def __init__(self,session: Session):
        self.db = session
    def update_user(self,id: int, _update_data: dict) -> int:
        try:
            res = self.db.query(users_table).filter_by(user_id=id).update(_update_data)
            self.db.commit()
            return 1 if res == 1 else 0
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    def update_trip(self, id: int, _update_data: dict) -> int:
        try:
            res = self.db.query(trips_table).filter_by(trip_id=id).update(_update_data)
            self.db.commit()
            return 1 if res == 1 else 0
        except Exception as exc:
            print(exc.__class__.__name__, end=": ")
            print(str(exc))
            return str(exc)
    # def close(self):
    #     self.db.close()
if __name__ == '__main__':
    args=args_parser()
    print(args)
    session = get_session()
    sql = SQLSession(session=session)
    if args.update_name == 'user':
        a = sql.update_user(args.id,{args.update_key:args.update_value})
    elif args.update_name == 'trip':
        a = sql.update_trip(args.id,{args.update_key:args.update_value})
    print(a)
    # sql.close()