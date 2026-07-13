from sqlalchemy import Column, String, Float, Integer
from Database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String(20), primary_key=True, unique=True, nullable=False)
    category = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    rental_rate = Column(Float, nullable=False)
    release_year = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="available")