from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.prediction_service import prediction_service

router = APIRouter()

@router.post("/predict")
async def predict(
    patient_id: int = Form(...),
    model_type: str = Form("cnn_rnn"), # cnn_rnn or vit
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Read file into bytes
        file_bytes = await file.read()
        return prediction_service.run_prediction(db, patient_id, file_bytes, "cnn_rnn")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict-with-explain")
async def predict_with_explain(
    patient_id: int = Form(...),
    model_type: str = Form("cnn_rnn"),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # For now, it's the same flow, just explicit endpoint naming as requested
    return await predict(patient_id, "cnn_rnn", file, db)
