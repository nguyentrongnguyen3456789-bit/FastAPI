from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from Database import get_db, Base, engine
from schemas import UserRequestDTO
import user_services

app = FastAPI(
    title="Manager Users"
)

Base.metadata.create_all(bind=engine)


# Test kết nối Database
@app.get("/test-connection")
def test_connections(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "message": "Ket noi thanh cong"
        }
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Khong the ket noi"
        )


# Thêm User
@app.post("/users", tags=["Users"], status_code=status.HTTP_201_CREATED)
def add_users(user: UserRequestDTO, db: Session = Depends(get_db)):
    db_user = user_services.create_user(db, user)

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Them du lieu khong thanh cong"
        )

    return {
        "status_code": 201,
        "message": "Them thanh cong",
        "data": db_user
    }


# Lấy User theo ID
@app.get("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
def get_users(user_id: int, db: Session = Depends(get_db)):
    db_user = user_services.get_user(db, user_id)

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay du lieu"
        )

    return {
        "status_code": 200,
        "message": "Lay thanh cong",
        "data": db_user
    }


# Cập nhật User
@app.put("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
def update_users(user_id: int, user: UserRequestDTO, db: Session = Depends(get_db)):
    db_user = user_services.update_user(db, user_id, user)

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay du lieu"
        )

    return {
        "status_code": 200,
        "message": "Cap nhat du lieu thanh cong",
        "data": db_user
    }


# Xóa User
@app.delete("/users/{user_id}", tags=["Users"], status_code=status.HTTP_200_OK)
def delete_users(user_id: int, db: Session = Depends(get_db)):
    db_user = user_services.delete_user(db, user_id)

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="Khong tim thay du lieu"
        )

    return {
        "status_code": 200,
        "message": "Xoa du lieu thanh cong",
        "data": db_user
    }