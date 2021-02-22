import os
import sys
from datetime import datetime
from sqlalchemy import insert
from dotenv import load_dotenv
from sqlalchemy import MetaData
from helper import scrape_table
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, Numeric, String, ForeignKey, Boolean, DateTime


load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

url = os.getenv('HERTS_COVID_URL')

metadata = MetaData()

cases = Table('cases', metadata,
    Column('id', Integer(), primary_key=True),
    Column('new_staff_cases', Integer()),
    Column('on_campus_new_student_cases', Integer(), nullable=False),
    Column('off_campus_new_student_cases', Integer(), nullable=False),
    Column('created_at', DateTime(), default=datetime.now),
    Column('scraped_at', DateTime(timezone=True), default=datetime.now, onupdate=datetime.now))


result = scrape_table(url)

metadata.create_all(engine)

ins = cases.insert()

with engine.connect() as connection:
    connection.execute(ins, result)
