from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel 
from sqlalchemy.orm import Session
from . import get_db
from loguru import logger
from src.db.models import StudentInfo
from typing import Optional

router = APIRouter()


class StudentCreate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    bookcode: Optional[int] = None
    issue_date: Optional[datetime] = None


@router.get("/get_all_stud_info", tags=["View Students"])
def get_all_stud_data(
        db: Session = Depends(get_db)
):
    try:
        res = db.query(StudentInfo).first()
        return {
            "status_code": 200,
            "detail": res
        }
    except Exception as e:
        logger.debug(f"Error Occurred in get_all_stud_data - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")


@router.get("/get_all_stud_id", tags=["View Students"])
def get_stud_by_id(
        id: int,
        db: Session = Depends(get_db)
):
    try:
        res = db.query(StudentInfo).filter_by(id=id).all()
        return {
            "status_code": 200,
            "detail": res
        }
    except Exception as e:
        logger.debug(f"Error Occurred in get_stud_by_id - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")


@router.post("/add_new_student", tags=["Manage Library credentials"])
def add_stud_info(
        info: StudentCreate,
        db: Session = Depends(get_db)
):
    try:
        stud_email = info.email
        stud_exists = db.query(StudentInfo).filter_by(email=stud_email).first()
        if (stud_exists) :
            logger.debug(f"Student Information already Exists - {stud_email}")
            raise HTTPException(status_code=400, detail=f"Student Email - {stud_email} information already exists")
        else:
            stud_add_info = StudentInfo(
                name=info.name,
                email=stud_email,
                bookcode=info.bookcode,
                issue_date=info.issue_date
            )
            db.add(stud_add_info)
            db.commit()
            return{
                "status_code":200,
                "detail":f"Student Name- {stud_email} Information Added Successfully"
            }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.debug(f"Error Occurred in add_stud_info - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")


@router.put("/Update_student_info", tags=["Manage Library credentials"])
def modify_stud_info(
        id: int,
        info: StudentCreate,
        db: Session = Depends(get_db)
):
    try:
        stud_name = info.name
        update_stud_info = db.query(StudentInfo).filter_by(id=id).update(info.dict(exclude_unset=True))
        if update_stud_info:
            db.commit()
            return {
                "status_code": 200,
                "detail": f"Student Name -{stud_name} Information Modified Successfully"
            }
        else:
            logger.debug(f"Student information not exists of Name - {stud_name}")
            raise HTTPException(status_code=400, detail=f"Student Name - {stud_name} information not exists")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.debug(f"Error Occurred in modify_stud_info- {e}")
        raise HTTPException(status_code=500, detail=f"{e}")


@router.delete("/delete_student", tags=["Manage Library credentials"])
def delete_stud_info(
        id: int,
        db: Session = Depends(get_db)
):
    try:
        res = db.query(StudentInfo).filter_by(id=id).all()
        if len(res) > 0:
            db.delete(res[0])
            db.commit()
            return {
                "status_code": 200,
                "detail": f"Student_id - {id} Information Deleted Successfully"
            }
        else:
            logger.debug(f"Student information not exists of student id - {id}")
            raise HTTPException(status_code=400, detail=f"Student id - {id} information not exists")
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.debug(f"Error Occurred in delete_stud_info - {e}")
        raise HTTPException(status_code=500, detail=f"{e}")
