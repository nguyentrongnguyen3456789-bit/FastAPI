from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional, Any, Literal
from datetime import datetime, timezone

app = FastAPI(
    title="Team Task Manager API"
)

tasks_db = [
    {
        "id": 1,
        "title": "Thiet ke database Shop AI",
        "description": "Xay dung bang va toi uu index",
        "assignee": "QuyDev",
        "priority": 1,
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2,
        "title": "Code bo API Authen",
        "description": "Trien khai filter verify JWT token",
        "assignee": "FixerQ",
        "priority": 2,
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]


class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str


class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=1)
    priority: int = Field(..., ge=1, le=5)


class TaskStatusUpdateSchema(BaseModel):
    status: Literal[
        "todo",
        "in_progress",
        "done"
    ]


def build_response(
    status_code: int,
    message: str,
    request: Request,
    data=None,
    error=None
):
    return JSONResponse(
        status_code=status_code,
        content=APIResponse(
            statusCode=status_code,
            message=message,
            data=data,
            error=error,
            timestamp=datetime.now(timezone.utc).isoformat(),
            path=request.url.path
        ).model_dump()
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return build_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
        request,
        None,
        "ERR-VAL-422: Validation error at Request Body fields constraint layout."
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(
        request: Request,
        exc: HTTPException
):
    detail = exc.detail

    if isinstance(detail, dict):
        return build_response(
            exc.status_code,
            detail["message"],
            request,
            None,
            detail["error"]
        )

    return build_response(
        exc.status_code,
        str(detail),
        request,
        None,
        None
    )


@app.exception_handler(Exception)
async def global_exception_handler(
        request: Request,
        exc: Exception
):
    return build_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "Lỗi hệ thống. Vui lòng thử lại sau!",
        request,
        None,
        "ERR-500: Internal Server Error."
    )
@app.get("/tasks")
async def get_all_tasks(
    request: Request,
    status: Optional[str] = None
):
    if status:
        data = [
            task for task in tasks_db
            if task["status"] == status
        ]
    else:
        data = tasks_db

    return build_response(
        status.HTTP_200_OK,
        "Lấy danh sách công việc thành công!",
        request,
        data
    )


@app.post("/tasks")
async def create_task(
    request: Request,
    task_in: TaskCreateSchema
):
    for task in tasks_db:
        if task["title"].lower() == task_in.title.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!",
                    "error": "ERR-TASK-01: Task conflict: Title field duplicates an existing record."
                }
            )

    new_id = 1

    if tasks_db:
        new_id = max(task["id"] for task in tasks_db) + 1

    new_task = {
        "id": new_id,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee.strip(),
        "priority": task_in.priority,
        "status": "todo",
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    tasks_db.append(new_task)

    return build_response(
        status.HTTP_201_CREATED,
        "Khởi tạo công việc mới thành công!",
        request,
        new_task
    )
@app.put("/tasks/{task_id}")
async def update_task_status(
    task_id: int,
    status_in: TaskStatusUpdateSchema,
    request: Request
):
    task = next((item for item in tasks_db if item["id"] == task_id), None)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Lỗi: Không tìm thấy công việc!",
                "error": "ERR-TASK-03: Task not found."
            }
        )

    if task["status"] == "done":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Lỗi: Công việc đã hoàn thành, không thể cập nhật trạng thái!",
                "error": "ERR-TASK-04: Completed task cannot be updated."
            }
        )

    task["status"] = status_in.status

    return build_response(
        status.HTTP_200_OK,
        "Cập nhật tiến độ công việc thành công!",
        request,
        task
    )
def calculate_team_metrics():
    total_tasks = len(tasks_db)

    completed_tasks = sum(
        1 for task in tasks_db
        if task["status"] == "done"
    )

    completion_rate_percentage = 0.0

    if total_tasks > 0:
        completion_rate_percentage = round(
            (completed_tasks / total_tasks) * 100,
            2
        )

    return (
        total_tasks,
        completed_tasks,
        completion_rate_percentage
    )


@app.get("/tasks/analytics/dashboard")
async def get_dashboard_analytics(
    request: Request
):
    total_tasks, completed_tasks, completion_rate_percentage = calculate_team_metrics()

    dashboard = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate_percentage": completion_rate_percentage
    }

    return build_response(
        status.HTTP_200_OK,
        "Lấy số liệu thống kê hiệu suất nhóm thành công!",
        request,
        dashboard
    )