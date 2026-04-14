# Ecommerce Analytics Portfolio Project

This project is designed to help a fresher get shortlisted for Data Analyst roles by showing an end-to-end ecommerce analytics workflow:

- ingest a large public dataset
- clean and model the data
- build business KPIs
- segment customers using RFM + clustering
- write interview-ready SQL
- present insights in a Streamlit dashboard

The project is intentionally structured like a real analytics case study rather than just a notebook.

## 1. Recommended Large Dataset

### Primary dataset for this project
- **Online Retail II - UCI Machine Learning Repository**
- Link: [https://archive-beta.ics.uci.edu/dataset/502/online+retail+ii](https://archive-beta.ics.uci.edu/dataset/502/online+retail+ii)
- Mirror page: [https://archive.ics.uci.edu/dataset/502/online+retail+ii](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- Size: **1,067,371 transactions**
- Period: **December 1, 2009 to December 9, 2011**
- Why this is excellent:
  - large enough to feel like real business data
  - ecommerce transactions, customers, invoices, countries, quantities, prices
  - perfect for sales analysis, retention, cohort, customer segmentation, and forecasting

### Optional alternative datasets
- **Olist Brazilian E-Commerce Public Dataset**
  - Link: [https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
  - Good for delivery analysis, payments, reviews, and seller performance
- **Instacart Market Basket Analysis**
  - Link: [https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data)
  - Good for basket analysis and product recommendation

## 2. Final Project Outcome

After running this project, you will have:

- cleaned transaction-level data
- business-ready summary tables
- customer RFM metrics
- customer segments generated with machine learning
- SQL analysis queries
- a dashboard for portfolio/demo use

That is enough to present as:

> "I built an end-to-end ecommerce analytics project on a 1M+ transaction dataset, covering cleaning, KPI reporting, customer segmentation, SQL analysis, and dashboarding."

## 3. Project Directory

```text
Ecommerce/
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   ├── processed/
│   │   └── .gitkeep
│   └── external/
│       └── .gitkeep
├── notebooks/
│   └── .gitkeep
├── reports/
│   └── .gitkeep
├── sql/
│   └── ecommerce_analysis.sql
└── src/
    ├── __init__.py
    ├── config.py
    ├── data/
    │   └── make_dataset.py
    ├── features/
    │   └── build_features.py
    ├── analysis/
    │   ├── generate_reports.py
    │   └── run_duckdb_queries.py
    ├── models/
    │   └── customer_segmentation.py
    ├── dashboard/
    │   └── app.py
    └── pipeline/
        └── run_pipeline.py
```

## 4. Business Questions This Project Answers

- What is total revenue, total orders, average order value, and monthly growth?
- Which countries generate the highest revenue?
- Which products and stock codes perform best?
- Who are the high-value customers?
- Which customers are at risk of churning?
- What customer segments exist based on recency, frequency, and monetary value?
- Which periods show strong seasonal demand?

## 5. Setup

## Prerequisites

- Python 3.10+

## Install dependencies

```bash
pip install -r requirements.txt
```

## Download dataset

1. Open the UCI dataset page:
   - [https://archive-beta.ics.uci.edu/dataset/502/online+retail+ii](https://archive-beta.ics.uci.edu/dataset/502/online+retail+ii)
2. Download the Excel file.
3. Save it in:

```text
data/raw/online_retail_II.xlsx
```

## Run full pipeline

```bash
python -m src.pipeline.run_pipeline
```

## Launch dashboard

```bash
streamlit run src/dashboard/app.py
```

## Run SQL analysis with DuckDB

```bash
python -m src.analysis.run_duckdb_queries
```

## 6. Output Files Created

After running the pipeline, these files will be generated in `data/processed/`:

- `transactions_clean.csv`
- `country_monthly_sales.csv`
- `product_sales_summary.csv`
- `customer_rfm.csv`
- `customer_segments.csv`
- `kpi_summary.csv`

Also generated in `reports/`:

- `business_summary.md`

## 7. Portfolio Story For Resume

You can write this on your resume:

**Ecommerce Analytics Project**
- Analyzed **1M+ ecommerce transactions** from a public retail dataset using Python, Pandas, SQL, and Streamlit
- Built a complete analytics pipeline for data cleaning, KPI tracking, country-wise sales analysis, and product performance
- Performed **RFM analysis** and **customer segmentation using KMeans**
- Created an interactive dashboard to visualize revenue trends, customer segments, and business insights

## 8. Interview Questions You Can Answer From This Project

- How did you clean cancelled orders and returns?
- How did you define revenue and order count?
- Why did you use RFM for segmentation?
- How did you decide the number of clusters?
- What were the top countries and products?
- Which metrics matter most in ecommerce analytics?

## 9. Suggested Next Upgrades

If you want to make this even stronger later, add:

- cohort retention analysis
- churn prediction model
- product recommendation / market basket analysis
- sales forecasting with Prophet or XGBoost
- Power BI dashboard version
- deployment on Streamlit Community Cloud

## 10. Step-By-Step Build Plan

1. Download the dataset and place it in `data/raw/`.
2. Run the pipeline to clean and transform the raw transactions.
3. Generate KPI tables and customer-level features.
4. Build customer segments using RFM and KMeans.
5. Explore interview-ready SQL queries in `sql/ecommerce_analysis.sql`.
6. Open the dashboard and take screenshots for LinkedIn, resume, and GitHub.
7. Push the project to GitHub with a strong README and results section.

This project is already structured to help you do that.
