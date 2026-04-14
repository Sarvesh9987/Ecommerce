from __future__ import annotations

import pandas as pd

from src.config import (
    COUNTRY_MONTHLY_FILE,
    CUSTOMER_RFM_FILE,
    PRODUCT_SUMMARY_FILE,
)


def build_country_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["order_month", "country"], as_index=False)
        .agg(
            revenue=("revenue", "sum"),
            orders=("invoice", "nunique"),
            customers=("customer_id", "nunique"),
            quantity=("quantity", "sum"),
        )
        .sort_values(["order_month", "revenue"], ascending=[True, False])
    )
    summary.to_csv(COUNTRY_MONTHLY_FILE, index=False)
    return summary


def build_product_sales_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby(["stock_code", "description"], as_index=False)
        .agg(
            units_sold=("quantity", "sum"),
            orders=("invoice", "nunique"),
            revenue=("revenue", "sum"),
            customers=("customer_id", "nunique"),
        )
        .sort_values("revenue", ascending=False)
    )
    summary.to_csv(PRODUCT_SUMMARY_FILE, index=False)
    return summary


def build_customer_rfm(df: pd.DataFrame) -> pd.DataFrame:
    snapshot_date = df["invoice_date"].max() + pd.Timedelta(days=1)
    order_level = (
        df.groupby(["customer_id", "invoice"], as_index=False)
        .agg(order_revenue=("revenue", "sum"))
    )
    customer_avg_order = (
        order_level.groupby("customer_id", as_index=False)
        .agg(avg_order_value=("order_revenue", "mean"))
    )
    rfm = (
        df.groupby("customer_id", as_index=False)
        .agg(
            first_purchase_date=("invoice_date", "min"),
            last_purchase_date=("invoice_date", "max"),
            frequency=("invoice", "nunique"),
            monetary=("revenue", "sum"),
            total_items=("quantity", "sum"),
            country=("country", lambda s: s.mode().iat[0] if not s.mode().empty else "Unknown"),
        )
    )
    rfm = rfm.merge(customer_avg_order, on="customer_id", how="left")
    rfm["recency"] = (snapshot_date - rfm["last_purchase_date"]).dt.days
    rfm["customer_tenure_days"] = (snapshot_date - rfm["first_purchase_date"]).dt.days

    columns = [
        "customer_id",
        "country",
        "first_purchase_date",
        "last_purchase_date",
        "recency",
        "frequency",
        "monetary",
        "total_items",
        "avg_order_value",
        "customer_tenure_days",
    ]
    rfm = rfm[columns].sort_values("monetary", ascending=False)
    rfm.to_csv(CUSTOMER_RFM_FILE, index=False)
    return rfm
