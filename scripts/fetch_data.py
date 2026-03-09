import requests
import zipfile
import json
import os
import io
from dotenv import load_dotenv

# load private variables from local dot env file
load_dotenv()
# access vars
EIA_KEY = os.getenv("eia_api_key")

# ensure we were able to get kets from env file
if EIA_KEY is None:
    raise RuntimeError("Missing eia_api_key. Set it in your environment or .env file.")

CENSUS_URLS = {
    "census_2010_2019": (
        "https://www2.census.gov/programs-surveys/popest/datasets/"
        "2010-2019/national/totals/nst-est2019-alldata.csv"
    ),
    "census_2020_2025": (
        "https://www2.census.gov/programs-surveys/popest/datasets/"
        "2020-2025/state/totals/NST-EST2025-ALLDATA.csv"
    )
}

# paginate since the eia API can only return 5000 rows at a time
def fetchEIA():
    filename = "eia_raw_2010_2025"
    base_url = f"https://api.eia.gov/v2/electricity/retail-sales/data/?frequency=annual&data[0]=sales&start=2010&end=2025&sort[0][column]=period&sort[0][direction]=desc&api_key={EIA_KEY}"
    try:
        all_data = []
        offset = 0
        limit = 5000

        while True:
            # paginate by updating offset in url for each request
            url = base_url + f"&offset={offset}&length={limit}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Request error: status code {response.status_code}")
                print(response.text)
                break

            data = response.json()
            rows = data.get("response", {}).get("data", [])

            if not rows:
                break

            all_data.extend(rows)
            print(f"Fetched {len(all_data)} rows so far...")

            # hit the end of the data
            if len(rows) < limit:
                break

            offset += limit

        print(f"Successful request: {filename} — {len(all_data)} total rows")
        with open(f"data/raw/{filename}.json", "w", encoding="latin-1") as file:
            json.dump(all_data, file)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")

def fetchCensus(filename, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Successful request: {filename}")
            with open(f"data/raw/{filename}.csv", "w", encoding="latin-1") as file:
                file.write(response.text)
        else:
            # unsuccessful request
            print(f"Request error: status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # for network related errors
        print(f"Network error: {e}")

def fetch_bea():
    url = "https://apps.bea.gov/regional/zip/SAGDP.zip"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Successful request: bea_raw")
            z = zipfile.ZipFile(io.BytesIO(response.content))
            target = [f for f in z.namelist() if "SAGDP2" in f and "ALL_AREAS" in f and f.endswith(".csv")]
            if not target:
                print("SAGDP2N file not found in ZIP contents:")
                print(z.namelist())
                return
            # split found filename into just name without path or extension
            filename = os.path.splitext(os.path.basename(target[0]))[0]
            with z.open(target[0]) as infile:
                content = infile.read().decode("latin-1")
            with open(f"data/raw/{filename}.csv", "w", encoding="latin-1") as outfile:
                outfile.write(content)
            print("Extracted SAGDP2N BEA data")
        else:
            print(f"Request error: status code {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")


fetchEIA()
for filename, url in CENSUS_URLS.items():
    fetchCensus(filename, url)
fetch_bea()