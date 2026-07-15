from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from schemas import EnrollmentCreate
import crud

app = FastAPI(
    title="Course Enrollment API"
)

Base.metadata.create_all(bind=engine)


# ==========================
# Đăng ký khóa học
# ==========================

@app.post("/enrollments", status_code=201)
def create_enrollment(
        enrollment: EnrollmentCreate,
        db: Session = Depends(get_db)
):

    result = crud.create_enrollment(db, enrollment)

    if result == "student_not_found":
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    if result == "course_not_found":
        raise HTTPException(
            status_code=404,
            detail="Khóa học không tồn tại"
        )

    if result == "student_inactive":
        raise HTTPException(
            status_code=400,
            detail="Sinh viên không hoạt động"
        )

    if result == "course_closed":
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đóng"
        )

    if result == "already_enrolled":
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã đăng ký khóa học"
        )

    if result == "course_full":
        raise HTTPException(
            status_code=400,
            detail="Khóa học đã đủ số lượng"
        )

    return {
        "id": result.id,
        "student_id": result.student_id,
        "course_id": result.course_id,
        "enrolled_at": result.enrolled_at
    }


# ==========================
# Xem khóa học của sinh viên
# ==========================

@app.get("/students/{student_id}/courses")
def get_student_courses(
        student_id: int,
        db: Session = Depends(get_db)
):

    result = crud.get_student_courses(db, student_id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    return result
