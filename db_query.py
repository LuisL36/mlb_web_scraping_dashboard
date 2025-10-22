import sqlite3
import pandas as pd

conn = sqlite3.connect("mlb_data.db")

print("Connected to mlb_data.db")
print("Try queries like: SELECT * FROM mlb_yearly_events LIMIT 5;")

while True:
    query = input("\nSQL> ")
    if query.lower() in ["exit", "quit"]:
        break
    try:
        result = pd.read_sql_query(query, conn)
        print(result.head())
    except Exception as e:
        print("Error:", e)

conn.close()
