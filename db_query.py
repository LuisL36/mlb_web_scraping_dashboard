import sqlite3
import pandas as pd

DB_FILE = "mlb_data.db"

# Connect to the database
try:
    conn = sqlite3.connect(DB_FILE)
    print(f"✅ Connected to {DB_FILE}")
except Exception as e:
    print(f"❌ Failed to connect to database: {e}")
    exit()

print("\nType your SQL queries below.")
print("Type 'exit' or 'quit' to leave.")
print("\n💡 Example queries:")
print("  SELECT * FROM mlb_stat_leaders LIMIT 5;")
print("  SELECT year, COUNT(*) FROM mlb_stat_leaders GROUP BY year;")
print("  SELECT * FROM mlb_stat_leaders WHERE year = 1998;")
print("  SELECT * FROM mlb_stat_leaders WHERE stat LIKE '%Home Runs%';")
print("  SELECT * FROM mlb_stat_leaders WHERE player LIKE '%Bonds%';")
print("  SELECT stat, COUNT(*) AS total FROM mlb_stat_leaders GROUP BY stat ORDER BY total DESC LIMIT 10;")

while True:
    query = input("\nSQL> ").strip()
    if query.lower() in ["exit", "quit"]:
        print("👋 Goodbye!")
        break

    # Convenience shortcut for keyword search
    # Example: search player Bonds
    if query.lower().startswith("search"):
        parts = query.split()
        if len(parts) >= 3:
            column = parts[1]
            keyword = " ".join(parts[2:])
            query = f"SELECT * FROM mlb_stat_leaders WHERE {column} LIKE '%{keyword}%';"
        else:
            print("⚠️ Usage: search <column> <keyword>")
            continue

    if not query.endswith(";"):
        query += ";"

    try:
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("⚠️ No results found.")
        else:
            # Display results as table
            print("\n", df.to_string(index=False, max_rows=20))
            if len(df) > 20:
                print(f"\n📊 Showing first 20 rows of {len(df)} total")
    except Exception as e:
        print(f"❌ SQL Error: {e}")

conn.close()
