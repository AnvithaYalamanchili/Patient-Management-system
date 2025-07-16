from pydantic import BaseModel,EmailStr
from datetime import date
from typing import Optional

class Patient(BaseModel):
    name:str
    age:int
    gender:str
    email:str
    phone_number:int
    diagnosis:str
    admission_date:date
    discharge_date:date | None=None

class PatientResponse(Patient):
    class Config:
        orm_mode=True
        pass

class User(BaseModel):
    name:str
    email:EmailStr
    password:str
    role:str

class UserResponse(BaseModel):
    name:str
    email:EmailStr
    role:str
    class Config:
        orm_mode=True
        pass

class TokenData(BaseModel):
    id:Optional[int]=None
