# 🏆 PyLab Homework Leaderboard

**PyLab Homework Leaderboard** is a professional data pipeline and analytics project that demonstrates how raw Excel homework results can be transformed into a clean leaderboard and visualized via an interactive Streamlit dashboard.

The project follows **ETL principles**, supports **local execution and cloud deployment**, and is designed to be easily extended with automation tools like **Apache Airflow** and **Docker Compose**.

---

## 📌 Key Features

- 📥 Load homework results from multiple Excel files  
- 🔄 ETL pipeline (Extract → Transform → Load)  
- 🧮 Automatic aggregation of scores across lectures  
- 🏆 рейтинг студентов по суммарному баллу  
- 🔍 Student profile search with per-lecture progress bars  
- 📊 Interactive charts (Plotly)  
- 📄 Exportable student profile reports (PNG & PDF)  
- ☁️ Deployed on **Streamlit Cloud** (auto-redeploy on GitHub push)

---

## 🛠️ Technologies Used

### Core Stack
- **Python 3.12+**
- **Pandas** — data processing
- **Streamlit** — UI & dashboard
- **Plotly** — interactive charts

### Reporting
- **Pillow (PIL)** — PNG report generation
- **ReportLab** — PDF report generation

### Data Sources
- **Excel (.xlsx)** → CSV → aggregated CSV

### DevOps / Deployment
- **GitHub**
- **Streamlit Cloud**
- *(Planned)* Docker Compose, Apache Airflow

---

## 📂 Project Structure
PyLab-Homework-Leaderboard/
│
├── app/
│ └── app_csv.py # Streamlit application
│
├── etl/
│ ├── extract.py # xlsx → csv
│ └── transform.py # cleaning, aggregation, leaderboard
│
├── input/
│ └── *.xlsx # raw Excel homework files (put here)
│
├── output/
│ ├── leaderboard.csv # final leaderboard
│ └── results_by_lecture.csv # per-lecture scores (optional but recommended)
│
├── assets/
│ ├── python.png # Python logo
│ └── trophy.png # Trophy icon
│
├── requirements.txt
└── README.md


---

## ▶️ How to Run Locally

### 1️⃣ Put Excel files
Place **all homework Excel files** here:



input/
└── lecture_1_results.xlsx
└── lecture_2_results.xlsx
└── lecture_3_results.xlsx


Each file represents one lecture.

---

### 2️⃣ Run ETL pipeline

```bash
cd etl
python extract.py
python transform.py


After this step, two result files will appear in:

output/
├── leaderboard.csv
└── results_by_lecture.csv

3️⃣ Run Streamlit app
cd app
streamlit run app_csv.py


Open in browser:

http://localhost:8501

📊 ETL Flow Diagram
flowchart TD
    A[Excel files (.xlsx)] --> B[extract.py]
    B --> C[CSV files]
    C --> D[transform.py]
    D --> E[leaderboard.csv]
    D --> F[results_by_lecture.csv]

🧠 Application Architecture
flowchart LR
    Excel --> ETL
    ETL --> CSV[Aggregated CSV]
    CSV --> Streamlit
    Streamlit --> User[Web Browser]

👤 Student Profile Logic
sequenceDiagram
    participant User
    participant Streamlit
    participant CSV

    User->>Streamlit: Search student name
    Streamlit->>CSV: Load leaderboard.csv
    Streamlit->>CSV: Load results_by_lecture.csv
    Streamlit->>User: Show KPIs (Total / Avg / Lectures)
    Streamlit->>User: Show per-lecture bars
    Streamlit->>User: Export PDF / PNG

☁️ Deployment (Streamlit Cloud)

Push updated CSV files to GitHub:

output/leaderboard.csv
output/results_by_lecture.csv


Streamlit Cloud automatically:

pulls changes

clears cache

redeploys the app

No local database is required for deployment.

🚀 Future Improvements
🔄 Full Pipeline Automation (Apache Airflow)
flowchart TD
    A[New Excel files] --> B[Airflow DAG]
    B --> C[extract.py<br/>(xlsx → csv)]
    C --> D[transform.py<br/>(cleaning, aggregation)]
    D --> E[output/*.csv]
    E --> F[GitHub push]
    F --> G[Streamlit Cloud auto-redeploy]


Airflow DAG scheduled (daily / weekly)

Fully automated leaderboard updates

Versioned data in GitHub

🐳 Docker & Database Backend

Docker Compose orchestration:

Airflow

Streamlit

PostgreSQL / MySQL

Database as optional backend instead of CSV

Scalable for large datasets
