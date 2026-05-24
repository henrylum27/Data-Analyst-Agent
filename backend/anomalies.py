import pandas as pd


def detect_numeric_anomalies(df: pd.DataFrame, z_threshold: float = 3.0) -> list:
    results = []

    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        series = df[col].dropna()

        if len(series) < 5 or series.std() == 0:
            continue

        z_scores = (series - series.mean()) / series.std()
        outliers = series[abs(z_scores) > z_threshold]

        if len(outliers) > 0:
            results.append({
                "column": col,
                "outlier_count": int(len(outliers)),
                "min_outlier": float(outliers.min()),
                "max_outlier": float(outliers.max())
            })

    return results