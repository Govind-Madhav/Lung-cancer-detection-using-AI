from sqlalchemy.orm import Session
from app.db import crud
from app.schemas import patient as patient_schema

class PatientService:
    @staticmethod
    def create_patient(db: Session, patient: patient_schema.PatientCreate):
        return crud.create_patient(db, patient)

    @staticmethod
    def get_patient(db: Session, patient_id: int):
        return crud.get_patient(db, patient_id)

patient_service = PatientService()
