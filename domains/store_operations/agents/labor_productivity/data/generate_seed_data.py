#!/usr/bin/env python3
"""Generates synthetic seed CSV data for Store Operations: Labor Productivity agent.

Generates 4 CSV files under domains/store_operations/agents/labor_productivity/data/:
1. stores.csv (store_id, store_name, region, city, district_manager for STORE-001..STORE-004)
2. hourly_foot_traffic.csv (store_id, date, hour_of_day [8..21], customer_traffic_count, completed_transactions; date anchor 2026-07-24)
3. hourly_staff_shifts.csv (store_id, date, hour_of_day [8..21], department [Checkout, Sales Floor, Stockroom], scheduled_staff_count, actual_staff_count; date anchor 2026-07-24)
4. store_labor_budgets.csv (store_id, date, department, budgeted_hours, actual_regular_hours, overtime_hours, budgeted_labor_cost, actual_labor_cost; date anchor 2026-07-24)

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
        "city": "San Francisco",
        "district_manager": "Sarah Jenkins",
    },
    {
        "store_id": "STORE-002",
        "store_name": "Suburban Plaza",
        "region": "West",
        "city": "Seattle",
        "district_manager": "Sarah Jenkins",
    },
    {
        "store_id": "STORE-003",
        "store_name": "Metro Center",
        "region": "Midwest",
        "city": "Chicago",
        "district_manager": "Michael Chang",
    },
    {
        "store_id": "STORE-004",
        "store_name": "City Galleria",
        "region": "East",
        "city": "New York",
        "district_manager": "David Ross",
    },
]

DEPARTMENTS = ["Checkout", "Sales Floor", "Stockroom"]
HOURLY_RATES = {
    "Checkout": 18.00,
    "Sales Floor": 20.00,
    "Stockroom": 22.00,
}


def write_stores() -> None:
  with open(DATA_DIR / "stores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["store_id", "store_name", "region", "city", "district_manager"])
    for store in STORES:
      writer.writerow([
          store["store_id"],
          store["store_name"],
          store["region"],
          store["city"],
          store["district_manager"],
      ])


def write_hourly_foot_traffic(rng: random.Random) -> None:
  start_date = WINDOW_END - datetime.timedelta(days=WINDOW_DAYS - 1)
  with open(DATA_DIR / "hourly_foot_traffic.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id", "date", "hour_of_day", "customer_traffic_count", "completed_transactions"
    ])
    for day_offset in range(WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      is_weekend = current_date.weekday() >= 5
      day_mult = 1.3 if is_weekend else 1.0

      for store in STORES:
        store_id = store["store_id"]
        for hour in range(8, 22):
          if 12 <= hour <= 14 or 17 <= hour <= 19:
            base_traffic = 110
          elif 10 <= hour <= 11 or 15 <= hour <= 16:
            base_traffic = 70
          else:
            base_traffic = 35

          traffic = max(10, round(base_traffic * day_mult + rng.uniform(-15, 15)))
          conv_rate = rng.uniform(0.45, 0.65)
          transactions = min(traffic, max(5, round(traffic * conv_rate)))

          writer.writerow([
              store_id,
              current_date.isoformat(),
              hour,
              traffic,
              transactions,
          ])


def write_hourly_staff_shifts(rng: random.Random) -> None:
  start_date = WINDOW_END - datetime.timedelta(days=WINDOW_DAYS - 1)
  with open(DATA_DIR / "hourly_staff_shifts.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id", "date", "hour_of_day", "department", "scheduled_staff_count", "actual_staff_count"
    ])
    for day_offset in range(WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      is_weekend = current_date.weekday() >= 5

      for store in STORES:
        store_id = store["store_id"]
        for hour in range(8, 22):
          for dept in DEPARTMENTS:
            if dept == "Checkout":
              scheduled = 6 if (12 <= hour <= 14 or 17 <= hour <= 19) else 3
              if is_weekend:
                scheduled += 1
            elif dept == "Sales Floor":
              scheduled = 5 if (11 <= hour <= 18) else 3
              if is_weekend:
                scheduled += 1
            else:  # Stockroom
              scheduled = 4 if (8 <= hour <= 10) else 2

            variance = rng.choice([0, 0, 0, -1, 0, 1])
            actual = max(1, scheduled + variance)

            writer.writerow([
                store_id,
                current_date.isoformat(),
                hour,
                dept,
                scheduled,
                actual,
            ])


def write_store_labor_budgets(rng: random.Random) -> None:
  start_date = WINDOW_END - datetime.timedelta(days=WINDOW_DAYS - 1)
  with open(DATA_DIR / "store_labor_budgets.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id", "date", "department", "budgeted_hours", "actual_regular_hours",
        "overtime_hours", "budgeted_labor_cost", "actual_labor_cost"
    ])
    for day_offset in range(WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      is_weekend = current_date.weekday() >= 5

      for store in STORES:
        store_id = store["store_id"]
        for dept in DEPARTMENTS:
          rate = HOURLY_RATES[dept]
          if dept == "Checkout":
            base_budget = 56.0 if is_weekend else 48.0
          elif dept == "Sales Floor":
            base_budget = 50.0 if is_weekend else 42.0
          else:  # Stockroom
            base_budget = 28.0 if is_weekend else 24.0

          budgeted_hours = round(base_budget, 1)
          reg_variance = rng.uniform(-4.0, 2.0)
          actual_regular_hours = round(max(10.0, budgeted_hours + reg_variance), 1)

          ot_val = rng.uniform(-1.0, 4.0) if is_weekend else rng.uniform(-2.0, 2.0)
          overtime_hours = round(max(0.0, ot_val), 1)

          budgeted_labor_cost = round(budgeted_hours * rate, 2)
          actual_labor_cost = round((actual_regular_hours * rate) + (overtime_hours * rate * 1.5), 2)

          writer.writerow([
              store_id,
              current_date.isoformat(),
              dept,
              budgeted_hours,
              actual_regular_hours,
              overtime_hours,
              budgeted_labor_cost,
              actual_labor_cost,
          ])


def main() -> None:
  rng = random.Random(42)
  write_stores()
  write_hourly_foot_traffic(rng)
  write_hourly_staff_shifts(rng)
  write_store_labor_budgets(rng)
  print(f"Generated 4 seed data CSVs in {DATA_DIR}")


if __name__ == "__main__":
  main()
