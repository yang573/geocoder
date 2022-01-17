import csv, time, sys
import requests
from typing import Tuple, List

# API TOS wants you to identify the app via the user-agent header
app_id = "Simple Geocoder" # change with the name of your app/organization

# Address class for handling structured data
class Address:
    def __init__(self, number: str, street: str, city: str = "", county: str = "",
            state: str = "", country: str = "US", postalcode: str = ""):
        self.street_number = number
        self.street_name = street
        self.city = city
        self.county = county
        self.state = state
        self.country = country
        self.postalcode = postalcode

    def to_query(self):
        # turn class properties into a dictionary
        # skips all empty strings
        query = {k: v for k, v in self.__dict__ if bool(v)}

        # fix street param
        query["street"] = "{} {}".format(self.street_number, self.street_name)
        del query["street_number"]
        del query["street_name"]

        return query

## Sending API requests
def send_geocode_request(params: List[str]) -> requests.Response:
    # request headers
    headers = {"user-agent": app_id}

    # send request and return relevant info
    resp = requests.get("https://nominatim.openstreetmap.org/search", headers=headers, params=params)
    json = resp.json()[0]
    return (json['lat'], json['lon'])

def geocode_address(addr: Address) -> Tuple[str, str]:
    # request params
    params = addr.to_query()
    params["format"] = "json"
    params["limit"] = 1

    x, y = send_geocode_request(params)
    return (x, y)

def geocode_query(addr: str) -> Tuple[str, str]:
    # request params
    params = {
        "q": addr,
        "format": "json",
        "limit": 1
    }

    x, y = send_geocode_request(params)
    return (x, y)


## Reading CSV
def read_csv(filename: str) -> List[Address]:
    return

def read_unstructured_csv(filename: str) -> List[str]:
    lines = None
    with open(filename, "r") as f:
        reader = csv.reader(f)
        lines = [", ".join(map(lambda s: s.strip(), row)) for row in list(reader)]
    return lines

## Main parsing functions
# API TOS wants us to limit request to 1/second
def geocode_unstructured_csv(filename: str):
    addrs = read_unstructured_csv(filename)
    for addr in addrs:
        x, y = geocode_query(addr)
        print("x:", x, "y:", y, "addr:", addr)
        time.sleep(1)
    return

def geocode_csv(filename: str):
    return

## main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: app.py [file]")
        sys.exit(1)

    geocode_unstructured_csv(sys.argv[1])
    sys.exit(0)

