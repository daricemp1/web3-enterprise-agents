#!/usr/bin/env python3
"""Generates synthetic seed CSV data for Finance: Gross Margin & Profitability agent.

Generates 4 CSV files under domains/finance/agents/gross_margin_profitability/data/:
1. stores.csv (store_id, store_name, region, city for STORE-001..STORE-004)
2. product_cost_master.csv (product_id, product_name, category, unit_cogs, unit_retail_price for SKU-001..SKU-006)
3. sales_profitability.csv (store_id, product_id, date, units_sold, gross_revenue, cogs_amount, markdown_discount_amount, net_revenue, gross_margin_amount, gross_margin_pct; date anchor 2026-07-24)
4. category_margin_targets.csv (category, fiscal_quarter, target_gross_margin_pct, target_revenue for Apparel, Electronics, Home; fiscal_quarter 2026-Q3)

Usage:
    uv run python domains/finance/agents/gross_margin_profitability/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
SALES_WINDOW_END = datetime.date(2026, 7, 24)
SALES_WINDOW_DAYS = 30

STORES = [
    {
        "store_id": "STORE-001",
        "store_name": "Downtown Flagship",
        "region": "West",
        "city": "San Francisco",
    },
    {
        "store_id": "STORE-002",
        "store_name": "Suburban Plaza",
        "region": "West",
        "city": "Seattle",
    },
    {
        "store_id": "STORE-003",
        "store_name": "Metro Center",
        "region": "Midwest",
        "city": "Chicago",
    },
    {
        "store_id": "STORE-004",
        "store_name": "City Galleria",
        "region": "East",
        "city": "New York",
    },
]

PRODUCTS = [
    {
        "product_id": "SKU-001",
        "product_name": "Down Parka",
        "category": "Apparel",
        "unit_cogs": 90.00,
        "unit_retail_price": 180.00,
        "baseline_units": 10,
    },
    {
        "product_id": "SKU-002",
        "product_name": "Rain Jacket",
        "category": "Apparel",
        "unit_cogs": 45.00,
        "unit_retail_price": 90.00,
        "baseline_units": 15,
    },
    {
        "product_id": "SKU-003",
        "product_name": "Wireless Earbuds",
        "category": "Electronics",
        "unit_cogs": 60.00,
        "unit_retail_price": 120.00,
        "baseline_units": 20,
    },
    {
        "product_id": "SKU-004",
        "product_name": "Smart Speaker",
        "category": "Electronics",
        "unit_cogs": 80.00,
        "unit_retail_price": 150.00,
        "baseline_units": 12,
    },
    {
        "product_id": "SKU-005",
        "product_name": "Espresso Maker",
        "category": "Home",
        "unit_cogs": 110.00,
        "unit_retail_price": 220.00,
        "baseline_units": 8,
    },
    {
        "product_id": "SKU-006",
        "product_name": "Air Purifier",
        "category": "Home",
        "unit_cogs": 75.00,
        "unit_retail_price": 150.00,
        "baseline_units": 14,
    },
]

CATEGORY_TARGETS = [
    {"category": "Apparel", "fiscal_quarter": "2026-Q1", "target_gross_margin_pct": 50.0, "target_revenue": 280000.00},
    {"category": "Apparel", "fiscal_quarter": "2026-Q2", "target_gross_margin_pct": 50.0, "target_revenue": 290000.00},
    {"category": "Apparel", "fiscal_quarter": "2026-Q3", "target_gross_margin_pct": 50.0, "target_revenue": 300000.00},
    {"category": "Apparel", "fiscal_quarter": "2026-Q4", "target_gross_margin_pct": 52.0, "target_revenue": 350000.00},
    {"category": "Electronics", "fiscal_quarter": "2026-Q1", "target_gross_margin_pct": 45.0, "target_revenue": 450000.00},
    {"category": "Electronics", "fiscal_quarter": "2026-Q2", "target_gross_margin_pct": 45.0, "target_revenue": 480000.00},
    {"category": "Electronics", "fiscal_quarter": "2026-Q3", "target_gross_margin_pct": 45.0, "target_revenue": 500000.00},
    {"category": "Electronics", "fiscal_quarter": "2026-Q4", "target_gross_margin_pct": 46.0, "target_revenue": 600000.00},
    {"category": "Home", "fiscal_quarter": "2026-Q1", "target_gross_margin_pct": 52.0, "target_revenue": 360000.00},
    {"category": "Home", "fiscal_quarter": "2026-Q2", "target_gross_margin_pct": 52.0, "target_revenue": 380000.00},
    {"category": "Home", "fiscal_quarter": "2026-Q3", "target_gross_margin_pct": 52.0, "target_revenue": 400000.00},
    {"category": "Home", "fiscal_quarter": "2026-Q4", "target_gross_margin_pct": 53.0, "target_revenue": 450000.00},
]


def write_stores() -> None:
  with open(DATA_DIR / "stores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["store_id", "store_name", "region", "city"])
    for store in STORES:
      writer.writerow([
          store["store_id"],
          store["store_name"],
          store["region"],
          store["city"],
      ])


def write_product_cost_master() -> None:
  with open(DATA_DIR / "product_cost_master.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["product_id", "product_name", "category", "unit_cogs", "unit_retail_price"])
    for product in PRODUCTS:
      writer.writerow([
          product["product_id"],
          product["product_name"],
          product["category"],
          f"{product['unit_cogs']:.2f}",
          f"{product['unit_retail_price']:.2f}",
      ])


def write_sales_profitability(rng: random.Random) -> None:
  start_date = SALES_WINDOW_END - datetime.timedelta(days=SALES_WINDOW_DAYS - 1)

  with open(DATA_DIR / "sales_profitability.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "product_id",
        "date",
        "units_sold",
        "gross_revenue",
        "cogs_amount",
        "markdown_discount_amount",
        "net_revenue",
        "gross_margin_amount",
        "gross_margin_pct",
    ])

    for day_offset in range(SALES_WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      is_weekend = current_date.weekday() >= 5
      weekend_mult = 1.3 if is_weekend else 1.0

      for store in STORES:
        store_id = store["store_id"]
        for product in PRODUCTS:
          product_id = product["product_id"]
          baseline = product["baseline_units"]
          units_sold = max(1, round(baseline * weekend_mult + rng.uniform(-2.0, 3.0)))

          gross_revenue = round(units_sold * product["unit_retail_price"], 2)
          cogs_amount = round(units_sold * product["unit_cogs"], 2)

          # Markdown discount applies occasionally or on promo days
          discount_pct = rng.choice([0.0, 0.0, 0.0, 0.05, 0.10, 0.15])
          markdown_discount_amount = round(gross_revenue * discount_pct, 2)

          net_revenue = round(gross_revenue - markdown_discount_amount, 2)
          gross_margin_amount = round(net_revenue - cogs_amount, 2)
          gross_margin_pct = (
              round((gross_margin_amount / net_revenue) * 100.0, 2) if net_revenue > 0 else 0.0
          )

          writer.writerow([
              store_id,
              product_id,
              current_date.isoformat(),
              units_sold,
              f"{gross_revenue:.2f}",
              f"{cogs_amount:.2f}",
              f"{markdown_discount_amount:.2f}",
              f"{net_revenue:.2f}",
              f"{gross_margin_amount:.2f}",
              f"{gross_margin_pct:.2f}",
          ])


def write_category_margin_targets() -> None:
  with open(DATA_DIR / "category_margin_targets.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "category",
        "fiscal_quarter",
        "target_gross_margin_pct",
        "target_revenue",
    ])
    for item in CATEGORY_TARGETS:
      writer.writerow([
          item["category"],
          item["fiscal_quarter"],
          f"{item['target_gross_margin_pct']:.2f}",
          f"{item['target_revenue']:.2f}",
      ])


def main() -> None:
  rng = random.Random(42)
  write_stores()
  write_product_cost_master()
  write_sales_profitability(rng)
  write_category_margin_targets()
  print(f"Generated 4 seed data CSVs in {DATA_DIR}")


if __name__ == "__main__":
  main()
