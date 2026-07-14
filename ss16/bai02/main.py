from database import Base, engine
import employee_models

Base.metadata.create_all(bind=engine)

print("Tạo bảng thành công!")