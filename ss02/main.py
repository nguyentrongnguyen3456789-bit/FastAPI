from fastapi import FastAPI
# import giúp kiểm soát dữ liệu
from pydantic import BaseModel

app = FastAPI(
    title="Quản lý sinh viên",
    description="đây là API quản lý sinh viên sinh viên đá bóng hay nhất thế giới",
    version="1.0.0",
)

class StudentSchema(BaseModel):
    email: str
    password: str
    age: int
student_database = {
    1 : {"email": "trongnguyen@gmail", "password" : "123", "age":"18"},
    2 : {"email": "nguyen@gmail", "password" : "456", "age":"18"},
}
# tạo api để lấy ds sinh viên
@app.get("/students")
def get_all_students():
    return list(student_database.values())
# tạo api dùng để thêm sinh viên  
@app.post("/students", tags=["Students"], summary="Thêm sinh viên")
def create_students(student: StudentSchema):
    studen_id = len(student_database) + 1
    new_student ={
        "email": student.email,
        "password": student.password,
        "age": student.age
    }
    student_database[studen_id] = new_student
    return new_student
# tạo api cơ bản
# decorator
@app.get("/")
def get_root():
    return {"message": "lấy dữ liệu thành công!"}