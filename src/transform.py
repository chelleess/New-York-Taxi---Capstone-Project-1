import pandas as pd

# load data 
df = pd.read_parquet(
    "./data/raw/yellow_tripdata_2026-01.parquet"
)

# rename kolom  transform ke snake_case 
df.columns = (
    df.columns
    .str.strip() #hapus spasi depan & belakang
    .str.lower() #huruf kecil 
    .str.replace(" ", "_")
)

#rename manual buat kolom camelCase 
df = df.rename(columns={
    "vendorid": "vendor_id",
    "ratecodeid": "ratecode_id"
})


#convert date time
df["tpep_pickup_datetime"] = pd.to_datetime(
    df["tpep_pickup_datetime"]
)

df["tpep_dropoff_datetime"] = pd.to_datetime(
    df["tpep_dropoff_datetime"]
)

#convert ke float 
numeric_cols = [
    "fare_amount",
    "tip_amount",
    "total_amount"
]

df[numeric_cols] = df[numeric_cols].astype(float)

# Check
print(df.head())
print(df.dtypes)


###### DATETIME TRANSFORMATION ######
# trip duration
df["trip_duration_minutes"] = (
    (
        df["tpep_dropoff_datetime"]
        -
        df["tpep_pickup_datetime"]
    )
    .dt.total_seconds()
    / 60
)

# pickup date
df["pickup_date"] = (
    df["tpep_pickup_datetime"]
    .dt.date
)

# pickup hour
df["pickup_hour"] = (
    df["tpep_pickup_datetime"]
    .dt.hour
)

# pickup day name
df["pickup_day_name"] = (
    df["tpep_pickup_datetime"]
    .dt.day_name()
)

# weekend
df["is_weekend"] = (
    df["pickup_day_name"]
    .isin(
        [
            "Saturday",
            "Sunday"
        ]
    )
)

print(
    df[
        [
            "trip_duration_minutes",
            "pickup_date",
            "pickup_hour",
            "pickup_day_name",
            "is_weekend"
        ]
    ].head()
)

#categorize time 
def get_time_period(hour):

    if hour <= 5:
        return "Late Night"

    elif hour <= 10:
        return "Morning"

    elif hour <= 15:
        return "Afternoon"

    elif hour <= 19:
        return "Evening Rush"

    else:
        return "Night"


df["time_period"] = (
    df["pickup_hour"]
    .apply(get_time_period)
)

#cek
print(
    df[
        [
            "pickup_hour",
            "time_period"
        ]
    ].head()
)

########## CATEGORICAL MAPPING ################
#payment mapping 
payment_map = {
    1: "Credit Card",
    2: "Cash",
    3: "No Charge",
    4: "Dispute",
    0: "Unknown"
}

df["payment_type_name"] = (
    df["payment_type"]
    .map(payment_map)
)

#store the flag mapping 
store_map = {
    "Y": "Store and Forward",
    "N": "Normal"
}

df["store_and_fwd_name"] = (
    df["store_and_fwd_flag"]
    .map(store_map)
)

print(
    df[
        [
            "payment_type", 
            "payment_type_name", 
            "store_and_fwd_flag", 
            "store_and_fwd_name"
        ]
    ].head()
)


############### Mapping Lokasi ##############
#load the lookup table 
zone = pd.read_csv(
    "./data/raw/taxi_zone_lookup.csv" 
)

#pickup loaction
df = df.merge(
    zone, 
    left_on="pulocationid",
    right_on="LocationID",
    how="left"
)

df = df.rename(columns={
    "Zone": "pickup_zone", 
    "Borough": "pickup_borough"
})

print(
    df[
        [
        "pulocationid",
        "pickup_zone",
        "pickup_borough"
        ]
    ].head()
)

#dropoff location 
df = df.merge(
    zone, 
    left_on="dolocationid",
    right_on="LocationID",
    how = "left"
)

df = df.rename(columns={
    "Zone": "dropoff_zone",
    "Borough": "dropoff_borough"
})

print(
    df[[
        "dolocationid",
        "dropoff_zone",
        "dropoff_borough"
    ]
    ].head()
)

import os

os.makedirs("./data/transformed", exist_ok=True)

df.to_parquet("./data/transformed/data.parquet", index=False)