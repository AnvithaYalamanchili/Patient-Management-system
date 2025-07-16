from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List
import schemas
from sqlalchemy.orm import Session
from database import get_db,engine
import models
import utils

router=APIRouter(tags=['Patient (user)'])

@router.get('/user',response_model=List[schemas.UserResponse])
def get_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No users in the table')
    
    return users

@router.get('/user/{id}',response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='No user found')
    
    return user

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(patient:schemas.User,db:Session=Depends(get_db)):
    try:
        hashed_password=utils.hash(patient.password)
        patient.password=hashed_password
        new_user=models.User(**patient.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        if new_user==None:
            raise HTTPException(status.HTTP_204_NO_CONTENT,detail="Provide user details")
        return new_user
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    




