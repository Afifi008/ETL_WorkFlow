# CI/CD for Data Platforms — Lab Repo

Hands-on companion to **Session 05: CI/CD for Data Platforms with GitHub Actions**.

You'll build a GitHub Actions workflow that:
- Runs **DAG integrity tests** so broken DAGs never reach Airflow.
- Runs **unit tests** on the transformation logic.
- Runs **data quality tests** on the sample data.

---

## What's in here akdskla

```
cicd-airflow-lab/
├── dags/
│   ├── etl_sales_dag.py        # Airflow DAG: extract → transform → load
│   └── transformations.py      # Pure functions (easy to unit-test)
├── data/
│   └── raw_sales.csv           # Sample input data
├── tests/
│   ├── conftest.py             # Shared pytest fixtures
│   ├── test_dag_integrity.py   # DAG structure tests
│   ├── test_transformations.py # Unit tests
│   └── test_data_quality.py    # Data assertions
├── solution/
│   └── ci.yml                  # Finished workflow (peek after the lab)
├── requirements.txt
├── .gitignore
└── README.md
```

> **Note:** `.github/workflows/` is intentionally empty. You'll create
> `ci.yml` together during the session.

---

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the tests:

```bash
pytest tests/ -v
```

You should see **all green** before pushing.

---

## Lab steps (during the session)

1. **Fork** this repo to your own GitHub account.
2. **Clone** your fork locally.
3. Create `.github/workflows/ci.yml` — we'll write it together.
4. **Commit & push** to a feature branch.
5. **Open a pull request** to `main` — watch CI run.
6. **Break a test** on purpose (e.g. change `>= 0` to `> 0` in
   `dags/transformations.py`). Push again. See CI fail. Fix it.
7. **Merge** when green.

---

## After the lab

Compare your `ci.yml` to [`solution/ci.yml`](./solution/ci.yml).

---

## Branch protection (instructor demo)

In **Settings → Branches**, add a rule for `main`:
- ✅ Require a pull request before merging
- ✅ Require status checks to pass before merging → select your CI job
- ✅ Require branches to be up to date

Now `main` cannot receive a commit that fails CI.
