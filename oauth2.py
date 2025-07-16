from jose import JWTError,jwt
from datetime import datetime,timedelta
import schemas
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException,status
from database import get_db
import models
from fastapi.security.oauth2 import OAuth2PasswordBearer


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login")
SECRET_KEY="anvitha"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    print("🔑 Token received:", token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("📦 Payload decoded:", payload)
        id: str = payload.get("user_id")
        if id is None:
            print("❌ user_id not found in token payload")
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError as e:
        print("❌ JWTError occurred:", e)
        raise credentials_exception
    return token_data


def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    token_data=verify_access_token(token,credentials_exception)
    print(f"token_data in get_current user {token_data}")
    user=db.query(models.User).filter(models.User.id==token_data.id).first()
    return user
