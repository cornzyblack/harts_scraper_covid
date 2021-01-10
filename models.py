from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class CovidTestResult(Base):
    __tablename__ = "covid_test_result"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(Date)
    scraped_at = Column(DateTime, default=datetime.now())
    new_staff_cases = Column(Integer)
    on_campus_new_student_cases = Column(Integer)
    off_campus_new_student_cases = Column(Integer)


class ScraperLog(Base):
    __tablename__ = "scraper_log"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now())
    status = Column(Boolean)
    status_code = Column(Integer)
