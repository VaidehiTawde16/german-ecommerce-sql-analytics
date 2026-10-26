#!/usr/bin/env python3
"""Prepare the UCI Online Retail workbook for reproducible SQL analysis.

Download the original Online Retail.xlsx file from the UCI Machine Learning
Repository and place it at data/raw/Online Retail.xlsx. This script preserves
source rows and adds flags; it does not silently discard cancellations,
returns, missing customer IDs, or duplicate-looking lines.

Requirements:
    pip install pandas openpyxl

Output:
    data/processed/real_retail_transactions.csv
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parent
DEFAULT_INPUT = ROOT / "data" / "raw" / "Online Retail.xlsx"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "real_retail_transactions.csv"

COLUMN_MAP = {
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "UnitPrice": "unit_price_gbp",
    "CustomerID": "customer_id",
    "Country": "country",
}
REQUIRED_COLUMNS = set(COLUMN_MAP)


def prepare(input_path: Path, output_path: Path) -> pd.DataFrame:
    if not input_path.exists():
        raise FileNotFoundError(
            f"Source workbook not found: {input_path}\n"
            "Download the UCI Online Retail workbook and save it at this path, "
            "or pass --input PATH."
        )

    raw = pd.read_excel(input_path, engine="openpyxl")
    missing = REQUIRED_COLUMNS - set(raw.columns)
    if missing:
        raise ValueError(
            "Unexpected source schema. Missing required columns: "
            + ", ".join(sorted(missing))
        )

    df = raw.rename(columns=COLUMN_MAP).copy()
    df["source_row_number"] = range(2, len(df) + 2)
    df["invoice_no"] = df["invoice_no"].astype("string").str.strip()
    df["stock_code"] = df["stock_code"].astype("string").str.strip()
    df["description"] = df["description"].astype("string").str.strip()
    df["country"] = df["country"].astype("string").str.strip()
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price_gbp"] = pd.to_numeric(df["unit_price_gbp"], errors="coerce")
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")

    # Preserve original rows and add transparent quality/business flags.
    df["is_cancellation_invoice"] = (
        df["invoice_no"].str.upper().str.startswith("C", na=False)
    )
    df["is_negative_quantity"] = df["quantity"].lt(0).fillna(False)
    df["is_zero_quantity"] = df["quantity"].eq(0).fillna(False)
    df["is_negative_unit_price"] = df["unit_price_gbp"].lt(0).fillna(False)
    df["has_missing_customer_id"] = df["customer_id"].isna()
    df["has_missing_invoice_date"] = df["invoice_date"].isna()
    df["has_missing_invoice_no"] = df["invoice_no"].isna() | df["invoice_no"].eq("")
    df["has_missing_stock_code"] = df["stock_code"].isna() | df["stock_code"].eq("")
    df["has_missing_country"] = df["country"].isna() | df["country"].eq("")
    df["has_invalid_quantity"] = df["quantity"].isna()
    df["has_invalid_unit_price"] = df["unit_price_gbp"].isna()

    # A duplicate candidate is flagged, not removed: repeated-looking invoice
    # lines can require source-specific investigation before deduplication.
    duplicate_key = [
        "invoice_no", "stock_code", "description", "quantity",
        "invoice_date", "unit_price_gbp", "customer_id", "country",
    ]
    df["is_exact_duplicate_candidate"] = df.duplicated(
        subset=duplicate_key, keep="first"
    )

    # Signed line value is useful for reconciliation, not automatically a
    # measure of recognized net revenue or refunded cash.
    df["signed_line_value_gbp"] = df["quantity"] * df["unit_price_gbp"]

    # Convenience flags for later analyses. The full data remains available.
    df["is_positive_sales_line"] = (
        ~df["is_cancellation_invoice"]
        & df["quantity"].gt(0)
        & df["unit_price_gbp"].gt(0)
        & df["invoice_date"].notna()
        & df["invoice_no"].notna()
        & df["invoice_no"].ne("")
    )
    df["is_germany"] = df["country"].str.casefold().eq("germany").fillna(False)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, date_format="%Y-%m-%d %H:%M:%S")

    print(f"Input rows: {len(df):,}")
    print(f"Output: {output_path}")
    print(f"Germany rows: {int(df['is_germany'].sum()):,}")
    print(f"Cancellation invoice rows: {int(df['is_cancellation_invoice'].sum()):,}")
    print(f"Negative-quantity rows: {int(df['is_negative_quantity'].sum()):,}")
    print(f"Missing customer IDs: {int(df['has_missing_customer_id'].sum()):,}")
    print(f"Exact duplicate candidates (flagged, not removed): "
          f"{int(df['is_exact_duplicate_candidate'].sum()):,}")
    print("No source rows were dropped. Review the flags before defining analysis filters.")
    return df


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        prepare(args.input, args.output)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
