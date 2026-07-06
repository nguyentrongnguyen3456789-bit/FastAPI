from fastapi import FastAPI, HTTPException, Request
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

courses_db = [
    {"id": 1, "course_name": "FastAPI Masterclass", "duration_hours": 32, "price": 1500000, "status": "active", "created_at": "2026-07-01T02:00:00Z"},
    {"id": 2, "course_name": "NextJS Next-Level", "duration_hours": 45, "price": 1800000, "status": "active", "created_at": "2026-07-01T03:15:00Z"}
]

class CourseCreate(BaseModel):
    course_name: str
    duration_hours: int
    price: int

def response_template(status_code:int, message:str, data=None, error=None, path:str=""):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "path": path
    }

@app.get("/courses")
def get_courses(request: Request):
    return response_template(
        200,
        "Lấy danh sách khóa học thành công!",
        data=courses_db,
        path=str(request.url.path)
    )

@app.post("/courses")
def create_course(course: CourseCreate, request: Request):
    for c in courses_db:
        if c.get("course_name").lower() == course.course_name.lower():
            raise HTTPException(
                status_code=400,
                detail=response_template(
                    400,
                    "Lỗi: Tên khóa học này đã tồn tại trong danh mục đào tạo!",
                    data=None,
                    error="ERR-EDU-01",
                    path=str(request.url.path)
                )
            )

    new_id = max(c.get("id") for c in courses_db) + 1
    new_course = {
        "id": new_id,
        "course_name": course.course_name,
        "duration_hours": course.duration_hours,
        "price": course.price,
        "status": "active",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    courses_db.append(new_course)
    return response_template(
        201,
        "Tạo mới khóa học thành công!",
        data=new_course,
        path=str(request.url.path)
    )


@app.delete("/courses/{course_id}")
def delete_course(course_id: int, request: Request):
    for c in courses_db:
        if c.get("id") == course_id:
            courses_db.remove(c)
            return response_template(
                200,
                "Xóa khóa học thành công!",
                data=None,
                path=str(request.url.path)
            )
    raise HTTPException(
        status_code=404,
        detail=response_template(
            404,
            "Lỗi: Không tìm thấy mã khóa học yêu cầu để xóa!",
            data=None,
            error="ERR-EDU-02: Target course ID can not be found.",
            path=str(request.url.path)
        )
    )
