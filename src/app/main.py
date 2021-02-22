from fastapi import FastAPI
from fastapi.responses import JSONResponse
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from . import crud, models, schemas
from .database import SessionLocal, engine
import os
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)
HERTS_COVID_URL = os.getenv('HERTS_COVID_URL')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/results/daily", response_model=schemas.Cases)
async def read_covid_test_results(db: Session = Depends(get_db)):
    results = crud.get_covid_test_results(db)
    return results


@app.get("/results/", response_model=List[schemas.Cases])
async def read_covid_test_results(db: Session = Depends(get_db)):
    results = crud.get_covid_test_results(db)
    return results
