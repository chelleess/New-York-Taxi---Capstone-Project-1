import pandas as pd
import os

os.makedirs("./data/mart", exist_ok=True)

df = pd.read_parquet("./data/transformed/data.parquet")

output = "./data/mart/taxi_mart.csv"

df.to_csv(output, index=False)

print(f"Load completed:  {output}")