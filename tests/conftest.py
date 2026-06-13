"""
Shared pytest fixtures.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

# Make `dags/` importable in tests without installing the project as a package.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def sample_sales_df() -> pd.DataFrame:
    """Small synthetic dataset that mirrors the production schema."""
    return pd.DataFrame(
        [
            {"order_id": 1, "customer_id": "C001", "product_category": "Electronics", "revenue": 100.0},
            {"order_id": 2, "customer_id": "C002", "product_category": "Books",       "revenue":  20.0},
            {"order_id": 3, "customer_id": None,   "product_category": "Books",       "revenue":  15.0},  # null customer
            {"order_id": 4, "customer_id": "C003", "product_category": "Clothing",    "revenue": -50.0},  # negative
            {"order_id": 5, "customer_id": "C004", "product_category": "Electronics", "revenue": 200.0},
        ]
    )
