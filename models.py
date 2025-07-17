from database import Base
from sqlalchemy import Column, Integer, String, Date,ForeignKey

class Patient(Base):
    __tablename__ = 'patient'

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(1), nullable=False)
    email = Column(String(255), nullable=False,unique=True)
    phone_number = Column(String(15), nullable=False,unique=True)
    diagnosis = Column(String(255), nullable=False)
    admission_date = Column(Date, nullable=False)
    discharge_date = Column(Date, nullable=True)
    managed_by_id=Column(Integer,ForeignKey("user.id",ondelete='SET NULL'),nullable=True)

class User(Base):
    __tablename__='user'

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    role=Column(String,nullable=False)