from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Cases(Base):
    __tablename__ = "cases"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=datetime.now)
    scraped_at = Column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    new_staff_cases = Column(Integer)
    on_campus_new_student_cases = Column(Integer, nullable=False)
    off_campus_new_student_cases = Column(Integer, nullable=False)


# class ScraperLog(Base):
#     __tablename__ = "scraper_log"
#     id = Column(Integer, primary_key=True, index=True)
#     created_at = Column(DateTime, default=datetime.now())
#     status = Column(Boolean)
#     status_code = Column(Integer)
