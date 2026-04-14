from __future__ import annotations

import pandas as pd

from src.config import CLEAN_TRANSACTIONS_FILE, RAW_DATA_FILE, ensure_directories


EXPECTED_COLUMNS = [
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country",
]


def load_raw_excel(file_path=RAW_DATA_FILE) -> pd.DataFrame:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Raw dataset not found at {file_path}. "
            "Download Online Retail II and save it as data/raw/online_retail_II.xlsx"
        )

    sheets = pd.read_excel(file_path, sheet_name=None)
    frames = []
    for sheet_name, frame in sheets.items():
        missing_columns = [col for col in EXPECTED_COLUMNS if col not in frame.columns]
        if missing_columns:
            raise ValueError(
                f"Sheet '{sheet_name}' is missing required columns: {missing_columns}"
            )
        frame = frame[EXPECTED_COLUMNS].copy()
        frame["source_sheet"] = sheet_name
        frames.append(frame)

    data = pd.concat(frames, ignore_index=True)
    return data


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [
        "invoice",
        "stock_code",
        "description",
        "quantity",
        "invoice_date",
        "unit_price",
        "customer_id",
        "country",
        "source_sheet",
    ]

    cleaned["description"] = cleaned["description"].fillna("Unknown Product").astype(str).str.strip()
    cleaned["invoice"] = cleaned["invoice"].astype(str).str.strip()
    cleaned["stock_code"] = cleaned["stock_code"].astype(str).str.strip()
    cleaned["country"] = cleaned["country"].fillna("Unknown").astype(str).str.strip()
    cleaned["invoice_date"] = pd.to_datetime(cleaned["invoice_date"], errors="coerce")
    cleaned["customer_id"] = pd.to_numeric(cleaned["customer_id"], errors="coerce").astype("Int64")
    cleaned["quantity"] = pd.to_numeric(cleaned["quantity"], errors="coerce")
    cleaned["unit_price"] = pd.to_numeric(cleaned["unit_price"], errors="coerce")

    cleaned = cleaned.dropna(subset=["invoice_date", "quantity", "unit_price", "customer_id"])
    cleaned = cleaned[(cleaned["quantity"] > 0) & (cleaned["unit_price"] > 0)]
    cleaned = cleaned[~cleaned["invoice"].str.startswith("C", na=False)]

    cleaned["customer_id"] = cleaned["customer_id"].astype(str)
    cleaned["revenue"] = cleaned["quantity"] * cleaned["unit_price"]
    cleaned["order_month"] = cleaned["invoice_date"].dt.to_period("M").astype(str)
    cleaned["order_date"] = cleaned["invoice_date"].dt.date.astype(str)
    cleaned["year"] = cleaned["invoice_date"].dt.year
    cleaned["month"] = cleaned["invoice_date"].dt.month
    cleaned["day"] = cleaned["invoice_date"].dt.day
    cleaned["hour"] = cleaned["invoice_date"].dt.hour
    cleaned["weekday"] = cleaned["invoice_date"].dt.weekday
    cleaned["day_name"] = cleaned["invoice_date"].dt.day_name()
    cleaned["is_weekend"] = cleaned["weekday"].isin([5, 6]).astype(int)

    cleaned = cleaned.sort_values("invoice_date").reset_index(drop=True)
    return cleaned


def build_and_save_clean_dataset() -> pd.DataFrame:
    ensure_directories()
    raw_df = load_raw_excel()
    clean_df = clean_transactions(raw_df)
    clean_df.to_csv(CLEAN_TRANSACTIONS_FILE, index=False)
    return clean_df


if __name__ == "__main__":
    build_and_save_clean_dataset()
