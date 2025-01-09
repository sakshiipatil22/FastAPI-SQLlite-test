from influxdb_client import UserResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,HTTPException
from typing import List




app=FastAPI()


DATABASE_URL="sqlite:///./test.db"

engine=create_engine(DATABASE_URL, connect_args={"check_same_thread":False})

SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    name=Column(String, index=True)
    email=Column(String, unique=True, index=True)


Base.metadata.create_all(bind=engine)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
class UserCreate(BaseModel):
    name=str
    email=str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

    class Config:
        orm_mode=True

@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate,db:Session=Depends(get_db)):
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserResponse])
def read_users(skip:int=0, limit:int=10, db: Session =Depends(get_db)):
    users =db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id:int, db:Session= Depends(get_db)):
    user =db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
