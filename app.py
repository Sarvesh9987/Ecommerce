from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import plotly.express as px
import streamlit as st

from src.config import (
    COUNTRY_MONTHLY_FILE,
    CUSTOMER_SEGMENTS_FILE,
    KPI_SUMMARY_FILE,
    PRODUCT_SUMMARY_FILE,
)


st.set_page_config(
    page_title="Ecommerce Analytics Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)


@st.cache_data
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def currency(value: float) -> str:
    return f"${value:,.2f}"


def main() -> None:
    st.title("Ecommerce Analytics Dashboard")
    st.caption("Portfolio project for Data Analyst interviews")

    required_files = [
        KPI_SUMMARY_FILE,
        COUNTRY_MONTHLY_FILE,
        PRODUCT_SUMMARY_FILE,
        CUSTOMER_SEGMENTS_FILE,
    ]
    missing_files = [str(path) for path in required_files if not path.exists()]
    if missing_files:
        st.error(
            "Processed files are missing. Run `python -m src.pipeline.run_pipeline` first.\n\n"
            + "\n".join(missing_files)
        )
        st.stop()

    kpis = load_csv(KPI_SUMMARY_FILE)
    country_monthly = load_csv(COUNTRY_MONTHLY_FILE)
    products = load_csv(PRODUCT_SUMMARY_FILE)
    segments = load_csv(CUSTOMER_SEGMENTS_FILE)

    metric_map = dict(zip(kpis["metric"], kpis["value"]))
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", currency(metric_map["total_revenue"]))
    col2.metric("Orders", f"{int(metric_map['total_orders']):,}")
    col3.metric("Customers", f"{int(metric_map['total_customers']):,}")
    col4.metric("Avg Order Value", currency(metric_map["average_order_value"]))

    st.subheader("Monthly Revenue Trend")
    monthly_total = (
        country_monthly.groupby("order_month", as_index=False)["revenue"].sum().sort_values("order_month")
    )
    fig_monthly = px.line(
        monthly_total,
        x="order_month",
        y="revenue",
        markers=True,
        title="Revenue by Month",
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    left, right = st.columns(2)

    with left:
        st.subheader("Top Countries by Revenue")
        country_total = (
            country_monthly.groupby("country", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False).head(10)
        )
        fig_country = px.bar(
            country_total,
            x="revenue",
            y="country",
            orientation="h",
            title="Top 10 Countries",
        )
        fig_country.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig_country, use_container_width=True)

    with right:
        st.subheader("Customer Segments")
        segment_counts = (
            segments.groupby("segment", as_index=False)["customer_id"].count().rename(columns={"customer_id": "customers"})
        )
        fig_segments = px.pie(
            segment_counts,
            names="segment",
            values="customers",
            title="Customer Segment Distribution",
        )
        st.plotly_chart(fig_segments, use_container_width=True)

    st.subheader("Top Products")
    top_products = products.head(15).copy()
    fig_products = px.bar(
        top_products,
        x="revenue",
        y="description",
        orientation="h",
        title="Top 15 Products by Revenue",
    )
    fig_products.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_products, use_container_width=True)

    st.subheader("Segment Detail")
    view_columns = [
        "customer_id",
        "segment",
        "recency",
        "frequency",
        "monetary",
        "rfm_score",
        "country",
    ]
    st.dataframe(segments[view_columns].head(100), use_container_width=True)


if __name__ == "__main__":
    main()
