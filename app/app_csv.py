import streamlit as st
import pandas as pd
import plotly.express as px
import os
# redeploy test

# ---------------------------------------------------------
# Streamlit Page Settings
# ---------------------------------------------------------
st.set_page_config(
    page_title="PyLab Homework Leaderboard",
    layout="wide",
    page_icon="🏆"
)

# ---------------------------------------------------------
# Load Data (CSV-based)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    csv_path = "output/leaderboard.csv"   # ✔ Correct path for Streamlit Cloud
    if not os.path.exists(csv_path):
        st.error(f"CSV file not found: {csv_path}")
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    return df


df = load_data()
if df.empty:
    st.stop()

# ---------------------------------------------------------
# Title + Info
# ---------------------------------------------------------
st.title("🏆 PyLab Homework Leaderboard (CSV Version)")
st.markdown("This dashboard displays student rankings based on total homework scores.")

# ---------------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("🔍 Filters")

username_filter = st.sidebar.text_input("Search by username:")

filtered_df = df.copy()
if username_filter:
    filtered_df = filtered_df[filtered_df["username"].str.contains(username_filter, case=False)]

# ---------------------------------------------------------
# KPI Cards (Top summary)
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🧑‍🎓 Total Students", len(df))

with col2:
    st.metric("📘 Total Lectures", df["lectures"].max())

with col3:
    st.metric("💯 Highest Score", df["total_score"].max())

# ---------------------------------------------------------
# Top 10 Bar Chart
# ---------------------------------------------------------
st.subheader("🏅 Top 10 Students")

top10 = filtered_df.head(10)

fig = px.bar(
    top10,
    x="username",
    y="total_score",
    text="total_score",
    color="total_score",
    color_continuous_scale="Blues",
    title="Top 10 by Total Score",
)
fig.update_traces(textposition="outside")
fig.update_layout(xaxis_tickangle=45)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# Full Leaderboard Table
# ---------------------------------------------------------
st.subheader("📊 Full Leaderboard")

st.dataframe(
    filtered_df,
    hide_index=True,  # ✔ No index in table
    use_container_width=True
)

