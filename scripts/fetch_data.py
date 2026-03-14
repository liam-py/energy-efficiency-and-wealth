import requests
import json
import os
from dotenv import load_dotenv

# load private variables from local dot env file
load_dotenv()
# access vars
APP_TOKEN = os.getenv("socrata_application_token")

NYC_COUNTIES = {
    "manhattan": "061",
    "bronx":     "005",
    "brooklyn":  "047",
    "queens":    "081",
    "staten_island": "085",
}

ACS_BASE_URL = "https://api.census.gov/data/2022/acs/acs5"

LL84_BASE_URL = "https://data.cityofnewyork.us/resource/5zyy-y8am.json"

def fetchLL84():
    all_data = []
    limit = 1000
    offset = 0

    headers = {}
    if APP_TOKEN:
        headers["X-App-Token"] = APP_TOKEN

    # fetch all data in pages from LL84 table
    while True:
        # bbl, bin, borough, 
        params = {
            "$select": (
                "property_id,"
                "nyc_borough_block_and_lot,"
                "nyc_building_identification,"
                "borough,"
                "electricity_use_grid_purchase_1,"
                "property_gfa_calculated_1,"
                "primary_property_type_self"
            ),
            "$where": (
                "electricity_use_grid_purchase_1 IS NOT NULL"
                " AND year_ending='2023-12-31T00:00:00.000'"),
            "$limit": limit,
            "$offset": offset,
        }

        try:
            response = requests.get(LL84_BASE_URL, params=params, headers=headers)
            if response.status_code != 200:
                print(f"Request Error: status code {response.status_code}")
                print(response.text)
                break
            
            rows = response.json()

            if not rows:
                break

            all_data.extend(rows)
            print(f"Fetched {len(all_data)} rows so far...")
            
            # if we've hit the end of the data not because of a limit
            if len(rows) < limit:
                break

            offset += limit
        except requests.exceptions.RequestException as e:
            print("Network Error: failed to reach LL84 {e}")
            print()

        # dump all data into local file
        with open(f"data/raw/ll84_raw.json", "w", encoding="latin-1") as file:
            json.dump(all_data, file)

def fetchACS():
    all_tracts = []

    # query for each county's data from ACS
    for borough, county_fips in NYC_COUNTIES.items():
        params = {
            "get": "NAME,B01003_001E,B19013_001E",
            "for": "tract:*",
            "in": f"state:36 county:{county_fips}",
        }
        try:
            response = requests.get(ACS_BASE_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                headers = data[0]
                # zip function iterates over multiple lists simultaneously and pairs elements in different areas into tuples by index.
                # by zipping one row with header we associate each data point (col) of each row with the header for it
                # turning table into a list of dictionaries
                rows = [dict(zip(headers, row)) for row in data[1:]]
                for row in rows:
                    row["borough"] = borough
                all_tracts.extend(rows)
                print(f"Fetched {len(rows)} tracts for {borough}")
            else:
                print(f"Request error for {borough}: status code {response.status_code}")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print(f"Network error ({borough}): {e}")

    print(f"Successful request: acs_raw — {len(all_tracts)} total tracts")
    with open("data/raw/acs_raw.json", "w") as file:
        json.dump(all_tracts, file)

fetchLL84()
fetchACS()