import pandas as pd


def profile_dataframe(df: pd.DataFrame) -> dict:
    columns_summary = []
    missing_columns = []
    numeric_summary = []

    for col in df.columns:
        missing_count = int(df[col].isna().sum())
        missing_pct = round(df[col].isna().mean() * 100, 2)

        columns_summary.append({
            "column": col,
            "dtype": str(df[col].dtype),
            "missing": missing_count,
            "missing_pct": missing_pct,
            "unique_values": int(df[col].nunique())
        })

        if missing_count > 0:
            missing_columns.append({
                "column": col,
                "missing_count": missing_count,
                "missing_pct": missing_pct
            })

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        numeric_summary.append({
            "column": col,
            "min": None if pd.isna(df[col].min()) else float(df[col].min()),
            "max": None if pd.isna(df[col].max()) else float(df[col].max()),
            "mean": None if pd.isna(df[col].mean()) else round(float(df[col].mean()), 2),
            "median": None if pd.isna(df[col].median()) else round(float(df[col].median()), 2),
            "missing": int(df[col].isna().sum())
        })

    duplicate_rows = int(df.duplicated().sum())

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "total_missing": int(df.isna().sum().sum()),
        "duplicate_rows": duplicate_rows,
        "columns_summary": columns_summary,
        "missing_columns": missing_columns,
        "numeric_summary": numeric_summary
    }