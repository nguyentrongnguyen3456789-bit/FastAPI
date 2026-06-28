# ==========================
# PHẦN 1. PHÂN TÍCH INPUT/OUTPUT
# ==========================

# 1. Input của bài toán
# - Input là danh sách books.
# - Mỗi phần tử là một dictionary gồm:
#   + id: Mã sách.
#   + title: Tên sách.
#   + quantity: Số lượng tồn kho.

# 2. Output mong muốn
# Khi gọi:
# GET /books/low-stock
#
# API trả về:
# {
#     "message": "Danh sách sách sắp hết hàng",
#     "data": [...]
# }
#
# Nếu không có sách nào sắp hết hàng:
# {
#     "message": "Không có sách nào sắp hết hàng",
#     "data": []
# }

# 3. Điều kiện xác định sách sắp hết hàng
# - quantity <= 5
# - Nếu thiếu trường quantity thì bỏ qua.
# - Nếu quantity < 0 thì bỏ qua.


# ==========================
# PHẦN 2. ĐỀ XUẤT GIẢI PHÁP
# ==========================

# Giải pháp 1:
# - Dùng vòng lặp for để duyệt từng quyển sách.
# - Kiểm tra các điều kiện rồi thêm vào danh sách kết quả.
# - Ưu điểm: Dễ đọc, dễ xử lý bẫy dữ liệu, dễ bảo trì.
# - Nhược điểm: Code dài hơn.

# Giải pháp 2:
# - Dùng List Comprehension để lọc dữ liệu.
# - Ưu điểm: Ngắn gọn.
# - Nhược điểm: Khó đọc và khó xử lý khi có nhiều điều kiện.


# ==========================
# PHẦN 3. SO SÁNH VÀ LỰA CHỌN
# ==========================

# Tiêu chí                  Vòng lặp for      List Comprehension
# --------------------------------------------------------------
# Độ dễ hiểu               Cao               Trung bình
# Độ ngắn gọn              Trung bình        Cao
# Dễ xử lý bẫy dữ liệu     Rất tốt           Trung bình
# Dễ bảo trì               Cao               Trung bình

# Em chọn giải pháp sử dụng vòng lặp for vì
# dễ đọc, dễ bảo trì và dễ xử lý các trường hợp đặc biệt.


# ==========================
# PHẦN 4. THIẾT KẾ CÁC BƯỚC XỬ LÝ
# ==========================

# Bước 1: Khởi tạo FastAPI.
# Bước 2: Khai báo danh sách books.
# Bước 3: Tạo endpoint GET /books/low-stock.
# Bước 4: Duyệt từng quyển sách.
# Bước 5: Nếu thiếu quantity thì bỏ qua.
# Bước 6: Nếu quantity < 0 thì bỏ qua.
# Bước 7: Nếu quantity <= 5 thì thêm vào danh sách kết quả.
# Bước 8: Nếu danh sách kết quả rỗng thì trả về message phù hợp.
# Bước 9: Nếu có dữ liệu thì trả về danh sách sách sắp hết hàng.


# ==========================
# PHẦN 5. TRIỂN KHAI CODE
# ==========================

from fastapi import FastAPI

app = FastAPI()

books = [
    {"id": 1, "title": "Python Basic", "quantity": 12},
    {"id": 2, "title": "FastAPI Beginner", "quantity": 3},
    {"id": 3, "title": "Clean Code", "quantity": 5},
    {"id": 4, "title": "Database Design", "quantity": 0},
    {"id": 5, "title": "Web API Design", "quantity": 20},
    {"id": 6, "title": "Java Basic"},
    {"id": 7, "title": "Spring Boot", "quantity": -2}
]


@app.get("/books/low-stock")
def get_low_stock_books():
    low_stock_books = []

    for book in books:
        if "quantity" not in book:
            continue

        if book["quantity"] < 0:
            continue

        if book["quantity"] <= 5:
            low_stock_books.append(book)

    if len(low_stock_books) == 0:
        return {
            "message": "Không có sách nào sắp hết hàng",
            "data": []
        }

    return {
        "message": "Danh sách sách sắp hết hàng",
        "data": low_stock_books
    }