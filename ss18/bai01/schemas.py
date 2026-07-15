from pydantic import BaseModel


# ==========================
# Student
# ==========================

class StudentCreate(BaseModel):
    full_name: str
    status: str


# ==========================
# Course
# ==========================

class CourseCreate(BaseModel):
    name: str
    max_students: int
    status: str


# ==========================
# Enrollment
# ==========================

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int
