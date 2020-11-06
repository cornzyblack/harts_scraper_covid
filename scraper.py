from helper import get_harts_html

url = "https://www.herts.ac.uk/coronavirus/covid-19-case-tracker"

result = get_harts_html(url)

soup = BeautifulSoup(result)

# soup.find("<h2>Latest University of Hertfordshire COVID-19 positive test results</h2>")
latest_link = soup.find("h2")

covid_details_list = list(latest_link.next_siblings)

start_date = covid_details_list[0]
covid_table = covid_details_list[1]

df = pd.read_html(str(covid_table))[0]
df = df.rename(columns={"Unnamed: 0": "days"})

# datetime.now(tz="London")
import  pytz
british_tz = pytz.timezone("GMT")
time_now = datetime.now(tz=british_tz)
current_year = time_now.year

start_datetime = dateparser.parse(start_date.text.split('Week commencing')[-1] + str(current_year))

df["dates"] = pd.date_range(start_datetime.strftime("%m/%d/%Y"), periods=df.shape[0])
