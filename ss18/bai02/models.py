from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    student_code = Column(String(50), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    status = Column(String(30), nullable=False)

    registrations = relationship(
        "Registration",
        back_populates="student"
    )


class Workshop(Base):
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    maximum_participants = Column(Integer, nullable=False)
    status = Column(String(30), nullable=False)
    start_time = Column(DateTime, nullable=False)

    registrations = relationship(
        "Registration",
        back_populates="workshop"
    )


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    workshop_id = Column(
        Integer,
        ForeignKey("workshops.id"),
        nullable=False
    )

    registered_at = Column(DateTime, nullable=False)

    status = Column(String(30), nullable=False)

    student = relationship(
        "Student",
        back_populates="registrations"
    )

    workshop = relationship(
        "Workshop",
        back_populates="registrations"
    )
