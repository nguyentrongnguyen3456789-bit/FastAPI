# # BÀI LÀM

# ## Phần 1. Phân tích lỗi

# ### a. Endpoint hiện tại trong source code là gì?

# Endpoint hiện tại là:

# ```text
# GET /student
# ```

# Đây là endpoint được khai báo trong FastAPI để xử lý yêu cầu lấy thông tin sinh viên.

# ---

# ### b. Vì sao khi gọi `GET /students` lại bị lỗi **404 Not Found**?

# Trong source code chỉ khai báo endpoint:

# ```text
# GET /student
# ```

# Trong khi đó, phía Frontend và Tester lại gọi:

# ```text
# GET /students
# ```

# Do FastAPI không tìm thấy endpoint `/students` nên hệ thống trả về lỗi **404 Not Found**.

# Nguyên nhân là đường dẫn API trong source code không khớp với đường dẫn mà khách hàng yêu cầu.

# ---

# ### c. Vì sao tên endpoint `/student` chưa phù hợp với yêu cầu lấy danh sách sinh viên?

# Endpoint `/student` sử dụng danh từ số ít nên thường được hiểu là lấy thông tin của **một sinh viên**.

# Tuy nhiên, yêu cầu của bài toán là lấy **toàn bộ danh sách sinh viên**, vì vậy endpoint nên sử dụng danh từ số nhiều.

# Theo chuẩn RESTful, endpoint đúng là:

# ```text
# GET /students
# ```

# Tên endpoint này thể hiện rõ API dùng để lấy danh sách sinh viên.

# ---

# ### d. Vì sao dòng `return students[0]` chưa đúng với yêu cầu nghiệp vụ?

# Đoạn code:

# ```python
# return students[0]
# ```

# chỉ trả về phần tử đầu tiên trong danh sách sinh viên.

# Trong khi đó, yêu cầu của khách hàng là API phải trả về **toàn bộ danh sách sinh viên** để Frontend hiển thị đầy đủ dữ liệu.

# Vì vậy, việc chỉ trả về một sinh viên là không đúng với yêu cầu nghiệp vụ.

# ---

# ### e. API đúng theo yêu cầu khách hàng nên có đường dẫn là gì?

# API đúng theo yêu cầu là:

# ```text
# GET /students
# ```

# Endpoint này tuân thủ chuẩn RESTful, đúng với yêu cầu lấy danh sách toàn bộ sinh viên.

# ---

# ## Phần 2. Sửa lỗi

# ### Source code sau khi sửa

# ```python
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
# ```
# ### Giải thích
# * Đổi endpoint từ **`/student`** thành **`/students`** để đúng với yêu cầu của khách hàng và chuẩn RESTful.
# * Đổi tên hàm thành **`get_students()`** để thể hiện rõ chức năng lấy danh sách sinh viên.
# * Thay `return students[0]` bằng `return students` để API trả về toàn bộ danh sách sinh viên.
# * Sau khi sửa, API có thể chạy trên FastAPI và khi gọi `GET /students` sẽ trả về dữ liệu JSON chứa đầy đủ danh sách sinh viên.
