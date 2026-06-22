# -*- coding: utf-8 -*-
"""Load orders.csv into DuckDB and run every query in queries/, printing results."""
import glob
import os
import duckdb

con = duckdb.connect(":memory:")
con.execute("""
    create table orders as
    select * from read_csv_auto('data/orders.csv', header=true)
""")
n = con.sql("select count(*) from orders").fetchone()[0]
print(f"Loaded {n} orders into DuckDB\n")

for path in sorted(glob.glob("queries/*.sql")):
    name = os.path.basename(path)
    sql = open(path, encoding="utf-8").read()
    # first comment line as title
    title = next((l[3:] for l in sql.splitlines() if l.startswith("-- ")), name)
    print("=" * 78)
    print(f"{name}  |  {title}")
    print("=" * 78)
    rel = con.sql(sql)
    cols = rel.columns
    rows = rel.fetchall()
    print(" | ".join(cols))
    for r in rows[:12]:
        print(" | ".join(str(x) for x in r))
    if len(rows) > 12:
        print(f"... ({len(rows)} rows total)")
    print()
