from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/testapi"

engine = create_engine(DATABASE_URL)
LocalsSession  = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = LocalsSession()
    try:
        yield db
    finally:
        db.close()
