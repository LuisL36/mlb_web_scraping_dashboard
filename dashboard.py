import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# Connect to database
conn = sqlite3.connect(os.path.join("data", "mlb_data.db"))

# Load data
df = pd.read_sql_query("SELECT * FROM mlb_yearly_events", conn)

# Streamlit UI
st.title("MLB Historical Events Dashboard")
st.subheader("Top Events by Year")
st.dataframe(df.head())

# Example Plot
fig = px.bar(df, x="Year", y="EventCount", title="Events per Year")
st.plotly_chart(fig)

conn.close()
