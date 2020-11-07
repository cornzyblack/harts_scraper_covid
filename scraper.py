from helper import extract_table

url = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"
result = extract_table(url)
print(result)
