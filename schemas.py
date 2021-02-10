from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, date


class CasesBase(BaseModel):
    created_at: datetime
    scraped_at: datetime
    new_staff_cases: int
    on_campus_new_student_cases: int
    off_campus_new_student_cases: int


class CasesCreate(CasesBase):
    pass


class Cases(CasesBase):
    class Config:
        orm_mode = True
