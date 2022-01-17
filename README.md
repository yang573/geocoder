## Geocoder

Geocoder using the Nominatim API

### Usage
```
Usage: python3 app.py -i <input> [options]
  -i, --input [file]: Input csv file.
  -o, --output [file]: Output csv file. Defaults to <input>-geocoded.csv
  --ignore [columns]: Comma-separate list of columns to ignore, 1-indexed
  --no-header: File contains no header, so do not skip the first row.
```

Example:

| test.csv | | | | | |
| --- | --- | --- | --- | --- | --- |
| 1 | William | 5601 Williams Rd | Lewisville | North Carolina | 27023 |
| 2 | Bob | 834 S Chambers Rd |	Aurora | Colorado | 80017 |

```
> python3 app.py -i test.csv --no-header --ignore 1,2
```

### Notes

Make sure you modify **app\_id** at the top of the script to identify yourself.

Nominatim TOS: https://operations.osmfoundation.org/policies/nominatim/

> Requirements
> * No heavy uses (an absolute maximum of 1 request per second).
> * Provide a valid HTTP Referer or User-Agent identifying the application (stock User-Agents as set by http libraries will not do).
> * Clearly display attribution as suitable for your medium.
> * Data is provided under the ODbL license which requires to share alike (although small extractions are likely to be covered by fair usage / fair dealing)

