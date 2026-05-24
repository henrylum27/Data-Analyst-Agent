# Data Analyst Agent

Data Analyst Agent is a full-stack AI-powered analytics assistant that helps users analyze CSV datasets. Users can upload a CSV file, automatically profile the data, detect missing values and anomalies, generate business-focused executive summaries, ask natural-language data questions, run SQL with DuckDB, and download the summary as a PDF report.

This project runs locally for free using Ollama, so no paid AI API is required.

---

## Features

- Upload and analyze CSV files
- Preview dataset rows
- Detect missing values and data quality issues
- Detect numeric anomalies and unusual values
- Generate business-focused executive summaries
- Explain the business impact of missing values
- Generate SQL from natural-language questions
- Run SQL safely using DuckDB
- Download executive summary as a PDF
- Runs locally using Ollama

---

## Tech Stack

### Frontend

- React
- Vite
- Axios
- HTML2PDF.js
- CSS

### Backend

- FastAPI
- Pandas
- DuckDB
- Scikit-learn
- Python Multipart
- Requests

### AI

- Ollama
- Local open-source LLM such as `llama3.2`

---

## Project Structure

```text
Data Analyst Agent/
├── backend/
│   ├── main.py
│   ├── profiler.py
│   ├── anomalies.py
│   ├── llm.py
│   ├── sql_agent.py
│   └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── index.css
│   └── package.json
│
├── Sample Data/
│   └── sales.csv
│
├── README.md
└── .gitignore
```

---

# How to Run the Project Locally

To run this project, you need to run three things:

1. Ollama local AI model
2. FastAPI backend
3. React frontend

You should use three separate terminals.

---

## 1. Clone the Repository

```bash
git clone https://github.com/henrylum27/Data-Analyst-Agent.git
cd Data-Analyst-Agent
```

---

## 2. Install and Run Ollama

Download and install Ollama from:

```text
https://ollama.com
```

After installing Ollama, open a terminal and run:

```bash
ollama run llama3.2
```

Keep this terminal open while using the project.

This model is used to generate the AI executive summary locally.

---

## 3. Run the Backend

Open a new terminal.

Go to the backend folder:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

For Windows:

```bash
.venv\Scripts\activate
```

For macOS/Linux:

```bash
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install the dependencies manually:

```bash
pip install fastapi uvicorn pandas duckdb python-multipart requests scikit-learn
```

Start the backend server:

```bash
python -m uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

You can test the backend API documentation here:

```text
http://127.0.0.1:8000/docs
```

---

## 4. Run the Frontend

Open another new terminal.

Go to the frontend folder:

```bash
cd Frontend
```

Install frontend dependencies:

```bash
npm install
```

Start the frontend:

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

Open that link in your browser.

---

# Quick Start

Run these commands in three separate terminals.

## Terminal 1: Ollama

```bash
ollama run llama3.2
```

## Terminal 2: Backend

```bash
cd backend
python -m uvicorn main:app --reload
```

## Terminal 3: Frontend

```bash
cd Frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

---

## How to Use the App

1. Open the frontend in your browser.
2. Upload a CSV file.
3. Click **Analyze CSV**.
4. Review the dataset overview, missing values, column summary, and anomalies.
5. Click **Generate AI Summary**.
6. Review the business-focused executive summary.
7. Download the summary as a PDF report.
8. Ask a data question, such as:

```text
Show total sales by region
```

or:

```text
Which product has the highest profit?
```

The app will generate SQL, run it using DuckDB, and return the result.

---

## Example Questions

```text
Show total sales by region
```

```text
Show total profit by product
```

```text
Which sales rep has the highest total sales?
```

```text
Show average discount by sales channel
```

```text
Which products have negative or missing profit?
```

```text
Show sales by payment method
```

```text
Show profit by sales channel
```

---

## API Endpoints

### `GET /`

Checks whether the backend is running.

### `POST /upload`

Uploads and profiles a CSV file.

Returns:

- Dataset preview
- Row count
- Column count
- Missing value count
- Column summary
- Anomaly detection results

### `POST /summary`

Generates a business-focused executive summary using Ollama.

The summary focuses on:

- Dataset overview
- Missing values
- Business impact of data quality issues
- Anomalies and risk areas
- Recommendations
- Suggested next analysis

### `POST /generate-sql`

Generates a SQL query from a natural-language question.

### `POST /run-sql`

Generates and runs a safe SQL query using DuckDB.

Only read-only SQL analysis is allowed.

---

## Privacy and Security

This project is designed to run locally.

- Uploaded CSV files are processed locally.
- No paid external AI API is required.
- AI summaries are generated using Ollama on the user's machine.
- SQL queries are restricted to read-only analysis.
- The app does not execute arbitrary AI-generated Python code.
- Uploaded data should not be committed to GitHub unless it is sample or synthetic data.

---

## Why This Project Is Useful

Many business users receive raw CSV files but may not immediately understand the data quality issues inside them. This tool helps identify missing values, anomalies, and reporting risks before the data is used for decision-making.

For example:

- Missing `region` values can affect regional sales reporting.
- Missing `product` values can affect product profitability analysis.
- Missing `sales` or `profit` values can affect revenue and margin reporting.
- Missing `sales_rep` values can affect employee performance tracking.
- Missing `payment_method` values can affect customer payment behavior analysis.
- Missing `sales_channel` values can affect channel performance reporting.
- Outliers or negative profit values may require business investigation.

The goal is not only to summarize data, but also to explain why data issues matter to the company.

---

## Notes

This project is intended as a portfolio and learning project. It is not production-ready without additional security, authentication, logging, file validation, error handling, and deployment hardening.