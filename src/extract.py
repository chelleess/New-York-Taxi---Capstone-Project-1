import requests
import os

DATA_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2026-01.parquet"
LOOKUP_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"

SAVE_FOLDER = "./data/raw"

os.makedirs(SAVE_FOLDER, exist_ok=True)


def download(url, filename):
    response = requests.get(url)

    # check download success
    if response.status_code == 200:

        filepath = os.path.join(
            SAVE_FOLDER,
            filename
        )

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"{filename} downloaded")

    else:
        print(
            f"Download failed: {response.status_code}"
        )


download(
    DATA_URL,
    "yellow_tripdata_2026-01.parquet"
)

download(
    LOOKUP_URL,
    "taxi_zone_lookup.csv"
)