from pydantic import BaseModel,EmailStr
from datetime import date

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

class PatientUser(BaseModel):
    name:str
    email:EmailStr
    password:str

class PatientUserResponse(BaseModel):
    name:str
    email:EmailStr
    password:str
    class Config:
        orm_mode=True
        pass