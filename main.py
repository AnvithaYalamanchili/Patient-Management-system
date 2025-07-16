from fastapi import FastAPI,Response,HTTPException,status,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import schemas
from sqlalchemy.orm import Session
from database import get_db,engine
import models
from router import patient, user,auth

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


while True:
    try:
        conn=psycopg2.connect(host='localhost',database='patientrcdsys',user='postgres',password='Venu@66691',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print('Database Connection successful')
        break
    except Exception as err:
        print(err)
        time.sleep(2)

app.include_router(patient.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
def root():
    return 'success'
