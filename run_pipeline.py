from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis.generate_reports import build_kpi_summary, write_business_summary
from src.data.make_dataset import build_and_save_clean_dataset
from src.features.build_features import (
    build_country_monthly_sales,
    build_customer_rfm,
    build_product_sales_summary,
)
from src.models.customer_segmentation import segment_customers


def main() -> None:
    transactions = build_and_save_clean_dataset()
    country_monthly = build_country_monthly_sales(transactions)
    product_summary = build_product_sales_summary(transactions)
    rfm = build_customer_rfm(transactions)
    customer_segments = segment_customers(rfm)
    kpis = build_kpi_summary(transactions)
    write_business_summary(transactions, kpis, customer_segments, product_summary)

    print("Pipeline completed successfully.")
    print(f"Clean transactions: {len(transactions):,} rows")
    print(f"Country-month rows: {len(country_monthly):,}")
    print(f"Product summary rows: {len(product_summary):,}")
    print(f"Customer RFM rows: {len(rfm):,}")
    print(f"Customer segment rows: {len(customer_segments):,}")


if __name__ == "__main__":
    main()
