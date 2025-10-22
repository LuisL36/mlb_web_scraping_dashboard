import sqlite3
import pandas as pd
import os

conn = sqlite3.connect("mlb_data.db")
cursor = conn.cursor()

for file in os.listdir("data"):
    if file.endswith(".csv"):
        table_name = file.replace(".csv", "")
        df = pd.read_csv(f"data/{file}")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"Imported {file} into table '{table_name}'")

conn.commit()
conn.close()
