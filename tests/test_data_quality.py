"""
Data quality tests — assertions on the data itself, not the code.

These run against the sample CSV shipped with the repo. In a real project
they'd run against a small fixture pulled from the warehouse.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

RAW_CSV = Path(__file__).resolve().parent.parent / "data" / "raw_sales.csv"


@pytest.fixture(scope="module")
def raw_df() -> pd.DataFrame:
    return pd.read_csv(RAW_CSV)


def test_raw_has_required_columns(raw_df):
    expected = {"order_id", "customer_id", "product_category", "revenue", "order_date"}
    assert expected.issubset(raw_df.columns)


def test_raw_order_ids_are_unique(raw_df):
    assert raw_df["order_id"].is_unique, "Duplicate order_id values found"


def test_raw_has_known_categories(raw_df):
    known = {"Electronics", "Books", "Clothing"}
    unknown = set(raw_df["product_category"].dropna()) - known
    assert not unknown, f"Unknown product categories: {unknown}"


def test_raw_revenue_within_expected_range(raw_df):
    # Sanity check — a single order over $100k is almost certainly a bug
    assert raw_df["revenue"].max() < 100_000
