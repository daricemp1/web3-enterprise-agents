#!/usr/bin/env python3
"""Generates this agent's synthetic BigQuery seed data (data/*.csv).

Run once; the output is committed as static CSVs, not regenerated at load time. See
docs/superpowers/specs/2026-07-25-assortment-planning-agent-design.md sections 3-5 for the
schema and data design this implements.

Usage:
    uv run python domains/merchandising/agents/assortment_planning/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
SALES_WINDOW_END = datetime.date(2026, 7, 24)
SALES_WINDOW_DAYS = 60
PLANOGRAM_DATE = datetime.date(2026, 7, 1)

STORES = ["STORE-101", "STORE-102"]

PRODUCTS = [
    {"product_id": "SKU-001", "product_name": "Down Parka", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "retail_price": 180.00, "baseline_units": 6},
    {"product_id": "SKU-002", "product_name": "Rain Jacket", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "retail_price": 90.00, "baseline_units": 8},
    {"product_id": "SKU-003", "product_name": "Fleece Vest", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "retail_price": 65.00, "baseline_units": 10},
    {"product_id": "SKU-004", "product_name": "Running Shoe", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "retail_price": 95.00, "baseline_units": 12},
    {"product_id": "SKU-005", "product_name": "Ankle Boot", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "retail_price": 110.00, "baseline_units": 7},
    {"product_id": "SKU-006", "product_name": "Sandal", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "retail_price": 35.00, "baseline_units": 9},
]

TREND_PRODUCT_ID = "SKU-001"  # Down Parka: mild upward daily trend, for `forecast` to project
ANOMALY_PRODUCT_ID = "SKU-004"  # Running Shoe: demand spike, for `detect_anomalies` to find
ANOMALY_STORE_ID = "STORE-101"
ANOMALY_DAY_OFFSET = 30  # mid-window


def write_product_catalog() -> None:
  with open(DATA_DIR / "product_catalog.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "product_id", "product_name", "category", "department", "brand",
        "launch_date", "status", "planned_assortment",
    ])
    for product in PRODUCTS:
      writer.writerow([
          product["product_id"], product["product_name"], product["category"],
          product["department"], product["brand"], "2024-01-15", "active", "true",
      ])


def write_planogram_space_allocation() -> None:
  with open(DATA_DIR / "planogram_space_allocation.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id", "product_id", "shelf_location", "facings",
        "space_allocated_sq_ft", "planogram_date",
    ])
    for store_id in STORES:
      for product_index, product in enumerate(PRODUCTS):
        aisle = 1 if product["department"] == "Apparel" else 2
        writer.writerow([
            store_id, product["product_id"], f"AISLE-{aisle}-BAY-{product_index + 1}",
            4 + (product_index % 3), round(6.0 + product_index * 1.5, 1),
            PLANOGRAM_DATE.isoformat(),
        ])


def write_sales_by_sku(rng: random.Random) -> None:
  start_date = SALES_WINDOW_END - datetime.timedelta(days=SALES_WINDOW_DAYS - 1)

  with open(DATA_DIR / "sales_by_sku.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "store_id", "product_id", "units_sold", "revenue"])

    for day_offset in range(SALES_WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      is_weekend = current_date.weekday() >= 5

      for store_id in STORES:
        for product in PRODUCTS:
          baseline = product["baseline_units"]
          units = baseline * 1.3 if is_weekend else baseline

          if product["product_id"] == TREND_PRODUCT_ID:
            trend_factor = 1.0 + (0.4 * day_offset / (SALES_WINDOW_DAYS - 1))
            units *= trend_factor

          units = max(1, round(units + rng.uniform(-1.5, 1.5)))

          if (
              product["product_id"] == ANOMALY_PRODUCT_ID
              and store_id == ANOMALY_STORE_ID
              and day_offset == ANOMALY_DAY_OFFSET
          ):
            units = baseline * 5

          price_variance = rng.uniform(0.97, 1.03)
          revenue = round(units * product["retail_price"] * price_variance, 2)

          writer.writerow([
              current_date.isoformat(), store_id, product["product_id"], units, revenue,
          ])


def main() -> None:
  rng = random.Random(42)
  write_product_catalog()
  write_planogram_space_allocation()
  write_sales_by_sku(rng)
  print(f"Wrote seed CSVs to {DATA_DIR}")


if __name__ == "__main__":
  main()
