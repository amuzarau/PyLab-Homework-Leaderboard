# 🏆 PyLab Homework Leaderboard

A professional **ETL + Analytics + Visualization** project that processes homework results from Excel files, builds a leaderboard, and presents it through an interactive **Streamlit dashboard** with student profiles and downloadable reports.

🔗 **Live App:**  
https://pylab-homework-leaderboard.streamlit.app/

🔗 **Repository:**  
https://github.com/amuzarau/PyLab-Homework-Leaderboard

---

## 📌 Project Overview

This project demonstrates a **real-world data pipeline**:

- Ingests homework results from Excel files
- Cleans and aggregates scores
- Builds a leaderboard
- Visualizes results in a Streamlit web app
- Generates **student profile reports** (PNG & PDF)
- Is ready for **full automation** and **production deployment**

---

## 🧰 Tech Stack

### Core
- **Python 3.12+**
- **Pandas** — data processing
- **Streamlit** — interactive dashboard
- **Plotly** — charts
- **Pillow (PIL)** — PNG report generation
- **ReportLab** — PDF report generation

### DevOps / Architecture
- **GitHub** — version control
- **Streamlit Cloud** — deployment
- **Docker / Docker Compose** — containerization (planned)
- **Apache Airflow** — pipeline automation (planned)

---

## 📁 Project Structure

PyLab-Homework-Leaderboard/
│
├── app/
│ └── app_csv.py # Streamlit dashboard
│
├── etl/
│ ├── extract.py # Excel → CSV
│ └── transform.py # Cleaning & aggregation
│
├── output/
│ ├── leaderboard.csv # Final leaderboard
│ └── results_by_lecture.csv # Per-lecture scores
│
├── assets/
│ ├── python.png
│ └── trophy.png
│
├── requirements.txt
└── README.md

yaml
Копировать код

---

## ▶️ How to Run Locally

### 1️⃣ Clone the repository
```bash
git clone https://github.com/amuzarau/PyLab-Homework-Leaderboard.git
cd PyLab-Homework-Leaderboard
2️⃣ Create & activate virtual environment
bash
Копировать код
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
3️⃣ Install dependencies
bash
Копировать код
pip install -r requirements.txt
4️⃣ Place Excel input files
Put all homework Excel files into the input/ folder:

css
Копировать код
input/
├── lecture_1_results.xlsx
├── lecture_2_results.xlsx
├── lecture_3_results.xlsx
5️⃣ Run ETL pipeline
bash
Копировать код
python etl/extract.py
python etl/transform.py
6️⃣ Output files
After running ETL, the following files will appear:

lua
Копировать код
output/
├── leaderboard.csv
└── results_by_lecture.csv
7️⃣ Run Streamlit app
bash
Копировать код
streamlit run app/app_csv.py
📊 Application Features
🏆 Leaderboard
Total score ranking

KPIs:

Highest score

Total lectures

Total students

👤 Student Profile
Total score

Average score per lecture

Lectures passed

Per-lecture progress bars

Downloadable reports:

📄 PDF

🖼 PNG (portrait layout)

📈 Visual Analytics
Top-10 bar chart

Full sortable leaderboard table

🔄 ETL Flow Diagram (Mermaid)
mermaid
Копировать код
flowchart TD
    A[Excel Files] --> B[extract.py]
    B --> C[CSV Files]
    C --> D[transform.py]
    D --> E[leaderboard.csv]
    D --> F[results_by_lecture.csv]
🧠 Application Architecture
mermaid
Копировать код
flowchart LR
    User -->|Browser| Streamlit
    Streamlit --> CSV[(CSV Files)]
    CSV --> Streamlit
    Streamlit -->|Charts| Plotly
    Streamlit -->|Reports| PDF_PNG[PDF / PNG Generator]
👤 Student Profile Logic (Sequence Diagram)
mermaid
Копировать код
sequenceDiagram
    participant User
    participant Streamlit
    participant CSV
    participant Report

    User->>Streamlit: Search student
    Streamlit->>CSV: Load leaderboard
    Streamlit->>CSV: Load results_by_lecture
    Streamlit->>User: Display profile & bars
    User->>Streamlit: Download report
    Streamlit->>Report: Generate PDF / PNG
    Report->>User: Download file
🚀 Future Improvements
🔄 Full Pipeline Automation (Apache Airflow)
The entire ETL + deployment flow can be fully automated using Apache Airflow, running inside Docker Compose.

Automated Flow:
scss
Копировать код
Excel files
   ↓
extract.py   (xlsx → csv)
   ↓
transform.py (cleaning, aggregation)
   ↓
output/*.csv
   ↓
GitHub push
   ↓
Streamlit Cloud auto-redeploy
Airflow Automation Diagram
mermaid
Копировать код
flowchart TD
    A[New Excel Files] --> B[Airflow DAG]
    B --> C[extract.py]
    C --> D[transform.py]
    D --> E[output CSV files]
    E --> F[Git Commit & Push]
    F --> G[Streamlit Cloud Auto-Redeploy]
🐳 Docker Compose Usage
Airflow services (scheduler, webserver, workers)

ETL environment

Database backend

GitHub credentials via secrets

🗄 Database Backend (Planned)
Add a relational database using Docker Compose:

PostgreSQL or MySQL

Replace CSV storage or work in hybrid mode

Enable:

Historical data

Advanced analytics

API integration

mermaid
Копировать код
flowchart LR
    ETL --> Database[(PostgreSQL / MySQL)]
    Database --> Streamlit
📌 Why This Project Matters
This project demonstrates:

Real ETL pipeline design

Data cleaning & aggregation

Analytics & visualization

Report generation

Cloud deployment

Production-ready architecture

Clear path to orchestration with Apache Airflow

👨‍💻 Author
