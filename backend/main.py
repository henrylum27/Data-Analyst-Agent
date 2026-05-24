import duckdb
from sql_agent import generate_sql_query, is_safe_sql
from pydantic import BaseModel
from llm import generate_executive_summary
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO

from profiler import profile_dataframe
from anomalies import detect_numeric_anomalies

app = FastAPI(title="Data Analyst Agent API")
class SQLRequest(BaseModel):
    question: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Data Analyst Agent Backend is running"
    }


@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    contents = await file.read()
    decoded = contents.decode("utf-8")

    df = pd.read_csv(StringIO(decoded))

    profile = profile_dataframe(df)
    anomalies = detect_numeric_anomalies(df)

    preview = df.head(10).fillna("").to_dict(orient="records")

    return {
        "filename": file.filename,
        "preview": preview,
        "profile": profile,
        "anomalies": anomalies
    }

@app.post("/summary")
async def generate_summary(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    contents = await file.read()
    decoded = contents.decode("utf-8")

    df = pd.read_csv(StringIO(decoded))

    profile = profile_dataframe(df)
    anomalies = detect_numeric_anomalies(df)

    summary = generate_executive_summary(profile, anomalies)

    return {
        "filename": file.filename,
        "summary": summary
    }

@app.post("/generate-sql")
async def generate_sql(file: UploadFile = File(...), question: str = ""):
    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    if not question:
        return {"error": "Question is required"}

    contents = await file.read()
    decoded = contents.decode("utf-8")

    df = pd.read_csv(StringIO(decoded))

    columns = df.columns.tolist()

    sql_query = generate_sql_query(columns, question)

    safe = is_safe_sql(sql_query)

    return {
        "filename": file.filename,
        "question": question,
        "sql": sql_query,
        "is_safe": safe
    }

@app.post("/run-sql")
async def run_sql(file: UploadFile = File(...), question: str = ""):
    if not file.filename.endswith(".csv"):
        return {"error": "Only CSV files are allowed"}

    if not question:
        return {"error": "Question is required"}

    contents = await file.read()
    decoded = contents.decode("utf-8")

    df = pd.read_csv(StringIO(decoded))

    columns = df.columns.tolist()

    sql_query = generate_sql_query(columns, question)

    if not is_safe_sql(sql_query):
        return {
            "error": "Generated SQL was blocked because it was not safe.",
            "sql": sql_query
        }

    try:
        connection = duckdb.connect(database=":memory:")
        connection.register("uploaded_data", df)

        result_df = connection.execute(sql_query).df()

        return {
            "filename": file.filename,
            "question": question,
            "sql": sql_query,
            "results": result_df.head(50).fillna("").to_dict(orient="records")
        }

    except Exception as e:
        return {
            "error": "SQL execution failed.",
            "sql": sql_query,
            "details": str(e)
        }