from sqlalchemy.orm import Session
from models import Device
from schemas import DeviceRequestDTO
from sqlalchemy.exc import SQLAlchemyError


# Lấy danh sách thiết bị + tìm kiếm + sắp xếp
def get_all_devices(
    db: Session,
    category: str = None,
    status: str = None,
    sort_by: str = None,
    order: str = "asc"
):
    query = db.query(Device)

    # Tìm theo category
    if category:
        query = query.filter(Device.category.ilike(f"%{category}%"))

    # Lọc theo status
    if status:
        query = query.filter(Device.status == status)

    # Sắp xếp
    if sort_by == "rental_rate":
        if order == "desc":
            query = query.order_by(Device.rental_rate.desc())
        else:
            query = query.order_by(Device.rental_rate.asc())

    elif sort_by == "release_year":
        if order == "desc":
            query = query.order_by(Device.release_year.desc())
        else:
            query = query.order_by(Device.release_year.asc())

    else:
        query = query.order_by(Device.id.asc())

    return query.all()


# Lấy chi tiết thiết bị
def get_device(db: Session, device_id: str):
    return db.query(Device).filter(Device.id == device_id).first()


# Thêm thiết bị
def create_device(db: Session, device: DeviceRequestDTO):

    check_device = get_device(db, device.id)

    if check_device:
        return None

    try:
        new_device = Device(
            id=device.id,
            category=device.category,
            model=device.model,
            rental_rate=device.rental_rate,
            release_year=device.release_year,
            status=device.status
        )

        db.add(new_device)
        db.commit()
        db.refresh(new_device)

        return new_device

    except SQLAlchemyError:
        db.rollback()
        raise


# Cập nhật thiết bị
def update_device(
    db: Session,
    device_id: str,
    device: DeviceRequestDTO
):

    db_device = get_device(db, device_id)

    if not db_device:
        return None

    try:

        db_device.category = device.category
        db_device.model = device.model
        db_device.rental_rate = device.rental_rate
        db_device.release_year = device.release_year
        db_device.status = device.status

        db.commit()
        db.refresh(db_device)

        return db_device

    except SQLAlchemyError:
        db.rollback()
        raise


# Xóa thiết bị
def delete_device(db: Session, device_id: str):

    db_device = get_device(db, device_id)

    if not db_device:
        return None

    try:

        db.delete(db_device)
        db.commit()

        return db_device

    except SQLAlchemyError:
        db.rollback()
        raise