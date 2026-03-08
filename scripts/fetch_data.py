import requests

# URL endpoint for eia data
eia_url = "https://api.eia.gov/v2/electricity/retail-sales/data/?frequency=annual&data[0]=customers&data[1]=sales&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

def fetchRaw(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Succesful request")
            data = response.json
            with open("eia_raw.txt", "w") as file:
                file.write(data)
        else:
            # unsuccessful request
            print(f"Request error: status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        # for network related errors
        print(f"Network error: {e}")

fetchRaw(eia_url)
# fetchRaw(census_url)
# fetchRaw(bea_url)
