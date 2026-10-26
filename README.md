# German E-Commerce — Advanced SQL Analytics Case Study

A SQL portfolio project exploring commercial questions through analytical SQL, DuckDB and Python.

> The repository includes synthetic data for repeatable testing and a separate workflow for preparing a real public retail dataset. Findings from the synthetic dataset are illustrative and must not be presented as real market results.

## Existing synthetic dataset

The synthetic generator creates approximately 22,000 order records across 3,000 customers, 10 German cities and 7 categories from 2023 to mid-2025. It contains no personal data. Because the data-generating process shapes the patterns, use it for SQL development and testing—not as evidence about actual customer behaviour.

## Real-data analysis

The planned real-data source is [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail), a transaction-line dataset from a UK-based online retailer. The initial analysis scope is records where the source country is Germany. This is not a dataset from a German retailer, and monetary results remain in GBP.

### Prepare the workbook

1. Download the original Online Retail workbook from UCI.
2. Save it as `data/raw/Online Retail.xlsx` (or supply a different path).
3. Install dependencies and run the preparation script:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python prepare_real_data.py
```

The script writes `data/processed/real_retail_transactions.csv`. It preserves source rows and adds quality flags for cancellation invoices, negative/zero quantities, negative prices, missing values and duplicate candidates. It does not silently delete flagged records. Inspect the counts and flags before defining the final analysis filters.

See [real-data methodology](docs/real_data_methodology.md) for source scope, metric definitions, cleaning rules and limitations.

## Current SQL analyses

| File | Business question | SQL technique |
|------|----------|---------------|
| `queries/01_monthly_revenue_growth.sql` | How is revenue trending month over month? | `LAG()` |
| `queries/02_cohort_retention.sql` | Do customers return after their first month? | Cohort analysis |
| `queries/03_rfm_segmentation.sql` | Which customers have different recency, frequency and spend profiles? | `NTILE()`, `CASE` |
| `queries/04_category_running_total.sql` | How concentrated is revenue across categories? | Running totals, share of total |
| `queries/05_top_customers_per_city.sql` | Who are the top spenders in each city? | `RANK()` and `PARTITION BY` |

These queries currently target the synthetic `orders` table. The real-data preparation workflow is the first step; a validated staging view and explicit metric filters must be added before running equivalent business analyses on the real dataset.

## Metric and data limitations

- The existing synthetic schema has one row per order and uses generated values. Treat its findings as illustrative.
- The UCI source has transaction-line grain, so invoice counts should use distinct invoice numbers.
- Cancellation invoices and negative quantities may represent cancellations or returns. They need explicit handling; gross positive sales and net sales are not interchangeable.
- Customer analyses require identifiable customer IDs; report how excluding missing IDs affects coverage.
- The source is from a UK-based retailer, and monetary values are in GBP.
- Product costs and marketing spend are not available, so this project cannot claim profit, margin or campaign ROI.

## Roadmap

1. Validate the real dataset and document cleaning decisions.
2. Define revenue, invoice, average order value and retention metrics.
3. Adapt the existing SQL analyses to the cleaned real-data staging layer.
4. Add query tests, reproducible result tables and business recommendations.
5. Present evidence, assumptions and limitations in a concise stakeholder report.
