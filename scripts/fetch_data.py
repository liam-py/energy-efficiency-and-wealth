import requests
import json
import os
from dotenv import load_dotenv

# load private variables from local dot env file
load_dotenv()
# access vars
eia_key = os.getenv("eia_api_key")

# URL endpoint for eia data
# catch errors with private key variable
if eia_key is not None:
    eia_url = f"https://api.eia.gov/v2/electricity/retail-sales/data/?frequency=annual&data[0]=customers&data[1]=sales&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000&api_key={eia_key}"
else:
    raise RuntimeError("Missing eia_key. Set it in your environment or .env file.")

def fetchRaw(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Succesful request")
            data = response.json()
            with open("data/raw/eia_raw.txt", "w") as file:
                json.dump(data, file)
        else:
            # unsuccessful request
            print(f"Request error: status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # for network related errors
        print(f"Network error: {e}")

fetchRaw(eia_url)
# fetchRaw(census_url)
# fetchRaw(bea_url)
