from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from ..config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
db = SessionLocal()

Base = declarative_base()  # inherit from this class to create ORM models

def get_db_session():
    session = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    db = session()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()