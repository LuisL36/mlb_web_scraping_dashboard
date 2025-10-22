import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path
import plotly.express as px

# Database connection
db_path = Path(__file__).parent / "mlb_data.db"

if not db_path.exists():
    st.error(f"❌ Database file not found at {db_path}")
    st.stop()

conn = sqlite3.connect(db_path)
df = pd.read_sql_query("SELECT * FROM mlb_yearly_events", conn)
conn.close()

# Data preprocessing
df["year"] = df["year"].astype(int)
event_counts = df.groupby("year").size().reset_index(name="count")

# App title
st.title("⚾ MLB History Dashboard")
st.write("Explore historical baseball data scraped from Baseball Almanac.")

# Year selector
years = sorted(df["year"].unique())
selected_year = st.selectbox("Select Year:", years)

# Chart 1: Events for selected year
fig1 = px.bar(
    event_counts[event_counts["year"] == selected_year],
    x="year",
    y="count",
    title=f"Number of MLB Events in {selected_year}"
)
fig1.update_layout(xaxis_title="Year", yaxis_title="Event Count")
st.plotly_chart(fig1, use_container_width=True)

# Chart 2: Histogram of recorded years
fig2 = px.histogram(
    event_counts,
    x="year",
    y="count",
    nbins=30,
    title="Distribution of Recorded Years"
)
fig2.update_layout(xaxis_title="Year", yaxis_title="Count")
st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Yearly data growth
event_counts["cumulative"] = event_counts["count"].cumsum()
fig3 = px.line(
    event_counts,
    x="year",
    y="cumulative",
    title="Cumulative Growth of Recorded Years"
)
fig3.update_layout(xaxis_title="Year", yaxis_title="Cumulative Count")
st.plotly_chart(fig3, use_container_width=True)

# Clickable link to Almanac page
selected_link = df[df["year"] == selected_year]["link"].values[0]
st.markdown(
    f"📎 [Open Baseball Almanac Page for {selected_year}]({selected_link})"
)

st.success("✅ Dashboard ready!")
