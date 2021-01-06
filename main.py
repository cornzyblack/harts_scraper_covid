from fastapi import FastAPI
from . import helper
from fastapi.responses import JSONResponse
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

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


@app.get("/scrape/weekly")
def scraper_weekly():
    url = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"
    result = helper.extract_table(url, daily=False)
    if isinstance(result, pd.DataFrame):
        result = result.to_dict(orient="records")
    return result


@app.get("/scrape/daily")
def scraper_daily():
    url = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"
    result = helper.scrape_table(url)
    if isinstance(result, pd.DataFrame):
        result = result.to_dict(orient="records")
    return result


@app.post("/results/", response_model=schemas.CovidTestResult)
def create_test_result(
    result: schemas.CovidTestResultCreate, db: Session = Depends(get_db)
):
    db_covid_result = crud.get_covid_test_result_date(db, date=result.date)
    if db_covid_result:
        raise HTTPException(status_code=400, detail="Test result already created")
    return crud.create_covid_test_result(db=db, covid_test_result=result)


@app.get("/results/", response_model=List[schemas.CovidTestResult])
def read_covid_test_results(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    results = crud.get_covid_test_results(db, skip=skip, limit=limit)
    return results


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
