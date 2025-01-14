import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from os import getcwd
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from loguru import logger

engine = None
Base = declarative_base()
DBSession: sessionmaker = None


def init_db():
    try:
        global DBSession
        engine = create_engine(f"sqlite:///{getcwd()}/config/student.db")
        conn = engine.connect()
        conn.close()
        Base.metadata.create_all(engine)
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        return True
    except Exception as e:
        logger.error(f"Error Occurred in init_db - {e}")
        return False


def get_session():
    if DBSession is not None:
        session = DBSession()
        return session
    else:
        return None


class StudentInfo(Base):
    __tablename__ = "stud"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    bookcode = Column(Integer, nullable=True)
    issue_date = Column(DateTime, nullable=True)
