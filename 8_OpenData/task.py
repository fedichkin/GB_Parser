import requests
import csv
from fake_headers import Headers

header = Headers(headers=True).generate()
url = "https://data.gov.ru/opendata/7703771271-ekp/data-20150914T1545-structure-20150914T1545.csv?encoding=UTF-8"
response = requests.get(url, headers=header)

with open("file.csv", "wb") as file:
    file.write(response.content)

with open("file.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        print(f"Row: {row}")
