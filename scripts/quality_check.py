import pandas as pd 
import os 

#load transform result 
df = pd.read_parquet("./data/transformed/data.parquet")

#make error coloumns 
df["error_type"] = None 

# 1 -- invalid duration case 
df.loc[df["trip_duration_minutes"] <= 0,
       "error_type"
       ] = "duration invalid"

# 2 -- invalid distance case 
df.loc[df["trip_distance"] <= 0,
       "error_type"
       ] = "distance invalid"

#split valid and invalid -- bedain 
valid = df[df["error_type"].isna()]
invalid = df[df["error_type"].notna()]

#create the folder 
os.makedirs("./data/mart_cleaned", exist_ok=True)

#save result
valid.to_csv("./data/mart_cleaned/valid.csv", index=False)
invalid.to_csv("./data/mart_cleaned/quarantine.csv", index=False)

#simple report / feedback
with open("./data/mart_cleaned/report.txt", "w") as f:
    f.write("DATA QUALITY REPORT\n\n")

    f.write(f"Total rows: {len(df)}\n")
    f.write(f"Valid rows: {len(valid)}\n")
    f.write(f"Invalid rows: {len(invalid)}\n\n")

    f.write("Error Summary:\n")
    f.write(
        str(
            df["error_type"]
            .value_counts(dropna=False)
        )
    )