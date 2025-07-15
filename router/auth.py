from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
import models
import utils
import schemas
import oauth2

router=APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user:schemas.PatientUserResponse,db:Session=Depends(get_db)):

        login=db.query(models.PatientUser).filter(models.PatientUser.email==user.email).first()
        if not login:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
        if not utils.verify(user.password,login.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
        access_token=oauth2.create_access_token(data={"user_id":login.id})
        return {"access_token":access_token,"token_type":"bearer"}
