# -*- coding: utf-8 -*-
"""
Generate a realistic synthetic German e-commerce orders dataset for SQL analysis.
Schema mirrors a typical DACH online-retail order export. Fully synthetic (no PII);
swap in a real export (e.g. a Kaggle online-retail set filtered to DE) to scale up.
"""
import csv
import random
from datetime import date, timedelta

random.seed(7)
CITIES = ["München", "Berlin", "Hamburg", "Köln", "Frankfurt", "Stuttgart",
          "Düsseldorf", "Leipzig", "Dortmund", "Nürnberg"]
CATEGORIES = ["Elektronik", "Haushalt", "Mode", "Sport", "Spielzeug", "Bücher", "Garten"]
CHANNELS = ["web", "mobile_app", "marketplace"]

N_CUSTOMERS = 3000
N_ORDERS = 22000
START = date(2023, 1, 1)
DAYS = 900  # ~ to mid-2025

# Give customers a signup date and a "loyalty" that drives repeat probability
customers = {}
for cid in range(1, N_CUSTOMERS + 1):
    signup = START + timedelta(days=random.randint(0, DAYS - 30))
    customers[cid] = {
        "city": random.choice(CITIES),
        "signup": signup,
        "loyalty": random.random(),  # 0..1
    }

rows = []
oid = 1000
for _ in range(N_ORDERS):
    cid = random.randint(1, N_CUSTOMERS)
    c = customers[cid]
    # order date after signup, repeat customers cluster orders
    max_offset = (START + timedelta(days=DAYS) - c["signup"]).days
    if max_offset <= 1:
        continue
    offset = int(random.random() ** (1.5 - c["loyalty"]) * max_offset)
    odate = c["signup"] + timedelta(days=offset)
    cat = random.choice(CATEGORIES)
    base = {"Elektronik": 220, "Haushalt": 70, "Mode": 55, "Sport": 90,
            "Spielzeug": 35, "Bücher": 22, "Garten": 110}[cat]
    amount = round(max(5, random.gauss(base, base * 0.45)), 2)
    qty = random.choices([1, 2, 3, 4], weights=[0.6, 0.25, 0.1, 0.05])[0]
    rows.append([
        oid, cid, odate.isoformat(), c["city"], cat,
        random.choice(CHANNELS), qty, amount,
    ])
    oid += 1

rows.sort(key=lambda r: r[2])
with open("data/orders.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["order_id", "customer_id", "order_date", "city",
                "category", "channel", "quantity", "amount_eur"])
    w.writerows(rows)
print(f"Wrote data/orders.csv ({len(rows)} orders, {N_CUSTOMERS} customers)")
