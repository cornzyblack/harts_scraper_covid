from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date


class CovidTestResultBase(BaseModel):
    created_at: datetime
    scraped_at: date
    new_staff_cases: int
    on_campus_new_student_cases: int
    off_campus_new_student_cases: int


class CovidTestResultCreate(CovidTestResultBase):
    pass


class CovidTestResult(CovidTestResultBase):
    class Config:
        orm_mode = True


class ScraperLogBase(BaseModel):
    created_at: datetime
    status: bool
    status_code: int


class ScraperLogCreate(ScraperLogBase):
    pass


class ScraperLogCreate(ScraperLogBase):
    class Config:
        orm_mode = True
