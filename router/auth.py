from fastapi import FastAPI,APIRouter,Depends,HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
import models
import utils
import schemas
import oauth2

router=APIRouter(tags=["Authentication"])

@router.post('/login')
def login(user:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):

        login=db.query(models.User).filter(models.User.email==user.username).first()
        if not login:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Credentials")
        if not utils.verify(user.password,login.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
        access_token=oauth2.create_access_token(data={"user_id":login.id,"user_role":login.role})
        return {"access_token":access_token,"token_type":"bearer"}
