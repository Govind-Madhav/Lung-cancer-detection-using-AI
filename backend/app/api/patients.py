from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.patient_service import patient_service
from app.schemas import patient as patient_schema

router = APIRouter()

@router.post("/patients", response_model=patient_schema.Patient)
def create_patient(patient: patient_schema.PatientCreate, db: Session = Depends(get_db)):
    return patient_service.create_patient(db, patient)

@router.get("/patients/{patient_id}", response_model=patient_schema.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return patient_service.get_patient(db, patient_id)
