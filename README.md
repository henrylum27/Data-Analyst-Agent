# Data Analyst Agent

Data Analyst Agent is a full-stack AI-powered analytics assistant that helps users understand CSV datasets quickly. Users can upload a CSV file, automatically profile the dataset, detect missing values and anomalies, generate SQL queries from natural-language questions, and create a business-focused executive summary.

The project is designed to run locally for free using Ollama, so no paid AI API is required. It uses FastAPI for the backend, React for the frontend, Pandas for data profiling, DuckDB for SQL analysis, and a local LLM for executive summary generation.

## Key Features

- Upload and analyze CSV files
- Automatically detect missing values and data quality issues
- Identify numeric anomalies and unusual values
- Generate executive summaries focused on business impact
- Explain how missing data may affect company decisions
- Generate and safely run SQL queries using DuckDB
- Download the executive summary as a PDF report
- Runs locally using Ollama with no paid API required