#!/usr/bin/env python3
"""Generates synthetic seed CSV data for Store Operations: Loss Prevention & Shrinkage agent.

Generates 4 CSV files under domains/store_operations/agents/loss_prevention_shrinkage/data/:
1. stores.csv (store_id STORE-001..STORE-004, store_name, region, district_manager, risk_level [Low, Medium, High])
2. shrinkage_monthly.csv (store_id, fiscal_month 2026-06, total_sales_value, book_inventory_value, physical_inventory_value, shrink_dollars, shrink_pct, shrink_cause [Known Theft, Unknown Loss, Admin Error, Damage]; date anchor 2026-07-24)
3. category_shrink.csv (store_id, fiscal_month 2026-06, category [Apparel, Electronics, Beauty, Grocery], units_lost, shrink_cost_value, high_risk_flag)
4. audit_exceptions.csv (store_id, date 2026-07-24, exception_type [No Sale Cash Drawer Open, Manual Price Override, High Value Refund, Unscanned Item], event_count, flagged_employee_count, investigation_status [Open, Resolved, Escalated])

Anchors date windows around 2026-07-24.
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
WINDOW_END = datetime.date(2026, 7, 24)
WINDOW_DAYS = 14

STORES = [
    {
        "store_id": "STORE-001",
        "store_name": "Downtown Flagship",
        "region": "West",
        "district_manager": "Sarah Jenkins",
        "risk_level": "High",
    },
    {
        "store_id": "STORE-002",
        "store_name": "Suburban Plaza",
        "region": "West",
        "district_manager": "Sarah Jenkins",
        "risk_level": "Low",
    },
    {
        "store_id": "STORE-003",
        "store_name": "Metro Center",
        "region": "Midwest",
        "district_manager": "Michael Chang",
        "risk_level": "Medium",
    },
    {
        "store_id": "STORE-004",
        "store_name": "City Galleria",
        "region": "East",
        "district_manager": "David Ross",
        "risk_level": "High",
    },
]

FISCAL_MONTHS = ["2026-04", "2026-05", "2026-06"]
SHRINK_CAUSES = ["Known Theft", "Unknown Loss", "Admin Error", "Damage"]
CATEGORIES = ["Apparel", "Electronics", "Beauty", "Grocery"]
EXCEPTION_TYPES = [
    "No Sale Cash Drawer Open",
    "Manual Price Override",
    "High Value Refund",
    "Unscanned Item",
]
INVESTIGATION_STATUSES = ["Open", "Resolved", "Escalated"]


def write_stores() -> None:
  with open(DATA_DIR / "stores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "store_name",
        "region",
        "district_manager",
        "risk_level",
    ])
    for store in STORES:
      writer.writerow([
          store["store_id"],
          store["store_name"],
          store["region"],
          store["district_manager"],
          store["risk_level"],
      ])


def write_shrinkage_monthly(rng: random.Random) -> None:
  with open(DATA_DIR / "shrinkage_monthly.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "fiscal_month",
        "total_sales_value",
        "book_inventory_value",
        "physical_inventory_value",
        "shrink_dollars",
        "shrink_pct",
        "shrink_cause",
    ])
    for month in FISCAL_MONTHS:
      for store in STORES:
        store_id = store["store_id"]
        risk = store["risk_level"]

        # Base values by risk level
        if risk == "High":
          base_sales = 850000.0
          shrink_rate = 0.024
        elif risk == "Medium":
          base_sales = 650000.0
          shrink_rate = 0.016
        else:
          base_sales = 500000.0
          shrink_rate = 0.010

        for cause in SHRINK_CAUSES:
          # Distribute shrink by cause
          cause_mult = {
              "Known Theft": 0.40,
              "Unknown Loss": 0.30,
              "Admin Error": 0.15,
              "Damage": 0.15,
          }[cause]

          sales_val = round(base_sales * rng.uniform(0.95, 1.05), 2)
          cause_shrink_dollars = round(sales_val * shrink_rate * cause_mult, 2)
          book_inv = round(sales_val * 0.4 + cause_shrink_dollars, 2)
          phys_inv = round(book_inv - cause_shrink_dollars, 2)
          shrink_dollars = round(book_inv - phys_inv, 2)
          shrink_pct = round((shrink_dollars / sales_val) * 100.0, 2)

          writer.writerow([
              store_id,
              month,
              sales_val,
              book_inv,
              phys_inv,
              shrink_dollars,
              shrink_pct,
              cause,
          ])


def write_category_shrink(rng: random.Random) -> None:
  with open(DATA_DIR / "category_shrink.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "fiscal_month",
        "category",
        "units_lost",
        "shrink_cost_value",
        "high_risk_flag",
    ])
    for month in FISCAL_MONTHS:
      for store in STORES:
        store_id = store["store_id"]
        for cat in CATEGORIES:
          is_high_risk = cat in ["Electronics", "Beauty"]
          high_risk_flag = "TRUE" if is_high_risk else "FALSE"

          if is_high_risk:
            units = rng.randint(40, 150)
            cost_per_unit = rng.uniform(45.0, 120.0)
          else:
            units = rng.randint(20, 80)
            cost_per_unit = rng.uniform(12.0, 35.0)

          shrink_cost = round(units * cost_per_unit, 2)

          writer.writerow([
              store_id,
              month,
              cat,
              units,
              shrink_cost,
              high_risk_flag,
          ])


def write_audit_exceptions(rng: random.Random) -> None:
  start_date = WINDOW_END - datetime.timedelta(days=WINDOW_DAYS - 1)
  with open(DATA_DIR / "audit_exceptions.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "date",
        "exception_type",
        "event_count",
        "flagged_employee_count",
        "investigation_status",
    ])
    for day_offset in range(WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      for store in STORES:
        store_id = store["store_id"]
        for ex_type in EXCEPTION_TYPES:
          events = rng.randint(2, 18)
          flagged_emp = rng.randint(1, min(5, events))
          status = rng.choice(INVESTIGATION_STATUSES)

          writer.writerow([
              store_id,
              current_date.isoformat(),
              ex_type,
              events,
              flagged_emp,
              status,
          ])


def main() -> None:
  rng = random.Random(42)
  write_stores()
  write_shrinkage_monthly(rng)
  write_category_shrink(rng)
  write_audit_exceptions(rng)
  print(f"Generated 4 seed data CSVs in {DATA_DIR}")


if __name__ == "__main__":
  main()
