import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import plotly.express as px

# Connect to database
db_path = Path("mlb_data.db")
if not db_path.exists():
    st.error(f"❌ Database not found at {db_path}. Run db_import.py first.")
    st.stop()

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM mlb_stat_leaders", conn)
conn.close()

df["year"] = df["year"].astype(int)

st.title("⚾ MLB Stat Leaders Dashboard")
st.write("Explore historical MLB statistical leaders scraped from Baseball Almanac.")

# Sidebar year selector
years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)
year_data = df[df["year"] == selected_year]

# 🧹 Cleaning function
team_keywords = [
    "Yankees", "Dodgers", "Giants", "Red Sox", "White Sox", "Braves", "Pirates",
    "Cardinals", "Phillies", "Senators", "Athletics", "Cubs", "Indians",
    "Orioles", "Mets", "Padres", "Royals", "Angels", "Mariners", "Tigers", "Twins"
]

junk_keywords = ["Statistic", "Stat", "Stats", "Statistics"]

def is_team_or_garbage(stat_name: str):
    if not isinstance(stat_name, str) or stat_name.strip() == "":
        return True
    if stat_name.strip().title() in junk_keywords:
        return True
    if len(stat_name) > 30:
        return True
    for kw in team_keywords:
        if kw.lower() in stat_name.lower():
            return True
    return False

# Clean dataframe globally
clean_df = df[~df["stat"].apply(is_team_or_garbage)]


# Chart 1: Number of stats recorded each year
year_counts = clean_df.groupby("year").size().reset_index(name="num_stats")
fig2 = px.line(
    year_counts,
    x="year",
    y="num_stats",
    title="📈 Number of Recorded Stat Leaders per Year",
    markers=True
)
fig2.update_layout(xaxis_title="Year", yaxis_title="Number of Stat Records")
st.plotly_chart(fig2, use_container_width=True)

# Chart 2: Most common stat categories overall
top_categories = clean_df["stat"].value_counts().reset_index()
top_categories.columns = ["stat", "total_count"]
fig3 = px.bar(
    top_categories.head(20),
    x="stat",
    y="total_count",
    title="🏆 Most Common Stat Categories (All Years)",
)
fig3.update_layout(xaxis_title="Stat", yaxis_title="Total Count", xaxis_tickangle=45)
st.plotly_chart(fig3, use_container_width=True)

# Table of leaders for selected year
st.subheader(f"📅 Leaders in {selected_year}")
st.dataframe(year_data[["stat", "player", "team", "value"]])

with st.expander("🔗 Show original links"):
    st.write(year_data[["stat", "link"]])
