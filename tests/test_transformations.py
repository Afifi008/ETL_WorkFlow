"""
Unit tests for the pure transformation functions.
These run fast in CI — no Airflow, no warehouse.
"""

from __future__ import annotations

from dags.transformations import aggregate_by_category, clean_sales


def test_clean_sales_drops_null_customers(sample_sales_df):
    cleaned = clean_sales(sample_sales_df)
    assert cleaned["customer_id"].notna().all()


def test_clean_sales_drops_negative_revenue(sample_sales_df):
    cleaned = clean_sales(sample_sales_df)
    assert (cleaned["revenue"] >= 0).all()


def test_clean_sales_keeps_valid_rows(sample_sales_df):
    cleaned = clean_sales(sample_sales_df)
    # Of 5 input rows, 2 are bad (null customer + negative revenue) → 3 valid
    assert len(cleaned) == 3


def test_aggregate_by_category_sums_revenue(sample_sales_df):
    cleaned = clean_sales(sample_sales_df)
    agg = aggregate_by_category(cleaned)
    electronics = agg.loc[agg["product_category"] == "Electronics", "revenue"].iloc[0]
    assert electronics == 300.0  # 100 + 200


def test_aggregate_is_sorted_descending(sample_sales_df):
    cleaned = clean_sales(sample_sales_df)
    agg = aggregate_by_category(cleaned)
    revenues = agg["revenue"].tolist()
    assert revenues == sorted(revenues, reverse=True)
