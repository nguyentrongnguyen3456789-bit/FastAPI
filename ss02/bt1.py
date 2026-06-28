# # BÀI LÀM

# ## 1. Phân tích lỗi

# ### a. Trace luồng xử lý khi gọi `/getStudents`

# ```text
# Client (Frontend/Postman)
#         │
#         │ GET /getStudents
#         ▼
# FastAPI Router
#         │
#         ▼
# Hàm get_students()
#         │
#         ▼
# return str(students)
#         │
#         ▼
# FastAPI Response
#         │
#         ▼
# Trả về dữ liệu dạng String
#         │
#         ▼
# Frontend không đọc được dữ liệu dưới dạng JSON Array
# ```

# ### Legacy Code

# ```python
# from fastapi import FastAPI

# app = FastAPI()

# students = [
#     {"id": 1, "name": "An", "age": 20},
#     {"id": 2, "name": "Bình", "age": 21}
# ]

# @app.get("/getStudents")
# def get_students():
#     return str(students)
# ```

# ### b. Giải thích vì sao FastAPI không nên trả về String trong API JSON

# Trong đoạn code trên, hàm `str(students)` đã chuyển danh sách sinh viên từ kiểu dữ liệu **List** của Python sang **String**. Khi đó FastAPI sẽ trả về một chuỗi ký tự thay vì dữ liệu JSON.

# Trong khi đó, Frontend mong muốn nhận được dữ liệu ở dạng **JSON Array** để có thể hiển thị danh sách sinh viên hoặc thực hiện các thao tác như duyệt mảng, tìm kiếm và lọc dữ liệu. Nếu API trả về String thì Frontend sẽ không xử lý được dữ liệu đúng cách và có thể phát sinh lỗi.

# Vì vậy, trong FastAPI không nên sử dụng `str()` hoặc nối chuỗi để trả về dữ liệu JSON.

# ### c. Chỉ ra lỗi trong thiết kế REST Endpoint (Naming Convention)

# Endpoint hiện tại là:

# ```text
# GET /getStudents
# ```

# Endpoint này chưa đúng chuẩn RESTful vì URL chứa động từ **get**. Theo quy ước RESTful, hành động lấy dữ liệu đã được thể hiện bởi phương thức **GET**, nên URL chỉ cần biểu diễn tên của tài nguyên.

# Endpoint đúng nên là:

# ```text
# GET /students
# ```

# Cách đặt tên này ngắn gọn, dễ hiểu, đúng chuẩn RESTful và thuận tiện cho việc mở rộng hệ thống sau này.

# ---

## 2. Sửa lỗi

### Code sau khi sửa

from fastapi import FastAPI

app = FastAPI()

students = [
    {"id": 1, "name": "An", "age": 20},
    {"id": 2, "name": "Bình", "age": 21},
    {"id": 3, "name": "Cường", "age": 22}
]

@app.get("/students")
def get_students():
    return students


# ### Giải thích

# * Đổi endpoint từ **`/getStudents`** thành **`/students`** để đúng chuẩn RESTful.
# * Không sử dụng `str()` hoặc nối chuỗi để trả dữ liệu.
# * Trả về trực tiếp danh sách `students`.
# * FastAPI sẽ tự động chuyển đổi danh sách Python thành **JSON Array**.
# * Frontend sẽ nhận được dữ liệu JSON đúng chuẩn và có thể hiển thị danh sách sinh viên mà không gặp lỗi.
