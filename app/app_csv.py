import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import base64

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
OUTPUT_DIR = PROJECT_DIR / "output"
ASSETS_DIR = PROJECT_DIR / "assets"

# ---------------------------------------------------------
# Helpers
# ---------------------------------------------------------
def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

python_b64 = img_to_base64(ASSETS_DIR / "python.png")
trophy_b64 = img_to_base64(ASSETS_DIR / "trophy.png")

# ---------------------------------------------------------
# Page config
# ---------------------------------------------------------
st.set_page_config(
    page_title="PyLab Homework Leaderboard",
    layout="wide",
)

# ---------------------------------------------------------
# Header (images like emojis)
# ---------------------------------------------------------
st.markdown(
    f"""
    <h1 style="display:flex; align-items:center; gap:10px;">
        <img src="data:image/png;base64,{python_b64}" width="38"/>
        PyLab Homework Leaderboard
        <img src="data:image/png;base64,{trophy_b64}" width="38"/>
    </h1>
    <p style="color:#555">
        This dashboard displays student rankings based on total homework scores.
    </p>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------
@st.cache_data
def load_leaderboard():
    path = OUTPUT_DIR / "leaderboard.csv"
    if not path.exists():
        st.error(f"CSV file not found: {path}")
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_results():
    path = OUTPUT_DIR / "results_by_lecture.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


df = load_leaderboard()
df_lectures = load_results()

if df.empty:
    st.stop()

# ---------------------------------------------------------
# MAIN KPIs
# ---------------------------------------------------------
k1, k2, k3 = st.columns(3)
k1.metric("🏆 Highest Score", int(df["total_score"].max()))
k2.metric("📘 Total Lectures", int(df["lectures"].max()))
k3.metric("👥 Total Students", len(df))

st.divider()

# ---------------------------------------------------------
# Sidebar search
# ---------------------------------------------------------
st.sidebar.header("🔍 Search Student")
student_name = st.sidebar.text_input("Enter student name")

# ---------------------------------------------------------
# SEARCH STUDENT
# ---------------------------------------------------------
if student_name:
    s_df = df[df["username"].str.contains(student_name, case=False, na=False)]

    if s_df.empty:
        st.warning("Student not found.")
    else:
        row = s_df.iloc[0]
        username = row["username"]
        avg = round(row["total_score"] / row["lectures"], 2)

        st.subheader(f"👤 Student Profile: {username}")

        a, b, c = st.columns(3)
        a.metric("🏆 Total Score", int(row["total_score"]))
        b.metric("📊 Average Score", avg)
        c.metric("📘 Lectures Passed", int(row["lectures"]))

        # ---------------------------------------------
        # Results by lecture (solid bars, one line)
        # ---------------------------------------------
        if not df_lectures.empty:
            st.subheader("📈 Results by Lecture")

            TOTAL = 30  # bar width

            student_lectures = (
                df_lectures[df_lectures["username"] == username]
                .sort_values("lecture")
            )

            for _, r in student_lectures.iterrows():
                lecture = int(r["lecture"])
                score = int(r["score"])

                filled = int(score / 100 * TOTAL)
                empty = TOTAL - filled

                bar = (
    f"<span style='color:#3498db'>{"█" * filled}</span>"
    f"<span style='color:#cfe8f9'>{"█" * empty}</span>")

                st.markdown(
                    f"`Lecture {lecture}` | **{score}** | "
                    f"<span style='color:#3498db; font-family:monospace'>{bar}</span>",
                    unsafe_allow_html=True,
                )

        st.divider()

# ---------------------------------------------------------
# Top 10 chart
# ---------------------------------------------------------
st.subheader("🏅 Top 10 Students")

fig = px.bar(
    df.head(10),
    x="username",
    y="total_score",
    color_discrete_sequence=["#3498db"],
)

fig.update_layout(showlegend=False)
st.plotly_chart(fig, width="stretch")

# ---------------------------------------------------------
# Full leaderboard
# ---------------------------------------------------------
st.subheader("📊 Full Leaderboard")
st.dataframe(df, hide_index=True, width="stretch")


