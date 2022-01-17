import csv, getopt, time, sys
import requests
from typing import Tuple, List

# API TOS wants you to identify the app via the user-agent header
app_id = "Simple Geocoder" # change with the name of your app/organization

## Sending API requests
def send_geocode_request(params: List[str]) -> Tuple[str, str]:
    # request headers
    headers = {"user-agent": app_id}

    # send request and return relevant info
    resp = requests.get("https://nominatim.openstreetmap.org/search", headers=headers, params=params)
    json = resp.json()
    if json:
        return (json[0]['lat'], json[0]['lon'])
    else:
        return ('0', '0')

def geocode_query(addr: str) -> Tuple[str, str]:
    # request params
    params = {
        "q": addr,
        "format": "json",
        "limit": 1
    }

    print(params)

    x, y = send_geocode_request(params)
    return (x, y)

## Reading CSV
def read_unstructured_csv(filename: str) -> List[str]:
    lines = None
    try:
        with open(filename, "r") as f:
            reader = csv.reader(f)
            lines = [list(map(lambda s: s.strip(), row)) for row in list(reader)]
    except (IOError, OSError) as err:
        print(err)
    return lines

## Main parsing functions
# API TOS wants us to limit request to 1/second
def geocode_unstructured_csv(infile: str, outfile: str, ignore: List[int], has_header: bool):
    # Read the file
    addrs = read_unstructured_csv(infile)
    if addrs == None:
        return False

    # Create header for output file
    header = None
    if has_header:
        header = addrs[0]
    else:
        header = ['-' for i in addrs[0]]
    header.append('latitude')
    header.append('longitude')

    # Geocode and write to output
    try:
        with open(outfile, "w") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for addr in addrs:
                addr_str = ", ".join([x for i, x in enumerate(addr) if i+1 not in ignore])
                x, y = geocode_query(addr_str)
                addr_str += " | x: " + x + " y: " + y
                print(addr_str)

                addr.append(x)
                addr.append(y)
                writer.writerow(addr)
                time.sleep(1)
    except (IOError, OSError, csv.Error) as err:
        print(err)
        return False
    return True

def help():
    print("Usage: python3 app.py -i <input> [options]")
    print("  -i, --input [file]: Input csv file.")
    print("  -o, --output [file]: Output csv file. Defaults to <input>-geocoded.csv")
    print("  --ignore [columns]: Comma-separate list of columns to ignore, 1-indexed")
    print("  --no-header: File contains no header, so do not skip the first row.")
    return

## main
if __name__ == "__main__":
    # Parse arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:", ['input=', 'output=', 'ignore=', 'no-header'])
    except getopt.GetoptError as err:
        print(err)
        help()
        sys.exit(1)

    header = True
    ignore = []
    infile = None
    outfile = None
    for o, a in opts:
        if o in ("-i", '--input'):
            infile = a
        elif o in ("-o", '--output'):
            outfile = a
        elif o == "--no-header":
            header = False
        elif o == "--ignore":
            ignore = [int(x) for x in a.split(',')]
        else:
            print("Unrecognized option", o)
            help()
            sys.exit(1)

    if not infile:
        print("Missing input file")
        help()
        sys.exit(1)
    if not outfile:
        outfile = infile.rsplit('.', 1)[0] + "-geocoded" + ".csv"

    # Geocode the data
    success = geocode_unstructured_csv(infile, outfile, ignore, header)
    sys.exit(int(success))

