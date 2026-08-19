from fastapi import Request
from fastapi.responses import JSONResponse


# Quyền của từng API
ROLE_PERMISSIONS = {
    "/api/v1/salary/modify": ["ADMIN", "HR"],
    "/api/v1/system/settings": ["ADMIN"],
    "/api/v1/profile": ["ADMIN", "HR", "STAFF"],
}


async def authorization_middleware(request: Request, call_next):
    path = request.url.path

    # Chỉ kiểm tra những API nằm trong danh sách cần bảo vệ
    if path in ROLE_PERMISSIONS:

        # Lấy role từ Header X-User-Role
        user_role = request.headers.get("X-User-Role")

        # Không có role hoặc role không có quyền
        if user_role not in ROLE_PERMISSIONS[path]:
            return JSONResponse(
                status_code=403,
                content={
                    "error": "Permission Denied"
                },
            )

    # Nếu hợp lệ thì cho request đi tiếp
    response = await call_next(request)

    return response