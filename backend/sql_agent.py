from llm import ask_local_llm


BLOCKED_SQL_KEYWORDS = [
    "insert",
    "update",
    "delete",
    "drop",
    "alter",
    "create",
    "copy",
    "attach",
    "detach",
    "replace",
    "truncate",
    "grant",
    "revoke",
]


def generate_sql_query(columns: list, user_question: str) -> str:
    """
    Generate a SQL query from a natural language question.
    The table name should always be uploaded_data.
    """

    prompt = f"""
You are a SQL data analyst.

Given this table:

Table name: uploaded_data

Columns:
{columns}

User question:
{user_question}

Write one SQL query that answers the user's question.

Rules:
- Use only the table uploaded_data.
- Return only SQL.
- Do not explain the SQL.
- Only write a SELECT query.
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, COPY, or any destructive command.
"""

    sql = ask_local_llm(prompt)

    return clean_sql(sql)


def clean_sql(sql: str) -> str:
    """
    Clean model output so only SQL remains.
    """

    sql = sql.strip()

    if "```" in sql:
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

    return sql


def is_safe_sql(query: str) -> bool:
    """
    Check if SQL is safe before running.
    Only SELECT queries are allowed.
    """

    cleaned = query.lower().strip()

    if not cleaned.startswith("select"):
        return False

    for keyword in BLOCKED_SQL_KEYWORDS:
        if keyword in cleaned:
            return False

    return True