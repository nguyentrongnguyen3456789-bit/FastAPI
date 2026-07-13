from Database import Base
from sqlalchemy import Column,String,Integer

def UserModel(Base):
    __tablename__ = "User"

    id =Column(Integer, primary_key=True,index=True,autoincrement=True)
    name = Column(String(100),)