from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = ROOT_DIR / "reports"
SQL_DIR = ROOT_DIR / "sql"

RAW_DATA_FILE = RAW_DIR / "online_retail_II.xlsx"
CLEAN_TRANSACTIONS_FILE = PROCESSED_DIR / "transactions_clean.csv"
COUNTRY_MONTHLY_FILE = PROCESSED_DIR / "country_monthly_sales.csv"
PRODUCT_SUMMARY_FILE = PROCESSED_DIR / "product_sales_summary.csv"
CUSTOMER_RFM_FILE = PROCESSED_DIR / "customer_rfm.csv"
CUSTOMER_SEGMENTS_FILE = PROCESSED_DIR / "customer_segments.csv"
KPI_SUMMARY_FILE = PROCESSED_DIR / "kpi_summary.csv"
BUSINESS_REPORT_FILE = REPORTS_DIR / "business_summary.md"


def ensure_directories() -> None:
    for directory in [RAW_DIR, PROCESSED_DIR, REPORTS_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
