from sqlalchemy import Column, Integer, String
from database import Base


class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String(100), nullable=False)

    age = Column(Integer)

    gender = Column(String(20))

    phone = Column(String(15))

    email = Column(
        String(100),
        unique=True,
        index=True
    )