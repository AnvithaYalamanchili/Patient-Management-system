from pydantic import BaseModel
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