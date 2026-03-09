import requests
import json
import os
from dotenv import load_dotenv

# load private variables from local dot env file
load_dotenv()
# access vars
EIA_KEY = os.getenv("eia_api_key")
CENSUS_KEY = os.getenv("census_api_key")

URLS = {
    "eia_2010_2021": (
        f"https://api.eia.gov/v2/electricity/retail-sales/data/?frequency=annual&data[0]=customers&data[1]=sales&start=2010&end=2025&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={EIA_KEY}"
    ),
    "census_2010_2019": (
        "https://www2.census.gov/programs-surveys/popest/datasets/"
        "2010-2019/national/totals/nst-est2019-alldata.csv"
    ),
    "census_2020_2025": (
        "https://www2.census.gov/programs-surveys/popest/datasets/"
        "2020-2025/state/totals/NST-EST2025-ALLDATA.csv"
    ),
}

def fetchRaw(filename, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successful request: {filename}")
            if filename.startswith("census"):
                with open(f"data/raw/{filename}.csv", "w", encoding="latin-1") as file:
                    file.write(response.text)
            else:
                data = response.json()
                with open(f"data/raw/{filename}.txt", "w") as file:
                    json.dump(data, file)
        else:
            # unsuccessful request
            print(f"Request error: status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # for network related errors
        print(f"Network error: {e}")

for URL in URLS:
    fetchRaw(URL, URLS[URL])
