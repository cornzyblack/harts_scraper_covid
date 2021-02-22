from sqlalchemy.orm import Session
import models
from datetime import datetime



def get_covid_test_result_by_date(db: Session, date: datetime):
    return (
        db.query(models.Cases)
        .filter(models.Cases.created_at == date)
        .first()
    )


def get_covid_test_results(db: Session):
    return db.query(models.Cases).all()
