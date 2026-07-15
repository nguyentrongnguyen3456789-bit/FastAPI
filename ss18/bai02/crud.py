from sqlalchemy.orm import Session
from datetime import datetime
from models import Student, Workshop, Registration
from schemas import StudentCreate, WorkshopCreate, RegistrationCreate

def create_student(db: Session, student: StudentCreate):
    new_student = Student(
        student_code=student.student_code,
        full_name=student.full_name,
        email=student.email,
        status=student.status
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


def get_all_students(db: Session):
    return db.query(Student).all()

def create_workshop(db: Session, workshop: WorkshopCreate):
    new_workshop = Workshop(
        title=workshop.title,
        description=workshop.description,
        maximum_participants=workshop.maximum_participants,
        status=workshop.status,
        start_time=workshop.start_time
    )

    db.add(new_workshop)
    db.commit()
    db.refresh(new_workshop)

    return new_workshop


def get_all_workshops(db: Session):
    return db.query(Workshop).all()


def get_workshop_by_id(db: Session, workshop_id: int):
    return db.query(Workshop).filter(
        Workshop.id == workshop_id
    ).first()

def register_workshop(db: Session, registration: RegistrationCreate):

    student = db.query(Student).filter(
        Student.id == registration.student_id
    ).first()

    if not student:
        return "student_not_found"

    workshop = db.query(Workshop).filter(
        Workshop.id == registration.workshop_id
    ).first()

    if not workshop:
        return "workshop_not_found"

    if workshop.status.lower() == "closed":
        return "workshop_closed"

    check_registration = db.query(Registration).filter(
        Registration.student_id == registration.student_id,
        Registration.workshop_id == registration.workshop_id
    ).first()

    if check_registration:
        return "already_registered"

    total = db.query(Registration).filter(
        Registration.workshop_id == registration.workshop_id
    ).count()

    if total >= workshop.maximum_participants:
        return "workshop_full"

    new_registration = Registration(
        student_id=registration.student_id,
        workshop_id=registration.workshop_id,
        registered_at=datetime.now(),
        status="Registered"
    )

    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    return new_registration

def get_student_workshops(db: Session, student_id: int):

    return db.query(Registration).filter(
        Registration.student_id == student_id
    ).all()

def get_workshop_students(db: Session, workshop_id: int):

    return db.query(Registration).filter(
        Registration.workshop_id == workshop_id
    ).all()

def cancel_registration(db: Session, registration_id: int):

    registration = db.query(Registration).filter(
        Registration.id == registration_id
    ).first()

    if not registration:
        return None

    db.delete(registration)
    db.commit()

    return registration
