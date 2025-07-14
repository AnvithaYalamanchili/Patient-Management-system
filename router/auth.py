from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
import models
import utils
import schemas

router=APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user:schemas.PatientUserResponse,db:Session=Depends(get_db)):
    try:
        login=db.query(models.PatientUser).filter(models.PatientUser.email==user.email).first()
        if not login:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
        if not utils.verify(user.password,login.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    except Exception as e:
        print(e)
    return {"token":"example"}
