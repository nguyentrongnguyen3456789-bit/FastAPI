# # database.py
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/ontap"

# engine = create_engine(DATABASE_URL)

# LocalSseion = sessionmaker(
#     autocommit = False,
#     autoflush= False,
#     bind= engine
# )

# Base = declarative_base()

# def get_db():
#     try:
#         db = LocalSseion(bind = engine)
#         yield db
#     finally:
#         db.close()

# models.py

from Database import Base
from sqlalchemy import Column,String,Integer

class UserModel():
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(100),nullable=False)
    email = Column(String(100),nullable=False,unique=True)