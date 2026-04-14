-- Interview-ready SQL queries for ecommerce analytics.
-- These queries expect a table named transactions_clean.

-- 1. Overall KPIs
SELECT
    COUNT(DISTINCT invoice) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(COUNT(DISTINCT invoice), 0), 2) AS avg_order_value
FROM transactions_clean;

-- 2. Monthly revenue trend
SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    ROUND(SUM(revenue), 2) AS monthly_revenue,
    COUNT(DISTINCT invoice) AS monthly_orders
FROM transactions_clean
GROUP BY 1
ORDER BY 1;

-- 3. Top countries by revenue
SELECT
    country,
    COUNT(DISTINCT invoice) AS orders,
    COUNT(DISTINCT customer_id) AS customers,
    ROUND(SUM(revenue), 2) AS revenue
FROM transactions_clean
GROUP BY 1
ORDER BY revenue DESC
LIMIT 10;

-- 4. Top products by revenue
SELECT
    stock_code,
    description,
    SUM(quantity) AS units_sold,
    ROUND(SUM(revenue), 2) AS revenue
FROM transactions_clean
GROUP BY 1, 2
ORDER BY revenue DESC
LIMIT 15;

-- 5. Customers with the highest lifetime value
SELECT
    customer_id,
    COUNT(DISTINCT invoice) AS orders,
    ROUND(SUM(revenue), 2) AS lifetime_value,
    MAX(invoice_date) AS last_purchase_date
FROM transactions_clean
GROUP BY 1
ORDER BY lifetime_value DESC
LIMIT 20;

-- 6. Average basket size by country
SELECT
    country,
    ROUND(AVG(order_quantity), 2) AS avg_items_per_order
FROM (
    SELECT
        country,
        invoice,
        SUM(quantity) AS order_quantity
    FROM transactions_clean
    GROUP BY 1, 2
) t
GROUP BY 1
ORDER BY avg_items_per_order DESC;

-- 7. Revenue share by weekday
SELECT
    day_name,
    ROUND(SUM(revenue), 2) AS revenue
FROM transactions_clean
GROUP BY 1
ORDER BY revenue DESC;

-- 8. Monthly active customers
SELECT
    DATE_TRUNC('month', invoice_date) AS month,
    COUNT(DISTINCT customer_id) AS active_customers
FROM transactions_clean
GROUP BY 1
ORDER BY 1;
