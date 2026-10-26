# Real-data methodology: UCI Online Retail

## Source and scope

Use the Online Retail dataset from the UCI Machine Learning Repository:
https://archive.ics.uci.edu/dataset/352/online+retail

The source describes transactions for a UK-based online retailer from 2010-12-01 to 2011-12-09. The dataset includes a country field, so this project initially examines records where Country = Germany. It must not be described as data from a German retailer.

Download the original Excel workbook and save it as data/raw/Online Retail.xlsx. Do not commit the workbook unless its license and repository-size implications have been reviewed. The preparation script writes a derived CSV under data/processed/; generated data files are intended to remain untracked.

## Grain and metric definitions

- **Source grain:** one transaction line as represented by the source workbook.
- **Signed line value:** Quantity * UnitPrice. This is a reconciliation field, not automatically recognized net revenue.
- **Gross positive sales-line value:** Quantity * UnitPrice for positive quantity and positive unit price, excluding cancellation invoices.
- **Invoice count:** distinct invoice numbers after the selected analysis filters.
- **Average order value (AOV):** sales value divided by distinct invoice count, only when the numerator and denominator use the same filters.
- **Customer retention:** a customer with an identifiable customer ID who has a qualifying purchase in a later period, divided by the defined original cohort size. Recent cohorts have incomplete observation windows and should not be compared directly with mature cohorts.

## Cleaning and quality policy

The preparation script intentionally flags rather than deletes rows. It preserves source rows and adds flags for:

- cancellation invoice numbers (invoice number begins with C);
- negative or zero quantities;
- negative unit prices;
- missing customer IDs, invoice dates, invoice numbers, stock codes, countries, quantities and prices;
- exact duplicate candidates.

A duplicate candidate is not proof of an erroneous duplicate. Investigate before removing records. Negative quantities may represent returns; cancellation invoices may require separate treatment. Do not treat all negative values as refunds without checking the source's business semantics.

For customer-level retention and RFM, records without customer IDs cannot be reliably attributed to customers and should be excluded from those specific analyses, while their impact should be reported.

## Known limitations

- The retailer is UK-based. German-country rows represent the retailer's transactions associated with Germany, not the German e-commerce market as a whole.
- Currency is GBP, so monetary results should remain labelled GBP.
- Product cost and marketing spend are not supplied; do not claim profit, margin, campaign ROI or causal impact.
- The source covers roughly one year, limiting long-term retention analysis.
- The dataset has no explicit order-line primary key. Duplicate candidates require investigation.
- Report the exact filters used for every metric, and distinguish gross sales from net sales after returns.

## Reproducibility

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
python prepare_real_data.py
```

If the workbook is elsewhere, pass --input PATH. Inspect the printed quality counts and the derived CSV before using it for business analysis.
