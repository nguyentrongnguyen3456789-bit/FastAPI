from sqlalchemy.orm import Session
from datetime import datetime
from models import Student, Course, Enrollment
from schemas import EnrollmentCreate


# ==========================
# Student
# ==========================

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(
        Student.id == student_id
    ).first()


# ==========================
# Course
# ==========================

def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(
        Course.id == course_id
    ).first()


# ==========================
# Enrollment
# ==========================

def create_enrollment(db: Session, enrollment: EnrollmentCreate):

    # Kiểm tra sinh viên
    student = db.query(Student).filter(
        Student.id == enrollment.student_id
    ).first()

    if not student:
        return "student_not_found"

    # Kiểm tra khóa học
    course = db.query(Course).filter(
        Course.id == enrollment.course_id
    ).first()

    if not course:
        return "course_not_found"

    # Sinh viên phải ACTIVE
    if student.status != "ACTIVE":
        return "student_inactive"

    # Khóa học phải OPEN
    if course.status != "OPEN":
        return "course_closed"

    # Không đăng ký trùng
    check = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()

    if check:
        return "already_enrolled"

    # Kiểm tra số lượng
    total = db.query(Enrollment).filter(
        Enrollment.course_id == enrollment.course_id
    ).count()

    if total >= course.max_students:
        return "course_full"

    # Tạo đăng ký
    new_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        enrolled_at=datetime.now()
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment


# ==========================
# Student Courses
# ==========================

def get_student_courses(db: Session, student_id: int):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        return None

    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()

    courses = []

    for item in enrollments:
        course = db.query(Course).filter(
            Course.id == item.course_id
        ).first()

        if course:
            courses.append({
                "id": course.id,
                "name": course.name
            })

    return {
        "student_id": student.id,
        "full_name": student.full_name,
        "courses": courses
    }
