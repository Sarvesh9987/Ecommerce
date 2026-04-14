from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import duckdb

from src.config import CLEAN_TRANSACTIONS_FILE, SQL_DIR


def main() -> None:
    if not CLEAN_TRANSACTIONS_FILE.exists():
        raise FileNotFoundError(
            "Clean dataset not found. Run `python -m src.pipeline.run_pipeline` first."
        )

    query = (SQL_DIR / "ecommerce_analysis.sql").read_text(encoding="utf-8")
    conn = duckdb.connect()
    conn.execute(
        f"""
        CREATE OR REPLACE VIEW transactions_clean AS
        SELECT *
        FROM read_csv_auto('{CLEAN_TRANSACTIONS_FILE.as_posix()}', HEADER=TRUE);
        """
    )

    statements = [statement.strip() for statement in query.split(";") if statement.strip()]
    for index, statement in enumerate(statements, start=1):
        print(f"\n--- Query {index} ---")
        result = conn.execute(statement).fetchdf()
        print(result.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
