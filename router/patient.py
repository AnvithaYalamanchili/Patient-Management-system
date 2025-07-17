from fastapi import FastAPI,Response,HTTPException,status,Depends,APIRouter
import psycopg2
from psycopg2.extras import RealDictCursor
import time
import schemas
from sqlalchemy.orm import Session
from database import get_db,engine
import models
import oauth2

router=APIRouter(tags=['Patients'])

@router.get('/patients',)
def get_patients(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM patient""")
    # patients=cursor.fetchall()
    patients=db.query(models.Patient).all()

    return {'patient data': patients}

@router.get('/patient/{id}')
def get_patient(id:int,response:Response,db:Session=Depends(get_db),):
    # cursor.execute("""SELECT * FROM patient WHERE id=%s""",(str(id)))
    # patient=cursor.fetchone()
    patient=db.query(models.Patient).filter(models.Patient.id==id).first()
    if not patient:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f'The patient with id {id} not found')
    return {f'patient data with id:{id}':patient}

@router.post('/patient', status_code=status.HTTP_201_CREATED, response_model=schemas.PatientResponse)
def create_patient(patient: schemas.Patient, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        print("Current user role:", current_user.role)  

        if current_user.role.strip().lower() != "doctor":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to create patient only doctor can create patient"
            )

        new_patient = models.Patient(**patient.dict(), managed_by_id=current_user.id)
        db.add(new_patient)
        db.commit()
        db.refresh(new_patient)
        return new_patient

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        print("Error:", str(e))  # Optional debug
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to insert patient"
        )

@router.put('/patient/{id}')
def update_patient(id:int,patient:schemas.Patient,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
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
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to update patient data")

@router.delete('/patient/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(id:int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
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
        db.rollback()
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Failed to delete patient.")

