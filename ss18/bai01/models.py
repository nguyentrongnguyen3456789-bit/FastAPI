from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    max_students = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)

    enrollments = relationship(
        "Enrollment",
        back_populates="course"
    )


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    enrolled_at = Column(DateTime, nullable=False)

    student = relationship(
        "Student",
        back_populates="enrollments"
    )

    course = relationship(
        "Course",
        back_populates="enrollments"
    )
