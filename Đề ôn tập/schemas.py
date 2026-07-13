from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any
from datetime import datetime


class DeviceRequestDTO(BaseModel):
    id: str = Field(
        min_length=3,
        max_length=20,
        description="Device ID"
    )

    category: str = Field(
        min_length=2,
        max_length=50,
        description="Device Category"
    )

    model: str = Field(
        min_length=2,
        max_length=100,
        description="Device Model"
    )

    rental_rate: float = Field(
        gt=0,
        description="Rental Rate"
    )

    release_year: int = Field(
        ge=2018,
        le=2026,
        description="Release Year"
    )

    status: str = Field(
        default="available"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        allow_status = [
            "available",
            "rented",
            "repairing"
        ]

        if value not in allow_status:
            raise ValueError(
                "Status must be available, rented or repairing"
            )

        return value


class DeviceResponseDTO(BaseModel):
    id: str
    category: str
    model: str
    rental_rate: float
    release_year: int
    status: str

    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    statusCode: int
    data: Optional[Any] = None
    message: str
    timestamp: str
    path: str
    error: Optional[Any] = None