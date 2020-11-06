import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import dateparser
import  pytz


def get_harts_html(url: str) -> Optional[str] :
    response = requests.get(url)
    result = None
    if response.status_code == 200:
    result = response.content
    return result


def extract_table(url: str) -> Optional[pd.DataFrame]:
    html_result = get_harts_html(url)
    df = None
    if html_result:
        soup = BeautifulSoup(result)
        latest_link = soup.find("h2")
        covid_details_list = list(latest_link.next_siblings)
        start_date = covid_details_list[0]
        covid_table = covid_details_list[1]

        df = pd.read_html(str(covid_table))[0]
        df = df.rename(columns={"Unnamed: 0": "days"})
    return df

def upload_db():
    pass
