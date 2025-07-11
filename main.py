from fastapi import FastAPI,Response,HTTPException,status,Depends
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import schemas
from sqlalchemy.orm import Session
from database import get_db,engine
import models

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


@app.get('/')
def root():
    return 'success'

@app.get('/patients')
def get_patients(db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM patient""")
    # patients=cursor.fetchall()
    patients=db.query(models.Patient).all()

    return {'patient data': patients}

@app.get('/patient/{id}')
def get_patient(id:int,response:Response,db:Session=Depends(get_db)):
    # cursor.execute("""SELECT * FROM patient WHERE id=%s""",(str(id)))
    # patient=cursor.fetchone()
    patient=db.query(models.Patient).filter(models.Patient.id==id).first()
    if not patient:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'The patient with id {id} not found')
    return {f'patient data with id:{id}':patient}

@app.post('/patient',status_code=status.HTTP_201_CREATED)
def create_patient(patient:schemas.Patient,db:Session=Depends(get_db)):
    try:
        # cursor.execute("""INSERT INTO patient (name,age,gender,email,phone_number,diagnosis,admission_date,discharge_date) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) RETURNING * """,(patient.name,patient.age,patient.gender,patient.email,patient.phone_number,patient.diagnosis,patient.admission_date,patient.discharge_date))
        # new_patient=cursor.fetchone()
        # conn.commit()
        new_patient=models.Patient(**patient.dict())
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return {"Patient added successfully":new_patient}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to insert patient")
    
@app.put('/patient/{id}')
def update_patient(id:int,patient:schemas.Patient,db:Session=Depends(get_db)):
    try:
        # cursor.execute("""UPDATE patient SET name=%s , age=%s, gender=%s, email=%s, phone_number=%s, diagnosis=%s,admission_date=%s,discharge_date=%s WHERE id= %s RETURNING * """,
        #                (patient.name,patient.age,patient.gender,patient.email,patient.phone_number,patient.diagnosis,patient.admission_date,patient.discharge_date,str(id)))
        # updated_patient=cursor.fetchone()
        # conn.commit()
        updated_patient=db.query(models.Patient).filter(models.Patient.id==id).first()
        if update_patient == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = 'Patient not found')
        db.query(models.Patient).filter(models.Patient.id == id).update(patient.dict(),synchronize_session=False)
        db.commit()
        return {"Patient updated successfully":updated_patient}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to update patient data")

@app.delete('/patient/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id:int,db:Session=Depends(get_db)):
    try:
        # cursor.execute("DELETE FROM patient WHERE id=%s RETURNING *",str(id))
        # deleted_patient=cursor.fetchone()
        # conn.commit()
        deleted_patient=db.query(models.Patient).filter(models.Patient.id==id)
        if deleted_patient.first()==None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Patient with id {id} not found")
        deleted_patient.delete(synchronize_session=False)
        db.commit()
        return {f'Patient with id {id} deleted successfully':deleted_patient}
    except Exception as e:
        conn.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to delete patient.")
