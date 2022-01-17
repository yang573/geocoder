import csv, sys
import requests
from typing import Tuple, List

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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: app.py [file]")
        sys.exit(1)

    geocode_unstructured_csv(sys.argv[1])

