import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os

# Helper: Load data
@st.cache_data
def load_data():
    db_path = os.path.join("data", "mlb_data.db")
    conn = sqlite3.connect(db_path)
    
    # Load yearly events
    events_df = pd.read_sql_query("SELECT * FROM mlb_yearly_events", conn)
    
    # Load player stats
    players_df = pd.read_sql_query("SELECT * FROM mlb_player_stats", conn)
    
    conn.close()
    return events_df, players_df


# Main dashboard function
def main():
    st.title("⚾ MLB Historical Data Dashboard")
    st.write("Explore historical MLB events and player statistics.")
    
    # Load data
    events_df, players_df = load_data()
    
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Year selection
    years = sorted(events_df["Year"].unique())
    selected_year = st.sidebar.selectbox("Select Year", years, index=0)
    
    # Player selection
    top_players = players_df["Player"].unique()
    selected_player = st.sidebar.selectbox("Select Player", top_players)
    
    # Filtered datasets
    events_filtered = events_df[events_df["Year"] == selected_year]
    player_filtered = players_df[players_df["Player"] == selected_player]
    
    # 1️. Bar chart: Events per Year
    st.subheader(f"MLB Events in {selected_year}")
    bar_fig = px.bar(events_filtered, x="Event", y="Count", title=f"Events for {selected_year}",
                     labels={"Event":"Event Name", "Count":"Occurrences"})
    st.plotly_chart(bar_fig)
    
    # 2. Line chart: Player performance over years
    st.subheader(f"{selected_player} Performance Over Years")
    player_history = players_df[players_df["Player"] == selected_player]
    
    line_fig = px.line(player_history, x="Year", y="Statistic", title=f"{selected_player} Stats Over Time",
                       labels={"Statistic":"Stat Value"})
    st.plotly_chart(line_fig)
    
    # 3. Histogram: Event distribution
    st.subheader("Distribution of Events Across All Years")
    hist_fig = px.histogram(events_df, x="Event", title="Event Occurrences Distribution",
                            labels={"Event":"Event Name"})
    st.plotly_chart(hist_fig)
    
    # Display filtered tables
    st.subheader("Filtered Events Data")
    st.dataframe(events_filtered)
    
    st.subheader("Filtered Player Stats")
    st.dataframe(player_filtered)

# Run the app
if __name__ == "__main__":
    main()
