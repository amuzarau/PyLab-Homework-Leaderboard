🏆 PyLab Homework Leaderboard

A professional ETL + Analytics + Visualization project that processes homework results from Excel files, builds a leaderboard, and presents it through an interactive Streamlit dashboard with student profiles and downloadable reports.

Live App: https://pylab-homework-leaderboard.streamlit.app/

Repository: https://github.com/amuzarau/PyLab-Homework-Leaderboard

📌 Project Overview

This project demonstrates a real-world data pipeline:

Ingests homework results from Excel files

Cleans and aggregates scores

Builds a leaderboard

Visualizes results in a Streamlit web app

Generates student profile reports (PNG & PDF)

Ready for automation and production deployment

🧰 Tech Stack
Core

Python 3.12+

Pandas

Streamlit

Plotly

Pillow (PIL) — PNG report generation

ReportLab — PDF report generation

DevOps / Architecture

GitHub

Streamlit Cloud

Docker / Docker Compose (planned)

Apache Airflow (planned)

📁 Project Structure
PyLab-Homework-Leaderboard/
│
├── app/
│   └── app_csv.py               # Streamlit dashboard
│
├── etl/
│   ├── extract.py               # Excel → CSV
│   └── transform.py             # Cleaning & aggregation
│
├── output/
│   ├── leaderboard.csv          # Final leaderboard
│   └── results_by_lecture.csv   # Per-lecture scores (optional)
│
├── assets/
│   ├── python.png
│   └── trophy.png
│
├── requirements.txt
└── README.md

▶️ How to Run Locally
1) Clone repository
git clone https://github.com/amuzarau/PyLab-Homework-Leaderboard.git
cd PyLab-Homework-Leaderboard

2) Create & activate venv
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

3) Install dependencies
pip install -r requirements.txt

4) Put Excel files

Place your Excel input files here:

input/
├── lecture_1_results.xlsx
├── lecture_2_results.xlsx
├── lecture_3_results.xlsx

5) Run ETL
python etl/extract.py
python etl/transform.py

6) Output files (created automatically)
output/
├── leaderboard.csv
└── results_by_lecture.csv

7) Run Streamlit app
streamlit run app/app_csv.py

📊 Application Features
🏆 Leaderboard

Student ranking by total score

KPIs: Highest score, Total lectures, Total students

Top-10 chart

Full sortable table

👤 Student Profile

Total Score

Average Score per lecture

Lectures Passed

Results by lecture with progress bars

Downloadable PDF and PNG profile report

🔄 ETL Flow Diagram
flowchart TD
    A[Excel Files in input/] --> B[extract.py]
    B --> C[CSV Files in input/]
    C --> D[transform.py]
    D --> E[output/leaderboard.csv]
    D --> F[output/results_by_lecture.csv]

🧠 Application Architecture
flowchart LR
    U[User Browser] --> S[Streamlit App]
    S --> O[(output/*.csv)]
    O --> S
    S --> P[Plotly Charts]
    S --> R[PDF/PNG Reports]

👤 Student Profile Logic
sequenceDiagram
    participant User
    participant App as Streamlit App
    participant CSV as CSV files
    participant Rep as Report Generator

    User->>App: Search student name
    App->>CSV: Load leaderboard.csv
    App->>CSV: Load results_by_lecture.csv
    App->>User: Show profile + lecture bars
    User->>App: Download PDF/PNG
    App->>Rep: Generate report
    Rep-->>User: File download

🚀 Future Improvements
🔄 Pipeline Automation with Apache Airflow (Docker Compose)

Goal: automate the full flow:

Excel files
↓
extract.py (xlsx → csv)
↓
transform.py (cleaning, aggregation)
↓
output/*.csv
↓
GitHub push
↓
Streamlit Cloud auto-redeploy

flowchart TD
    A[New Excel Files] --> B[Airflow DAG]
    B --> C[Run extract.py]
    C --> D[Run transform.py]
    D --> E[Update output/*.csv]
    E --> F[Git commit & push]
    F --> G[Streamlit Cloud redeploy]

🗄 Database Backend via Docker Compose (PostgreSQL / MySQL)

Store leaderboard history

Enable advanced analytics

Serve data via API later

flowchart LR
    ETL[ETL Pipeline] --> DB[(PostgreSQL/MySQL)]
    DB --> APP[Streamlit App]
