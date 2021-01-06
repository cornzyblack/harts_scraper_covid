from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def get_user(db: Session, date: datetime):
    return (
        db.query(models.CovidTestResult)
        .filter(models.CovidTestResult.created_at == date)
        .first()
    )


def get_covid_test_result_date(db: Session, date: datetime):
    return (
        db.query(models.CovidTestResult)
        .filter(models.CovidTestResult.date == date)
        .first()
    )


def get_covid_test_results(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CovidTestResult).offset(skip).limit(limit).all()


def create_covid_test_result(
    db: Session, covid_test_result: schemas.CovidTestResultCreate
):
    db_test_result = models.CovidTestResult(
        created_at=datetime.now(),
        new_staff_cases=3,
        on_campus_new_student_cases=1,
        off_campus_new_student_cases=10,
    )
    db.add(db_test_result)
    db.commit()
    db.refresh(db_test_result)
    return db_test_result


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
