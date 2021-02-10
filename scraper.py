from helper import scrape_table
import pandas as pd

url = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"
result = scrape_table(url)
print(result)
if isinstance(result, pd.DataFrame):
    print(result.to_json(orient="records"))
