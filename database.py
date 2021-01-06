from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

POSTGRES_URL = os.getenv("POSTGRES_URL")
print(POSTGRES_URL)

SQLALCHEMY_DATABASE_URL = POSTGRES_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class CovidTestResult(Base):
    __tablename__ = "covid_test_result"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(datetime)
    new_staff_cases = Column(Integer)
    new_student_cases = Column(Integer)
    on_campus_new_student_cases = Column(Integer)
    off_campus_new_student_cases = Column(Integer)

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class ScraperLog(Base):
    __tablename__ = "scraper_log"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(datetime)
    status = Column(Boolean)
    status_code = Column(Integer)
