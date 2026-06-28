# # BÀI LÀM

# ## Phần 1. Báo cáo phân tích

# ### 1. Input của bài toán

# Input là danh sách sinh viên có sẵn trong hệ thống:

# ```python
# students = [
#     {"id": 1, "name": "An", "status": "active"},
#     {"id": 2, "name": "Binh", "status": "inactive"},
#     {"id": 3, "name": "Cuong", "status": "active"},
#     {"id": 4, "name": "Dung", "status": "pending"}
# ]
# ```

# Mỗi sinh viên gồm các thông tin:

# * `id`: Mã sinh viên.
# * `name`: Tên sinh viên.
# * `status`: Trạng thái học tập.

# ---

# ### 2. Output mong muốn

# Khi gọi API:

# ```text
# GET /students/active
# ```

# Hệ thống trả về danh sách các sinh viên có trạng thái **"active"** theo định dạng JSON gồm hai trường:

# * `message`: Thông báo kết quả.
# * `data`: Danh sách sinh viên đang học.

# Nếu không có sinh viên nào đang học thì trả về:

# ```json
# {
#     "message": "Không có sinh viên đang học",
#     "data": []
# }
# ```

# ---

# ### 3. Điều kiện xác định sinh viên đang học

# Một sinh viên được xem là đang học khi:

# ```python
# student["status"] == "active"
# ```

# Chỉ những sinh viên có `status` bằng `"active"` mới được đưa vào danh sách kết quả.

# ---

# ### 4. Các bước xử lý API `GET /students/active`

# **Bước 1:** Khai báo endpoint `GET /students/active`.

# **Bước 2:** Duyệt toàn bộ danh sách `students`.

# **Bước 3:** Lọc các sinh viên có `status == "active"`.

# **Bước 4:** Kiểm tra kết quả sau khi lọc:

# * Nếu danh sách rỗng thì trả về:

#   * `message`: `"Không có sinh viên đang học"`
#   * `data`: `[]`
# * Nếu có dữ liệu thì trả về:

#   * `message`: `"Danh sách sinh viên đang học"`
#   * `data`: Danh sách sinh viên đang học.

# ---

## Phần 2. Triển khai code

from fastapi import FastAPI

app = FastAPI(
    title="Student Management API",
    version="1.0.0"
)

students = [
    {"id": 1, "name": "An", "status": "active"},
    {"id": 2, "name": "Binh", "status": "inactive"},
    {"id": 3, "name": "Cuong", "status": "active"},
    {"id": 4, "name": "Dung", "status": "pending"}
]

@app.get("/students/active")
def get_active_students():
    active_students = []

    for student in students:
        if student["status"] == "active":
            active_students.append(student)

    if len(active_students) == 0:
        return {
            "message": "Không có sinh viên đang học",
            "data": []
        }

    return {
        "message": "Danh sách sinh viên đang học",
        "data": active_students
    }

