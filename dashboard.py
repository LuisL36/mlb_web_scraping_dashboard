import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.title("⚾ MLB History Dashboard")
st.write("Explore historical baseball data scraped from Baseball Almanac.")

conn = sqlite3.connect("mlb_data.db")
df = pd.read_sql_query("SELECT * FROM mlb_yearly_events", conn)

# Filter selection
years = sorted(df["year"].unique())
selected_year = st.selectbox("Select Year:", years)

filtered_df = df[df["year"] == selected_year]

# Visualizations
st.subheader(f"Top MLB Events in {selected_year}")
fig1 = px.bar(filtered_df, x="year", y="link", title=f"Events for {selected_year}")
st.plotly_chart(fig1)

fig2 = px.histogram(df, x="year", nbins=30, title="Distribution of Recorded Years")
st.plotly_chart(fig2)

fig3 = px.line(df, x="year", y=df.index, title="Yearly Data Growth")
st.plotly_chart(fig3)

st.write("✅ Dashboard ready!")
