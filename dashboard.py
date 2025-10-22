import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import plotly.express as px

# Database connection
db_path = Path("mlb_data.db")
if not db_path.exists():
    st.error(f"❌ Database not found at {db_path}. Run db_import.py first.")
    st.stop()

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM mlb_stat_leaders", conn)
conn.close()

# Convert year to integer for sorting
df["year"] = df["year"].astype(int)

st.title("⚾ MLB Stat Leaders Dashboard")
st.write("Explore historical MLB statistical leaders scraped from Baseball Almanac.")

# Sidebar filters
years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", years)

# Filter for selected year
year_data = df[df["year"] == selected_year]

# Chart 1: Top stats for selected year
top_stats = year_data.groupby("stat").size().reset_index(name="count")
fig1 = px.bar(
    top_stats.sort_values("count", ascending=False),
    x="stat",
    y="count",
    title=f"📊 Stat Categories in {selected_year}",
)
fig1.update_layout(xaxis_title="Stat Category", yaxis_title="Occurrences", xaxis_tickangle=45)
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Number of stats recorded each year
year_counts = df.groupby("year").size().reset_index(name="num_stats")
fig2 = px.line(
    year_counts,
    x="year",
    y="num_stats",
    title="📈 Number of Recorded Stat Leaders per Year",
    markers=True
)
fig2.update_layout(xaxis_title="Year", yaxis_title="Number of Stat Records")
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Most common stat categories overall
top_categories = df["stat"].value_counts().reset_index()
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

# Optional: Show links
with st.expander("🔗 Show original links"):
    st.write(year_data[["stat", "link"]])
