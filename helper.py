import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from typing import Optional
import dateparser
import pytz


def get_harts_html(url: str) -> Optional[str]:
    """
    Returns the HTML content of the URL.

    Parameters:
        url (str):The Harts Covid URL page

    Returns:
        str: The page in HTML format
    """

    result = None
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.content
    except:
        pass
    return result


def extract_table(url: str) -> Optional[pd.DataFrame]:
    """
    Returns the HTML content of the URL.

    Parameters:
        url (str):The Harts Covid URL page

    Returns:
        pd.DataFrame: A DataFrame of the scraped Table in the Covid Page
    """
    html_result = get_harts_html(url)
    df = None
    if html_result:
        soup = BeautifulSoup(html_result, features="lxml")
        latest_link = soup.find("h2")
        covid_details_list = list(latest_link.next_siblings)
        start_date = covid_details_list[0]
        covid_table = covid_details_list[1]

        df = pd.read_html(str(covid_table))[0]
        df = df.rename(columns={"Unnamed: 0": "days"})
        british_tz = pytz.timezone("GMT")

        time_now = datetime.now(tz=british_tz)
        current_year = time_now.year

        start_datetime = dateparser.parse(
            start_date.text.split("Week commencing")[-1] + str(current_year)
        )

        df["dates"] = pd.date_range(
            start_datetime.strftime("%m/%d/%Y"), periods=df.shape[0]
        )

    return df


def upload_db():
    pass
