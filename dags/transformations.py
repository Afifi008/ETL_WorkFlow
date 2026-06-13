"""
Pure transformation functions — separated from the DAG so they can be
unit-tested without spinning up Airflow.

Rule of thumb: if a function takes a DataFrame in and returns a DataFrame out,
it belongs here, not in the DAG file.
"""

from __future__ import annotations

import pandas as pd


def clean_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing critical fields and remove negative revenue."""
    cleaned = df.dropna(subset=["customer_id", "product_category", "revenue"])
    cleaned = cleaned[cleaned["revenue"] >= 0]
    return cleaned.reset_index(drop=True)


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Sum revenue per product category, sorted high to low."""
    return (
        df.groupby("product_category", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
