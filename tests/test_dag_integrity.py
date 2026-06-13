"""
DAG integrity tests — catch broken DAGs before they reach Airflow.

These tests load the DAG file and verify structural properties without
actually running any tasks. This is the cheapest, highest-value CI check
you can add to an Airflow project.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from airflow.models import DagBag

DAG_FOLDER = str(Path(__file__).resolve().parent.parent / "dags")


@pytest.fixture(scope="session")
def dagbag() -> DagBag:
    return DagBag(dag_folder=DAG_FOLDER, include_examples=False)


def test_no_import_errors(dagbag):
    """Every .py file in dags/ must import without error."""
    assert dagbag.import_errors == {}, f"DAG import errors: {dagbag.import_errors}"


def test_etl_sales_dag_loaded(dagbag):
    """The etl_sales DAG must exist."""
    dag = dagbag.get_dag(dag_id="etl_sales")
    assert dag is not None, "DAG 'etl_sales' was not found"


def test_etl_sales_has_retries(dagbag):
    """Production DAGs must have at least 1 retry configured."""
    dag = dagbag.get_dag(dag_id="etl_sales")
    assert dag.default_args.get("retries", 0) >= 1


def test_etl_sales_has_owner(dagbag):
    """Every DAG must declare an owner — no anonymous pipelines."""
    dag = dagbag.get_dag(dag_id="etl_sales")
    assert dag.default_args.get("owner"), "DAG must have an owner"


def test_etl_sales_task_order(dagbag):
    """extract → transform → load must hold."""
    dag = dagbag.get_dag(dag_id="etl_sales")
    task_ids = {t.task_id for t in dag.tasks}
    assert task_ids == {"extract", "transform", "load"}

    extract = dag.get_task("extract")
    transform = dag.get_task("transform")
    load = dag.get_task("load")

    assert transform.task_id in [t.task_id for t in extract.downstream_list]
    assert load.task_id in [t.task_id for t in transform.downstream_list]
