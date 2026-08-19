from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.middleware import authorization_middleware


app = FastAPI()


# =========================
# CẤU HÌNH CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://internal.megamart.com"
    ],
    allow_methods=[
        "GET",
        "POST"
    ],
    allow_headers=[
        "Content-Type",
        "X-User-Role"
    ],
)


# =========================
# CUSTOM MIDDLEWARE
# =========================

app.middleware("http")(authorization_middleware)


# =========================
# API TEST
# =========================

@app.get("/api/v1/salary/modify")
def modify_salary():
    return {
        "message": "Salary modification page"
    }


@app.get("/api/v1/system/settings")
def system_settings():
    return {
        "message": "System settings"
    }


@app.get("/api/v1/profile")
def profile():
    return {
        "message": "Personal profile"
    }