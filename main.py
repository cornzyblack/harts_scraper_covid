from fastapi import FastAPI
from helper import extract_table
from fastapi.responses import JSONResponse
import pandas as pd

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/scrape")
def scraper():
    url = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"
    result = extract_table(url)
    if isinstance(result, pd.DataFrame):
        result = result.to_dict(orient="records")
    return result
