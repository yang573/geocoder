import csv, sys
import requests
from typing import Tuple, List

class Address:
    def __init__(self,
            number: str,
            street: str,
            city: str = "",
            county: str = "",
            state: str = "",
            country: str = "US",
            postalcode: str = ""):
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

def geocode_address(addr: Address) -> Tuple[str, str]:
    params = addr.to_query()
    params["format"] = "json"
    params["limit"] = 1

    resp = requests.get("https://nominatim.openstreetmap.org/search", params=params)
    json = resp.json()
    print(resp)
    return (json[0]['lat'], json[0]['lon'])

def geocode_query(addr: str) -> Tuple[str, str]:
    params = {
        "q": addr,
        "format": "json",
        "limit": 1
    }

    resp = requests.get("https://nominatim.openstreetmap.org/search", params=params)
    json = resp.json()
    print(json)
    return (json[0]['lat'], json[0]['lon'])

def read_csv(filename: str) -> List[Address]:
    return

def read_unstructured_csv(filename: str) -> List[str]:
    lines = None
    with open(filename, "r") as f:
        reader = csv.reader(f)
        lines = [", ".join(map(lambda s: s.strip(), row)) for row in list(reader)]
    return lines

def geocode_unstructured_csv(filename: str):
    addrs = read_unstructured_csv(filename)
    print(addrs)
    for addr in addrs:
        x, y = geocode_query(addr)
        print(x, y)
    return

def geocode_csv(filename: str):
    return

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: app.py [file]")
        sys.exit(1)

    geocode_unstructured_csv(sys.argv[1])

