from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime

from Database import Base, engine, get_db
from schemas import DeviceRequestDTO
import device_services

app = FastAPI(
    title="TechRent Device Management API"
)

Base.metadata.create_all(bind=engine)


# =======================
# Response thành công
# =======================
def success_response(
    status_code: int,
    message: str,
    data,
    request: Request
):
    return {
        "statusCode": status_code,
        "data": data,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "path": request.url.path,
        "error": None
    }


# =======================
# Exception Handler
# =======================
@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "statusCode": exc.status_code,
            "data": None,
            "message": str(exc.detail),
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path,
            "error": str(exc.detail)
        }
    )


# =======================
# GET /devices
# =======================
@app.get("/devices")
def get_devices(
    request: Request,
    category: str = None,
    status: str = None,
    sort_by: str = None,
    order: str = "asc",
    db: Session = Depends(get_db)
):

    devices = device_services.get_all_devices(
        db,
        category,
        status,
        sort_by,
        order
    )

    return success_response(
        200,
        "Get device list successfully",
        devices,
        request
    )


# =======================
# GET /devices/{device_id}
# =======================
@app.get("/devices/{device_id}")
def get_device(
    device_id: str,
    request: Request,
    db: Session = Depends(get_db)
):

    device = device_services.get_device(
        db,
        device_id
    )

    if not device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return success_response(
        200,
        "Get device successfully",
        device,
        request
    )


# =======================
# POST /devices
# =======================
@app.post(
    "/devices",
    status_code=status.HTTP_201_CREATED
)
def create_device(
    device: DeviceRequestDTO,
    request: Request,
    db: Session = Depends(get_db)
):

    new_device = device_services.create_device(
        db,
        device
    )

    if new_device is None:
        raise HTTPException(
            status_code=409,
            detail="Device ID already exists"
        )

    return success_response(
        201,
        "Create device successfully",
        new_device,
        request
    )


# =======================
# PUT /devices/{device_id}
# =======================
@app.put("/devices/{device_id}")
def update_device(
    device_id: str,
    device: DeviceRequestDTO,
    request: Request,
    db: Session = Depends(get_db)
):

    db_device = device_services.update_device(
        db,
        device_id,
        device
    )

    if not db_device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return success_response(
        200,
        "Update device successfully",
        db_device,
        request
    )


# =======================
# DELETE /devices/{device_id}
# =======================
@app.delete("/devices/{device_id}")
def delete_device(
    device_id: str,
    request: Request,
    db: Session = Depends(get_db)
):

    db_device = device_services.delete_device(
        db,
        device_id
    )

    if not db_device:
        raise HTTPException(
            status_code=404,
            detail="Device not found"
        )

    return success_response(
        200,
        "Delete device successfully",
        db_device,
        request
    )