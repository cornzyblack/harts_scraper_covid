from fastapi import FastAPI
import helper
from fastapi.responses import JSONResponse
import pandas as pd
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
HERTS_COVID_URL = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"
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
    url = HERTS_COVID_URL
    result = helper.scrape_table(url, daily=False)
    if isinstance(result, pd.DataFrame):
        result = result.to_dict(orient="records")
    return result


@app.get("/scrape/daily")
def scraper_daily():
    url = HERTS_COVID_URL
    result = helper.scrape_table(url)
    return result


@app.post("/results", response_model=schemas.CovidTestResult)
def create_test_result(trigger: Dict, db: Session = Depends(get_db)):
    result = None
    frequency = trigger["frequency"]
    if frequency == "daily":
        url = HERTS_COVID_URL
        result = helper.scrape_table(url)
        if result:
            db_covid_result = crud.get_covid_test_result_by_date(
                db, date=result.get("created_at", None)
            )
            if db_covid_result:
                raise HTTPException(
                    status_code=400, detail="Test result already created"
                )
    return crud.create_covid_test_result(
        db=db, covid_test_result=schemas.CovidTestResult(**result)
    )


@app.get("/results/daily", response_model=schemas.CovidTestResult)
def read_covid_test_results(db: Session = Depends(get_db)):
    results = crud.get_covid_test_results(db)
    return results


@app.get("/results/", response_model=List[schemas.CovidTestResult])
def read_covid_test_results(db: Session = Depends(get_db)):
    results = crud.get_covid_test_results(db)
    return results
