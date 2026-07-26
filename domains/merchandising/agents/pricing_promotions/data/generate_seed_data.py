#!/usr/bin/env python3
"""Generates this agent's synthetic BigQuery seed data (data/*.csv).

Run once; the output is committed as static CSVs, not regenerated at load time. See
docs/superpowers/specs/2026-07-26-pricing-promotions-agent-design.md (local-only, gitignored,
not on a fresh clone) for the schema and data design this implements.

Usage:
    uv run python domains/merchandising/agents/pricing_promotions/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

# Same 6 products as the Assortment Planning agent's catalog (own physically separate table,
# not a cross-agent reference -- each agent's data is self-contained by design).
PRODUCTS = [
    {"product_id": "SKU-001", "product_name": "Down Parka", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "msrp": 180.00},
    {"product_id": "SKU-002", "product_name": "Rain Jacket", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "msrp": 90.00},
    {"product_id": "SKU-003", "product_name": "Fleece Vest", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "msrp": 65.00},
    {"product_id": "SKU-004", "product_name": "Running Shoe", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "msrp": 95.00},
    {"product_id": "SKU-005", "product_name": "Ankle Boot", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "msrp": 110.00},
    {"product_id": "SKU-006", "product_name": "Sandal", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "msrp": 35.00},
]

# price_history: one row per price-state change (not per day). Two engineered scenarios:
# SKU-003 gets one clean markdown with a jump in avg_daily_units_at_price (elasticity signal);
# SKU-006 gets three markdowns on a fixed cadence with deepening depth and rising units
# (markdown cadence/depth signal). All other products are flat controls.
PRICE_HISTORY = [
    {"product_id": "SKU-001", "effective_date": "2026-03-26", "list_price": 180.00,
     "sale_price": 180.00, "discount_reason": "regular", "avg_daily_units_at_price": 6.0},
    {"product_id": "SKU-002", "effective_date": "2026-03-26", "list_price": 90.00,
     "sale_price": 90.00, "discount_reason": "regular", "avg_daily_units_at_price": 8.0},
    {"product_id": "SKU-003", "effective_date": "2026-03-26", "list_price": 65.00,
     "sale_price": 65.00, "discount_reason": "regular", "avg_daily_units_at_price": 10.0},
    {"product_id": "SKU-003", "effective_date": "2026-06-01", "list_price": 65.00,
     "sale_price": 50.00, "discount_reason": "markdown", "avg_daily_units_at_price": 16.0},
    {"product_id": "SKU-004", "effective_date": "2026-03-26", "list_price": 95.00,
     "sale_price": 95.00, "discount_reason": "regular", "avg_daily_units_at_price": 12.0},
    {"product_id": "SKU-005", "effective_date": "2026-03-26", "list_price": 110.00,
     "sale_price": 110.00, "discount_reason": "regular", "avg_daily_units_at_price": 7.0},
    {"product_id": "SKU-006", "effective_date": "2026-03-26", "list_price": 35.00,
     "sale_price": 35.00, "discount_reason": "regular", "avg_daily_units_at_price": 9.0},
    {"product_id": "SKU-006", "effective_date": "2026-05-15", "list_price": 35.00,
     "sale_price": 28.00, "discount_reason": "markdown", "avg_daily_units_at_price": 13.0},
    {"product_id": "SKU-006", "effective_date": "2026-06-05", "list_price": 35.00,
     "sale_price": 21.00, "discount_reason": "markdown", "avg_daily_units_at_price": 18.0},
    {"product_id": "SKU-006", "effective_date": "2026-06-26", "list_price": 35.00,
     "sale_price": 14.00, "discount_reason": "clearance", "avg_daily_units_at_price": 25.0},
]

PROMO_CALENDAR = [
    {"promo_id": "PROMO-001", "promo_name": "Rainy Season Kickoff", "start_date": "2026-06-01",
     "end_date": "2026-06-14", "discount_pct": 25.0, "scope_type": "product",
     "scope_value": "SKU-002", "promo_type": "percent_off"},
    {"promo_id": "PROMO-002", "promo_name": "Boot Clearance Push", "start_date": "2026-06-15",
     "end_date": "2026-06-28", "discount_pct": 15.0, "scope_type": "product",
     "scope_value": "SKU-005", "promo_type": "percent_off"},
    {"promo_id": "PROMO-003", "promo_name": "Footwear Category Days", "start_date": "2026-07-01",
     "end_date": "2026-07-10", "discount_pct": 20.0, "scope_type": "category",
     "scope_value": "Women's Footwear", "promo_type": "percent_off"},
    {"promo_id": "PROMO-004", "promo_name": "Outerwear Flash Sale", "start_date": "2026-07-11",
     "end_date": "2026-07-17", "discount_pct": 20.0, "scope_type": "product",
     "scope_value": "SKU-001", "promo_type": "percent_off"},
]

# promo_sales_lift: one row per (promo, product). Engineered so Rainy Season Kickoff shows a
# strong, unambiguous lift and Boot Clearance Push shows a weak/negative lift -- both give a
# clean, verifiable answer to "did this promo work" questions.
PROMO_SALES_LIFT = [
    {"promo_id": "PROMO-001", "product_id": "SKU-002", "baseline_daily_units": 8.0,
     "baseline_window_start": "2026-05-18", "baseline_window_end": "2026-05-31",
     "promo_period_daily_units": 22.0, "promo_window_days": 14, "sale_price": 67.50},
    {"promo_id": "PROMO-002", "product_id": "SKU-005", "baseline_daily_units": 7.0,
     "baseline_window_start": "2026-06-01", "baseline_window_end": "2026-06-14",
     "promo_period_daily_units": 6.5, "promo_window_days": 14, "sale_price": 93.50},
    {"promo_id": "PROMO-003", "product_id": "SKU-004", "baseline_daily_units": 12.0,
     "baseline_window_start": "2026-06-17", "baseline_window_end": "2026-06-30",
     "promo_period_daily_units": 15.5, "promo_window_days": 10, "sale_price": 76.00},
    {"promo_id": "PROMO-003", "product_id": "SKU-005", "baseline_daily_units": 7.0,
     "baseline_window_start": "2026-06-17", "baseline_window_end": "2026-06-30",
     "promo_period_daily_units": 8.5, "promo_window_days": 10, "sale_price": 88.00},
    {"promo_id": "PROMO-003", "product_id": "SKU-006", "baseline_daily_units": 25.0,
     "baseline_window_start": "2026-06-17", "baseline_window_end": "2026-06-30",
     "promo_period_daily_units": 30.0, "promo_window_days": 10, "sale_price": 11.20},
    {"promo_id": "PROMO-004", "product_id": "SKU-001", "baseline_daily_units": 6.0,
     "baseline_window_start": "2026-06-27", "baseline_window_end": "2026-07-10",
     "promo_period_daily_units": 9.0, "promo_window_days": 7, "sale_price": 144.00},
]


def write_product_catalog() -> None:
  with open(DATA_DIR / "product_catalog.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "product_id", "product_name", "category", "department", "brand",
        "launch_date", "status", "msrp",
    ])
    for product in PRODUCTS:
      writer.writerow([
          product["product_id"], product["product_name"], product["category"],
          product["department"], product["brand"], "2024-01-15", "active", product["msrp"],
      ])


def write_price_history() -> None:
  with open(DATA_DIR / "price_history.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "product_id", "effective_date", "list_price", "sale_price", "discount_reason",
        "avg_daily_units_at_price",
    ])
    for row in PRICE_HISTORY:
      writer.writerow([
          row["product_id"], row["effective_date"], row["list_price"], row["sale_price"],
          row["discount_reason"], row["avg_daily_units_at_price"],
      ])


def write_promo_calendar() -> None:
  with open(DATA_DIR / "promo_calendar.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "promo_id", "promo_name", "start_date", "end_date", "discount_pct", "scope_type",
        "scope_value", "promo_type",
    ])
    for promo in PROMO_CALENDAR:
      writer.writerow([
          promo["promo_id"], promo["promo_name"], promo["start_date"], promo["end_date"],
          promo["discount_pct"], promo["scope_type"], promo["scope_value"], promo["promo_type"],
      ])


def write_promo_sales_lift(rng: random.Random) -> None:
  with open(DATA_DIR / "promo_sales_lift.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "promo_id", "product_id", "baseline_daily_units", "baseline_window_start",
        "baseline_window_end", "promo_period_daily_units", "lift_pct", "incremental_units",
        "incremental_revenue", "promo_window_days",
    ])
    for row in PROMO_SALES_LIFT:
      baseline = row["baseline_daily_units"]
      promo_units = row["promo_period_daily_units"]
      lift_pct = round((promo_units - baseline) / baseline * 100, 1)
      incremental_units = round((promo_units - baseline) * row["promo_window_days"])
      jitter = rng.uniform(0.98, 1.02)
      incremental_revenue = round(incremental_units * row["sale_price"] * jitter, 2)

      writer.writerow([
          row["promo_id"], row["product_id"], baseline, row["baseline_window_start"],
          row["baseline_window_end"], promo_units, lift_pct, incremental_units,
          incremental_revenue, row["promo_window_days"],
      ])


def main() -> None:
  rng = random.Random(42)
  write_product_catalog()
  write_price_history()
  write_promo_calendar()
  write_promo_sales_lift(rng)
  print(f"Wrote seed CSVs to {DATA_DIR}")


if __name__ == "__main__":
  main()
