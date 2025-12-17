import base64
import io
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import black

# =========================================================
# Paths (works locally + Streamlit Cloud)
# Repo structure assumed:
#   app/app_csv.py
#   output/leaderboard.csv
#   output/results_by_lecture.csv
#   assets/python.png
#   assets/trophy.png
# =========================================================
BASE_DIR = Path(__file__).resolve().parent  # .../app
PROJECT_DIR = BASE_DIR.parent  # project root
OUTPUT_DIR = PROJECT_DIR / "output"
ASSETS_DIR = PROJECT_DIR / "assets"

LEADERBOARD_PATH = OUTPUT_DIR / "leaderboard.csv"
RESULTS_BY_LECTURE_PATH = OUTPUT_DIR / "results_by_lecture.csv"
PYTHON_ICON_PATH = ASSETS_DIR / "python.png"
TROPHY_ICON_PATH = ASSETS_DIR / "trophy.png"


# =========================================================
# Helpers
# =========================================================
def img_to_base64(path: Path) -> str | None:
    """Return base64 string for an image file, or None if not found/readable."""
    try:
        return base64.b64encode(path.read_bytes()).decode("utf-8")
    except Exception:
        return None


def safe_int(x, default=0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def get_student_lecture_rows(df_lectures: pd.DataFrame, username: str) -> pd.DataFrame:
    """Expect columns: username, lecture, score."""
    if df_lectures.empty:
        return pd.DataFrame()

    needed = {"username", "lecture", "score"}
    if not needed.issubset(set(df_lectures.columns)):
        return pd.DataFrame()

    out = df_lectures[df_lectures["username"] == username].copy()
    if out.empty:
        return out

    out["lecture"] = pd.to_numeric(out["lecture"], errors="coerce")
    out["score"] = pd.to_numeric(out["score"], errors="coerce")
    out = out.dropna(subset=["lecture", "score"]).sort_values("lecture")
    out["lecture"] = out["lecture"].astype(int)
    out["score"] = out["score"].astype(int)
    return out


def build_solid_bar(score: int, total_blocks: int = 34) -> str:
    """
    Solid bar (no spaces). Filled is blue, remaining is light blue.
    """
    score = max(0, min(100, int(score)))
    filled = int(round(score / 100 * total_blocks))
    empty = total_blocks - filled
    return (
        f"<span style='color:#3498db;'>{'█' * filled}</span>"
        f"<span style='color:#cfe8f9;'>{'█' * empty}</span>"
    )


# =========================================================
# Streamlit config
# =========================================================
st.set_page_config(
    page_title="PyLab Homework Leaderboard", layout="wide", page_icon="🏆"
)

python_b64 = img_to_base64(PYTHON_ICON_PATH)
trophy_b64 = img_to_base64(TROPHY_ICON_PATH)

# =========================================================
# Title: base64 images (no local file paths)
# Negative margins and baseline alignment.
# =========================================================
if python_b64 and trophy_b64:
    st.markdown(
        f"""
        <div style="display:flex; justify-content:center; align-items:baseline; gap:0; margin:0;">
            <img src="data:image/png;base64,{python_b64}"
                 style="height:40px; width:auto; margin-right:-6px; transform:translateY(4px);" />
            <span style="font-size:2.45rem; font-weight:800; line-height:1; margin:0 6px;">
                PyLab Homework Leaderboard
            </span>
            <img src="data:image/png;base64,{trophy_b64}"
                 style="height:40px; width:auto; margin-left:-6px; transform:translateY(4px);" />
        </div>
        <p style="text-align:center; color:#555; margin-top:6px;">
            This dashboard displays student rankings based on total homework scores.
        </p>
        """,
        unsafe_allow_html=True,
    )
else:
    # Fallback (if icons missing)
    st.title("PyLab Homework Leaderboard")
    st.caption(
        "This dashboard displays student rankings based on total homework scores."
    )

st.divider()


# =========================================================
# Load data
# =========================================================
@st.cache_data
def load_leaderboard(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data
def load_results_by_lecture(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


df = load_leaderboard(LEADERBOARD_PATH)
df_lectures = load_results_by_lecture(RESULTS_BY_LECTURE_PATH)

if df.empty:
    st.error(f"CSV file not found or empty: {LEADERBOARD_PATH}")
    st.stop()

# Required columns
for col in ["username", "lectures", "total_score"]:
    if col not in df.columns:
        st.error(
            f"leaderboard.csv must contain columns: username, lectures, total_score. Missing: {col}"
        )
        st.stop()

df["lectures"] = pd.to_numeric(df["lectures"], errors="coerce").fillna(0).astype(int)
df["total_score"] = (
    pd.to_numeric(df["total_score"], errors="coerce").fillna(0).astype(int)
)

# Sort
if "rating" in df.columns:
    df["rating"] = (
        pd.to_numeric(df["rating"], errors="coerce").fillna(999999).astype(int)
    )
    df = df.sort_values(["rating", "total_score"], ascending=[True, False]).reset_index(
        drop=True
    )
else:
    df = df.sort_values("total_score", ascending=False).reset_index(drop=True)

# =========================================================
# MAIN KPIs (Leaderboard)
# Order: Highest Score -> Total Lectures -> Total Students
# =========================================================
k1, k2, k3 = st.columns(3)
k1.metric("🏆 Highest Score", safe_int(df["total_score"].max()))
k2.metric("📘 Total Lectures", safe_int(df["lectures"].max()))
k3.metric("👥 Total Students", len(df))

st.divider()

# =========================================================
# Sidebar search
# =========================================================
st.sidebar.header("🔍 Search Student")
student_name = st.sidebar.text_input("Enter student name")

# =========================================================
# SEARCH STUDENT SECTION
# =========================================================
if student_name.strip():
    matches = df[
        df["username"]
        .astype(str)
        .str.contains(student_name.strip(), case=False, na=False)
    ]

    if matches.empty:
        st.warning("Student not found.")
    else:
        student_row = matches.iloc[0]
        username = str(student_row["username"])

        total_score = safe_int(student_row["total_score"])
        lectures_passed = safe_int(student_row["lectures"])
        avg_score = round(total_score / max(lectures_passed, 1), 2)

        # Lighter, natural profile icon color
        st.markdown(
            f"""
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
            <h2 style="margin-bottom:0.35rem; display:flex; align-items:center; gap:10px;">
                <i class="fa-solid fa-user" style="color:#b7bfc7;"></i>
                <span>Student Profile: {username}</span>
            </h2>
            """,
            unsafe_allow_html=True,
        )

        # KPI order: Total Score -> Average Score -> Lectures Passed
        a, b, c = st.columns(3)
        a.metric("🏆 Total Score", total_score)
        b.metric("📊 Average Score", avg_score)
        c.metric("📘 Lectures Passed", lectures_passed)

        st.markdown("## 📈 Results by Lecture")

        student_lectures = get_student_lecture_rows(df_lectures, username)

        if student_lectures.empty:
            st.info(
                "No per-lecture data found. "
                "If you want lecture bars, add output/results_by_lecture.csv with columns: username, lecture, score."
            )
        else:
            BAR_BLOCKS = 34
            for _, r in student_lectures.iterrows():
                lecture = safe_int(r["lecture"])
                score = safe_int(r["score"])
                bar_html = build_solid_bar(score, total_blocks=BAR_BLOCKS)

                st.markdown(
                    f"""
                    <div style="display:flex; align-items:center; gap:10px; margin:6px 0;">
                        <code style="min-width:90px;">Lecture {lecture}</code>
                        <div style="min-width:34px; font-weight:700;">{score}</div>
                        <div style="font-family:monospace; font-size:18px; line-height:1;">
                            {bar_html}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # =====================================================
        # Student report generation (PNG + PDF) 
        # =====================================================
        def generate_student_report_png(
            username_: str,
            total_score_: int,
            avg_score_: float,
            lectures_passed_: int,
            lectures_df: pd.DataFrame,
        ) -> io.BytesIO:
            # Portrait orientation
            W, H = 850, 1200
            img = Image.new("RGB", (W, H), "white")
            draw = ImageDraw.Draw(img)

            x0 = 60
            y = 50

            BLACK = (0, 0, 0)
            BLUE = (52, 152, 219)  # #3498db
            LIGHT = (207, 232, 249)  # #cfe8f9

            # Header
            draw.text((x0, y), f"Student Profile: {username_}", fill=BLACK)
            y += 55

            draw.text((x0, y), f"Total Score: {total_score_}", fill=BLACK)
            y += 30
            draw.text((x0, y), f"Average Score: {avg_score_}", fill=BLACK)
            y += 30
            draw.text((x0, y), f"Lectures Passed: {lectures_passed_}", fill=BLACK)
            y += 50

            draw.text((x0, y), "Results by Lecture", fill=BLACK)
            y += 35

            bar_x = x0 + 220
            bar_w = 520
            bar_h = 18
            row_h = 42

            for _, row in lectures_df.iterrows():
                lecture = int(row["lecture"])
                score = max(0, min(100, int(row["score"])))

                # TEXT — BLACK
                draw.text((x0, y + 2), f"Lecture {lecture}", fill=BLACK)
                draw.text((x0 + 120, y + 2), f"{score}", fill=BLACK)

                # FULL BAR (light background = remaining space)
                draw.rectangle([bar_x, y, bar_x + bar_w, y + bar_h], fill=LIGHT)

                # FILLED PART
                filled_w = int(bar_w * (score / 100))
                draw.rectangle([bar_x, y, bar_x + filled_w, y + bar_h], fill=BLUE)

                y += row_h

            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            return buf

        def generate_student_report_pdf(
            username_: str,
            total_score_: int,
            avg_score_: float,
            lectures_passed_: int,
            lectures_df: pd.DataFrame,
        ) -> io.BytesIO:
            buf = io.BytesIO()
            c = canvas.Canvas(buf, pagesize=A4)
            page_w, page_h = A4

            x0 = 50
            y = page_h - 70

            c.setFont("Helvetica-Bold", 16)
            c.drawString(x0, y, f"Student Profile: {username_}")
            y -= 30

            c.setFont("Helvetica", 12)
            c.drawString(x0, y, f"Total Score: {total_score_}")
            c.drawString(x0 + 170, y, f"Average Score: {avg_score_}")
            c.drawString(x0 + 360, y, f"Lectures Passed: {lectures_passed_}")
            y -= 35

            c.setFont("Helvetica-Bold", 13)
            c.drawString(x0, y, "Results by Lecture")
            y -= 18

            # Bars
            bar_x = x0 + 160
            bar_w = 320
            bar_h = 10
            row_h = 24

            blue = (52 / 255, 152 / 255, 219 / 255)
            light = (207 / 255, 232 / 255, 249 / 255)

            c.setFont("Helvetica", 11)
            c.setFillColor(black)

            for _, r in lectures_df.iterrows():
                lecture = safe_int(r["lecture"])
                score = max(0, min(100, safe_int(r["score"])))

                c.drawString(x0, y, f"Lecture {lecture}")
                c.drawRightString(x0 + 140, y, str(score))

                # background to 100
                c.setFillColorRGB(*light)
                c.rect(bar_x, y - 2, bar_w, bar_h, stroke=0, fill=1)

                # filled
                c.setFillColorRGB(*blue)
                filled_w = bar_w * (score / 100)
                c.rect(bar_x, y - 2, filled_w, bar_h, stroke=0, fill=1)

                # RESET TEXT COLOR
                c.setFillColor(black)

                y -= row_h

                if y < 70:
                    c.showPage()
                    y = page_h - 70
                    c.setFont("Helvetica", 11)

            c.showPage()
            c.save()
            buf.seek(0)
            return buf

        st.markdown("### 📥 Download Student Report")

        # Use lecture rows if available; otherwise create placeholders
        if student_lectures.empty:
            lectures_for_report = pd.DataFrame(
                [{"lecture": i + 1, "score": 0} for i in range(max(lectures_passed, 1))]
            )
        else:
            lectures_for_report = student_lectures

        col_dl1, col_dl2 = st.columns(2)

        with col_dl1:
            png_buf = generate_student_report_png(
                username_=username,
                total_score_=total_score,
                avg_score_=avg_score,
                lectures_passed_=lectures_passed,
                lectures_df=lectures_for_report,
            )
            st.download_button(
                label="⬇️ Download PNG report",
                data=png_buf,
                file_name=f"{username}_profile.png",
                mime="image/png",
                use_container_width=True,
            )

        with col_dl2:
            pdf_buf = generate_student_report_pdf(
                username_=username,
                total_score_=total_score,
                avg_score_=avg_score,
                lectures_passed_=lectures_passed,
                lectures_df=lectures_for_report,
            )
            st.download_button(
                label="⬇️ Download PDF report",
                data=pdf_buf,
                file_name=f"{username}_profile.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        st.divider()

# =========================================================
# Top 10 chart
# =========================================================
st.subheader("🏅 Top 10 Students")

top10 = df.head(10).copy()
fig = px.bar(
    top10,
    x="username",
    y="total_score",
    title="Top 10 by Total Score",
    color_discrete_sequence=["#3498db"],
)
fig.update_layout(xaxis_title="Student", yaxis_title="Total Score", showlegend=False)
st.plotly_chart(fig, width="stretch")

# =========================================================
# Full leaderboard
# =========================================================
st.subheader("📊 Full Leaderboard")
st.dataframe(df, hide_index=True, width="stretch")
