from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from schemas import StudentCreate, WorkshopCreate, RegistrationCreate
import crud
import models

app = FastAPI(
    title="Workshop Registration API"
)

Base.metadata.create_all(bind=engine)


# ==========================
# Student
# ==========================

@app.post("/students", status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    return {
        "message": "Tạo sinh viên thành công",
        "data": crud.create_student(db, student)
    }


@app.get("/students", status_code=200)
def get_all_students(db: Session = Depends(get_db)):
    return {
        "message": "Lấy danh sách sinh viên thành công",
        "data": crud.get_all_students(db)
    }


# ==========================
# Workshop
# ==========================

@app.post("/workshops", status_code=201)
def create_workshop(workshop: WorkshopCreate, db: Session = Depends(get_db)):
    return {
        "message": "Tạo workshop thành công",
        "data": crud.create_workshop(db, workshop)
    }


@app.get("/workshops", status_code=200)
def get_all_workshops(db: Session = Depends(get_db)):
    return {
        "message": "Lấy danh sách workshop thành công",
        "data": crud.get_all_workshops(db)
    }


@app.get("/workshops/{id}", status_code=200)
def get_workshop(id: int, db: Session = Depends(get_db)):

    workshop = crud.get_workshop_by_id(db, id)

    if not workshop:
        raise HTTPException(
            status_code=404,
            detail="Workshop không tồn tại"
        )

    return {
        "message": "Lấy chi tiết workshop thành công",
        "data": workshop
    }


# ==========================
# Registration
# ==========================

@app.post("/registrations", status_code=201)
def register_workshop(
        registration: RegistrationCreate,
        db: Session = Depends(get_db)
):

    result = crud.register_workshop(db, registration)

    if result == "student_not_found":
        raise HTTPException(
            status_code=404,
            detail="Sinh viên không tồn tại"
        )

    if result == "workshop_not_found":
        raise HTTPException(
            status_code=404,
            detail="Workshop không tồn tại"
        )

    if result == "workshop_closed":
        raise HTTPException(
            status_code=400,
            detail="Workshop đã đóng"
        )

    if result == "already_registered":
        raise HTTPException(
            status_code=400,
            detail="Sinh viên đã đăng ký workshop này"
        )

    if result == "workshop_full":
        raise HTTPException(
            status_code=400,
            detail="Workshop đã đủ số lượng"
        )

    return {
        "message": "Đăng ký workshop thành công",
        "data": result
    }


@app.get("/students/{id}/workshops", status_code=200)
def get_student_workshops(
        id: int,
        db: Session = Depends(get_db)
):

    return {
        "message": "Lấy danh sách workshop của sinh viên thành công",
        "data": crud.get_student_workshops(db, id)
    }


@app.get("/workshops/{id}/students", status_code=200)
def get_workshop_students(
        id: int,
        db: Session = Depends(get_db)
):

    return {
        "message": "Lấy danh sách sinh viên của workshop thành công",
        "data": crud.get_workshop_students(db, id)
    }


@app.delete("/registrations/{id}", status_code=200)
def cancel_registration(
        id: int,
        db: Session = Depends(get_db)
):

    registration = crud.cancel_registration(db, id)

    if not registration:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đăng ký"
        )

    return {
        "message": "Hủy đăng ký thành công"
    }
