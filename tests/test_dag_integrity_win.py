"""
DAG integrity tests — no Airflow import needed.
We parse the DAG file using Python's ast module so this runs on Windows too.
"""

from __future__ import annotations

import ast
from pathlib import Path

DAG_FILE = Path(__file__).resolve().parent.parent / "dags" / "etl_sales_dag.py"


def _parse_dag_file():
    return ast.parse(DAG_FILE.read_text(encoding="utf-8"))


def test_dag_file_exists():
    """The DAG file must exist."""
    assert DAG_FILE.exists(), f"DAG file not found: {DAG_FILE}"


def test_dag_file_has_no_syntax_errors():
    """The DAG file must parse without syntax errors."""
    try:
        _parse_dag_file()
    except SyntaxError as e:
        assert False, f"Syntax error in DAG file: {e}"


def test_dag_file_imports_airflow():
    """The DAG file must import from airflow."""
    tree = _parse_dag_file()
    imports = [
        node for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
    ]
    airflow_imports = [
        node for node in imports
        if isinstance(node, ast.ImportFrom) and node.module and "airflow" in node.module
    ]
    assert airflow_imports, "No airflow imports found in DAG file"


def test_dag_id_is_etl_sales():
    """dag_id must be 'etl_sales'."""
    tree = _parse_dag_file()
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "dag_id":
            if isinstance(node.value, ast.Constant):
                assert node.value.value == "etl_sales"
                return
    assert False, "dag_id not found in DAG file"

def test_dag_has_retries():
    """default_args must include retries >= 1."""
    tree = _parse_dag_file()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == "retries":
                    assert isinstance(value, ast.Constant) and value.value >= 1
                    return
    assert False, "retries not found in default_args"

def test_dag_has_owner():
    """default_args must include an owner."""
    tree = _parse_dag_file()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and key.value == "owner":
                    assert isinstance(value, ast.Constant) and value.value
                    return
    assert False, "owner not found in default_args"

def test_dag_has_three_tasks():
    """DAG must define extract, transform, and load tasks."""
    tree = _parse_dag_file()
    task_ids = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.keyword) and node.arg == "task_id":
            if isinstance(node.value, ast.Constant):
                task_ids.add(node.value.value)
    assert task_ids == {"extract", "transform", "load"}, \
        f"Expected tasks extract/transform/load, found: {task_ids}"


def test_dag_task_order_defined():
    """The >> operator must be used to chain tasks."""
    source = DAG_FILE.read_text(encoding="utf-8")
    assert ">>" in source, "No task chaining (>>) found in DAG file"
    # Verify correct order appears in source
    extract_pos = source.index("extract_task >>")
    transform_pos = source.index("transform_task >>")
    assert extract_pos < transform_pos, "extract must chain before transform"
