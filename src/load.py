import pandas as pd 
import os 

os.makedirs("./data/mart", exist_ok=True)

df = pd.read_parquet("./data/transformed/data.parquet")

df.to_parquet("./data/transformed/data.parquet", index=False)
print("Load completed")