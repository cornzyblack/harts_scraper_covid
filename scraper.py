from helper import extract_table
import pandas as pd

url = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"
result = extract_table(url)

if isinstance(result, pd.DataFrame):
    print(result.to_json(orient="records"))
