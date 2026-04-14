from __future__ import annotations

import pandas as pd

from src.config import BUSINESS_REPORT_FILE, KPI_SUMMARY_FILE


def build_kpi_summary(df: pd.DataFrame) -> pd.DataFrame:
    total_revenue = round(df["revenue"].sum(), 2)
    total_orders = int(df["invoice"].nunique())
    total_customers = int(df["customer_id"].nunique())
    average_order_value = round(total_revenue / total_orders, 2) if total_orders else 0.0
    average_items_per_order = round(df["quantity"].sum() / total_orders, 2) if total_orders else 0.0

    kpis = pd.DataFrame(
        [
            {"metric": "total_revenue", "value": total_revenue},
            {"metric": "total_orders", "value": total_orders},
            {"metric": "total_customers", "value": total_customers},
            {"metric": "average_order_value", "value": average_order_value},
            {"metric": "average_items_per_order", "value": average_items_per_order},
        ]
    )
    kpis.to_csv(KPI_SUMMARY_FILE, index=False)
    return kpis


def write_business_summary(
    df: pd.DataFrame,
    kpis: pd.DataFrame,
    customer_segments: pd.DataFrame,
    product_summary: pd.DataFrame,
) -> None:
    top_country = (
        df.groupby("country", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False).head(1)
    )
    top_product = product_summary.head(1)
    top_segment = (
        customer_segments.groupby("segment", as_index=False)["customer_id"]
        .count()
        .sort_values("customer_id", ascending=False)
        .head(1)
    )

    metric_lookup = dict(zip(kpis["metric"], kpis["value"]))

    report = f"""# Business Summary

## Core KPIs
- Total Revenue: {metric_lookup['total_revenue']:,.2f}
- Total Orders: {int(metric_lookup['total_orders']):,}
- Total Customers: {int(metric_lookup['total_customers']):,}
- Average Order Value: {metric_lookup['average_order_value']:,.2f}
- Average Items Per Order: {metric_lookup['average_items_per_order']:,.2f}

## Key Insights
- Top revenue country: {top_country.iloc[0]['country']} ({top_country.iloc[0]['revenue']:,.2f})
- Top product by revenue: {top_product.iloc[0]['description']} ({top_product.iloc[0]['revenue']:,.2f})
- Largest customer segment: {top_segment.iloc[0]['segment']} ({int(top_segment.iloc[0]['customer_id'])} customers)

## Analyst Talking Points
- Revenue trend can be tracked monthly using the processed files and dashboard.
- Customer segmentation uses recency, frequency, and monetary value.
- Product analysis identifies best-selling and high-revenue stock codes.
- Country analysis highlights geographic revenue concentration.
"""

    BUSINESS_REPORT_FILE.write_text(report, encoding="utf-8")
