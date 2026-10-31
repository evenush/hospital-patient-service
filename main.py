from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import engine, get_db
from schemas import PatientCreate, PatientResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Patient Service",
    version="1.0"
)


@app.get("/")
def home():
    return {
        "message": "Patient Service is running"
    }


@app.post(
    "/patients",
    response_model=PatientResponse
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(models.Patient).filter(
        models.Patient.email == patient.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Patient already exists"
        )

    new_patient = models.Patient(
        **patient.model_dump()
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


@app.get("/patients")
def get_patients(
    db: Session = Depends(get_db)
):

    return db.query(models.Patient).all()


@app.get("/patients/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    return patient


@app.delete("/patients/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):

    patient = db.query(models.Patient).filter(
        models.Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    db.delete(patient)
    db.commit()

    return {
        "message": "Patient deleted successfully"
    }