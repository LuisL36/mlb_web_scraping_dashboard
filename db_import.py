import sqlite3
import pandas as pd
from pathlib import Path

# File paths
csv_file = Path("mlb_stat_leaders.csv")
db_file = Path("mlb_data.db")

if not csv_file.exists():
    raise FileNotFoundError(f"❌ {csv_file} not found. Run web_scraper.py first.")

# Connect to database
conn = sqlite3.connect(db_file)

# Load CSV
df = pd.read_csv(csv_file)
print(f"✅ Loaded {len(df)} rows from {csv_file}")

# Create / replace table
df.to_sql("mlb_stat_leaders", conn, if_exists="replace", index=False)
conn.close()

print(f"📦 Imported data into {db_file} (table: mlb_stat_leaders)")
