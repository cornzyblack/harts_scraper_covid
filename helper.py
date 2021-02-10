import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
from datetime import date
from typing import Optional, List, Union, Tuple
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
    except Exception as e:
        print(e)
    return result


def is_weekday(day: date) -> bool:
    """
    Returns the boolean flag if the date is a weekday

    Parameters:
        day (date): The current date

    Returns:
        bool: boolean flag if the day is a weekday
    """
    is_weekday = False
    if day.weekday() in [0, 1, 2, 3, 4]:
        is_weekday = True
    return is_weekday


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
    except Exception as e:
        print(e)
    return result


def scrape_table(url: str, daily: bool = True) -> Union[pd.DataFrame, List]:
    """
    Returns the HTML content of the URL.
    Parameters:
        url (str): The Harts Covid URL page
        daily (bool): Tag to specify if results for the current page should be scraped
    Returns:
        pd.DataFrame: A DataFrame of the scraped Table in the Covid Page
    """
    html_result = get_harts_html(url)
    df = None
    start_week = None
    start_week_text = None
    result = None

    british_tz = pytz.timezone("GMT")
    time_now = datetime.now(tz=british_tz)
    current_year = time_now.year
    try:
        if html_result:
            soup = BeautifulSoup(html_result, features="lxml")
            table_tag = soup.find("table")
            table_html = str(table_tag)

            start_week_match = soup.find_all("h3", text=re.compile("Week commencing"))
            if start_week_match:
                start_week_text = start_week_match[0].text.lower()
                month_match = r"(\d{0,2})\s(january|february|march|april|may|june|july|august|september|october|november|december)"
                start_date_match = re.search(month_match, start_week_text)

                if start_date_match:
                    start_week_text = (
                        start_week_text[start_date_match.start() :]
                        + ","
                        + str(current_year)
                    )
                    start_week = dateparser.parse(start_week_text)

            df = pd.read_html(table_html)[0]
            df = df.rename(
                columns={
                    "Unnamed: 0": "weekdays",
                    "New staff cases": "new_staff_cases",
                    "New student cases: On-campus": "on_campus_new_student_cases",
                    "New student cases: Off-campus": "off_campus_new_student_cases",
                }
            )

            df["created_at"] = pd.date_range(
                start_week.strftime("%m/%d/%Y"), periods=df.shape[0]
            )
            result = df
            df["scraped_at"] = datetime.now()
            df = df[
                [
                    "created_at",
                    "scraped_at",
                    "new_staff_cases",
                    "on_campus_new_student_cases",
                    "off_campus_new_student_cases",
                ]
            ]

        if daily:
            result = df[df.created_at ==(time_now.date() - timedelta(days=1)).strftime("%Y-%m-%d")].to_dict(
                orient="records"
            )
            if result:
                result = result[0]
    except Exception as e:
        print(e)
        return None
    return result
