# German E-Commerce — Advanced SQL Analytics Case Study

A focused SQL portfolio project answering real commercial questions on a German
online-retail dataset using **analytical SQL** — window functions, cohort analysis,
and RFM segmentation — executed on **DuckDB**.

> **Why this project:** dashboards are easy to fake; *SQL depth* is not. This repo
> demonstrates the query patterns analysts are actually tested on in interviews:
> period-over-period growth, retention cohorts, customer segmentation, running totals,
> and partitioned ranking — each documented with the technique it showcases.

## Dataset
22,000 synthetic orders across 3,000 customers, 10 German cities and 7 categories
(2023 → mid-2025). Fully synthetic, no PII. The schema mirrors a typical DACH order
export, so the same queries run unchanged on a real export (e.g. a Kaggle online-retail
set filtered to Germany).

| Column | Example |
|--------|---------|
| order_id, customer_id | 1000, 1742 |
| order_date | 2024-03-11 |
| city | München, Berlin, Hamburg … |
| category | Elektronik, Garten, Sport … |
| channel | web / mobile_app / marketplace |
| quantity, amount_eur | 2, 219.90 |

## Quickstart
```bash
python -m venv .venv && source .venv/Scripts/activate
pip install duckdb
python generate_data.py     # writes data/orders.csv
python run_analysis.py      # runs every query in queries/ and prints results
```

## The five analyses

| File | Question | SQL technique |
|------|----------|---------------|
| `01_monthly_revenue_growth.sql` | How is revenue trending month-over-month? | `LAG()` for period comparison |
| `02_cohort_retention.sql` | Do customers come back after their first month? | First-touch cohorting + retention matrix |
| `03_rfm_segmentation.sql` | Who are our Champions vs At-Risk customers? | `NTILE(4)` scoring + segment `CASE` logic |
| `04_category_running_total.sql` | Which categories drive revenue (Pareto)? | `SUM() OVER` running total + ratio-to-report |
| `05_top_customers_per_city.sql` | Who are the top 3 spenders in each city? | `RANK() … PARTITION BY` |

## Sample findings
- **Strong growth ramp:** monthly revenue climbs from ~€2k (Jan-23) to ~€50k+ by end-2023.
- **Retention is front-loaded:** cohorts drop sharply after month 0 (~22–36% by month 1) —
  the classic "leaky bucket" that flags a re-engagement opportunity.
- **Champions are ~21% of customers** but carry the highest lifetime value (~€1,500 avg).
- **Pareto holds:** *Elektronik* alone is 36% of revenue; the top 3 categories are ~70%.

## What makes it mine
The dataset, the five business questions, the RFM segment thresholds, and this
documentation are my own design choices — the SQL patterns are standard, the analysis
and interpretation are mine. Every query carries an inline comment explaining the
technique so the logic is fully traceable.
