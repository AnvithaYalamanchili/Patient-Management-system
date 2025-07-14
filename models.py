from database import Base
from sqlalchemy import Column, Integer, String, Date

class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)
    email = Column(String(255), nullable=False)
    phone_number = Column(String(15), nullable=False)
    diagnosis = Column(String(255), nullable=False)
    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date, nullable=True)

class PatientUser(Base):
    __tablename__='patientUser'

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)