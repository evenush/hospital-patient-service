from pydantic import BaseModel, EmailStr, ConfigDict


class PatientCreate(BaseModel):

    name: str
    age: int
    gender: str
    phone: str
    email: EmailStr


class PatientResponse(PatientCreate):

    id: int

    model_config = ConfigDict(
        from_attributes=True
    )