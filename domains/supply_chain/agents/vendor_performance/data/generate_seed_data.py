#!/usr/bin/env python3
"""Generates this agent's synthetic BigQuery seed data (data/*.csv).

Run once; the output is committed as static CSVs, not regenerated at load time. See
docs/superpowers/specs/2026-07-26-vendor-performance-agent-design.md (local-only, gitignored,
not on a fresh clone) for the schema and data design this implements.

Per the cross-agent seed-data guidelines in `_shared/table_registry.yaml`'s header comment:
reuses the same SKU-001..006 identifiers already established by
domains/merchandising/agents/{assortment_planning,pricing_promotions}, and anchors to the same
`WINDOW_END` date Assortment Planning uses so all three agents read as one consistent timeline.

Usage:
    uv run python domains/supply_chain/agents/vendor_performance/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

# Same anchor as domains/merchandising/agents/assortment_planning/data/generate_seed_data.py's
# SALES_WINDOW_END -- keeps all agents' synthetic data on one shared timeline.
WINDOW_END = datetime.date(2026, 7, 24)
PO_ORDER_START = datetime.date(2026, 4, 1)
PO_COUNT_PER_VENDOR = 10
PO_SPACING_DAYS = 9  # 10 POs * 9 days = 90-day order window, ending 2026-06-21
EXPECTED_LEAD_DAYS = 14  # order_date -> expected_delivery_date

# Same 6 products already established by assortment_planning/pricing_promotions.
PRODUCTS = [
    {"product_id": "SKU-001", "product_name": "Down Parka", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "launch_date": "2024-01-15", "status": "active"},
    {"product_id": "SKU-002", "product_name": "Rain Jacket", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "launch_date": "2024-01-15", "status": "active"},
    {"product_id": "SKU-003", "product_name": "Fleece Vest", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "launch_date": "2024-01-15", "status": "active"},
    {"product_id": "SKU-004", "product_name": "Running Shoe", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "launch_date": "2024-01-15", "status": "active"},
    {"product_id": "SKU-005", "product_name": "Ankle Boot", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "launch_date": "2024-01-15", "status": "active"},
    {"product_id": "SKU-006", "product_name": "Sandal", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "launch_date": "2024-01-15", "status": "active"},
]

# "outcomes" is a 10-element list of (delay_days, shortfall_fraction) applied round-robin to each
# vendor's 10 POs. delay_days > 0 means late (actual_delivery_date is that many days after
# expected); shortfall_fraction > 0 means quantity_received is short by that fraction.
BEST_OUTCOMES = [
    (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (2, 0.0),
    (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0), (0, 0.0),
]  # 9/10 on-time + in-full -> OTIF 90% (engineered best performer)

MID_OUTCOMES = [
    (0, 0.0), (0, 0.0), (3, 0.0), (0, 0.0), (0, 0.0),
    (0, 0.15), (0, 0.0), (0, 0.0), (4, 0.0), (0, 0.0),
]  # 7/10 on-time + in-full -> OTIF 70% (engineered mid performer)

WORST_OUTCOMES = [
    (0, 0.0), (5, 0.0), (0, 0.10), (4, 0.20), (0, 0.0),
    (7, 0.0), (0, 0.10), (3, 0.15), (0, 0.0), (6, 0.0),
]  # 3/10 on-time + in-full -> OTIF 30% (engineered worst performer)

VENDORS = [
    {"vendor_id": "VEND-001", "vendor_name": "Highland Textile Mills",
     "category": "Apparel Manufacturing", "region": "North America",
     "onboarded_date": "2022-01-10", "status": "active",
     "skus": ["SKU-001", "SKU-002"], "outcomes": BEST_OUTCOMES},
    {"vendor_id": "VEND-002", "vendor_name": "Cascade Apparel Co",
     "category": "Apparel Manufacturing", "region": "North America",
     "onboarded_date": "2022-06-15", "status": "active",
     "skus": ["SKU-003"], "outcomes": MID_OUTCOMES},
    {"vendor_id": "VEND-003", "vendor_name": "Meridian Footwear Group",
     "category": "Footwear Manufacturing", "region": "Asia Pacific",
     "onboarded_date": "2021-11-01", "status": "active",
     "skus": ["SKU-004", "SKU-005"], "outcomes": MID_OUTCOMES},
    {"vendor_id": "VEND-004", "vendor_name": "Riverside Footwear Supply",
     "category": "Footwear Manufacturing", "region": "Asia Pacific",
     "onboarded_date": "2023-03-20", "status": "active",
     "skus": ["SKU-006"], "outcomes": WORST_OUTCOMES},
]

BASE_QUANTITY_ORDERED = 200


def write_product_catalog() -> None:
  with open(DATA_DIR / "product_catalog.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "product_id", "product_name", "category", "department", "brand", "launch_date", "status",
    ])
    for product in PRODUCTS:
      writer.writerow([
          product["product_id"], product["product_name"], product["category"],
          product["department"], product["brand"], product["launch_date"], product["status"],
      ])


def write_vendors() -> None:
  with open(DATA_DIR / "vendors.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "vendor_id", "vendor_name", "category", "region", "onboarded_date", "status",
    ])
    for vendor in VENDORS:
      writer.writerow([
          vendor["vendor_id"], vendor["vendor_name"], vendor["category"], vendor["region"],
          vendor["onboarded_date"], vendor["status"],
      ])


def _generate_purchase_orders_for_vendor(vendor: dict) -> list[dict]:
  pos = []
  for i in range(PO_COUNT_PER_VENDOR):
    order_date = PO_ORDER_START + datetime.timedelta(days=i * PO_SPACING_DAYS)
    expected_delivery_date = order_date + datetime.timedelta(days=EXPECTED_LEAD_DAYS)
    delay_days, shortfall_fraction = vendor["outcomes"][i]
    actual_delivery_date = expected_delivery_date + datetime.timedelta(days=delay_days)
    sku_id = vendor["skus"][i % len(vendor["skus"])]
    quantity_ordered = BASE_QUANTITY_ORDERED
    quantity_received = round(quantity_ordered * (1 - shortfall_fraction))

    on_time = actual_delivery_date <= expected_delivery_date
    in_full = quantity_received >= quantity_ordered

    pos.append({
        "po_id": f"PO-{vendor['vendor_id'][-3:]}-{i + 1:03d}",
        "vendor_id": vendor["vendor_id"],
        "sku_id": sku_id,
        "order_date": order_date.isoformat(),
        "expected_delivery_date": expected_delivery_date.isoformat(),
        "actual_delivery_date": actual_delivery_date.isoformat(),
        "quantity_ordered": quantity_ordered,
        "quantity_received": quantity_received,
        "on_time": on_time,
        "in_full": in_full,
        "delay_days": max(delay_days, 0),
    })
  return pos


def write_purchase_orders(all_pos: list[dict]) -> None:
  with open(DATA_DIR / "purchase_orders.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "po_id", "vendor_id", "sku_id", "order_date", "expected_delivery_date",
        "actual_delivery_date", "quantity_ordered", "quantity_received", "on_time", "in_full",
    ])
    for po in all_pos:
      writer.writerow([
          po["po_id"], po["vendor_id"], po["sku_id"], po["order_date"],
          po["expected_delivery_date"], po["actual_delivery_date"], po["quantity_ordered"],
          po["quantity_received"], po["on_time"], po["in_full"],
      ])


def write_vendor_scorecard(all_pos: list[dict]) -> None:
  period_start = PO_ORDER_START.isoformat()
  period_end = (PO_ORDER_START + datetime.timedelta(
      days=(PO_COUNT_PER_VENDOR - 1) * PO_SPACING_DAYS + EXPECTED_LEAD_DAYS
  )).isoformat()

  with open(DATA_DIR / "vendor_scorecard.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "vendor_id", "period_start", "period_end", "total_pos", "on_time_pos", "in_full_pos",
        "otif_pos", "otif_pct", "avg_delay_days",
    ])
    for vendor in VENDORS:
      vendor_pos = [po for po in all_pos if po["vendor_id"] == vendor["vendor_id"]]
      total_pos = len(vendor_pos)
      on_time_pos = sum(1 for po in vendor_pos if po["on_time"])
      in_full_pos = sum(1 for po in vendor_pos if po["in_full"])
      otif_pos = sum(1 for po in vendor_pos if po["on_time"] and po["in_full"])
      otif_pct = round(otif_pos / total_pos * 100, 1)
      avg_delay_days = round(sum(po["delay_days"] for po in vendor_pos) / total_pos, 1)

      writer.writerow([
          vendor["vendor_id"], period_start, period_end, total_pos, on_time_pos, in_full_pos,
          otif_pos, otif_pct, avg_delay_days,
      ])


def main() -> None:
  write_product_catalog()
  write_vendors()
  all_pos = []
  for vendor in VENDORS:
    all_pos.extend(_generate_purchase_orders_for_vendor(vendor))
  write_purchase_orders(all_pos)
  write_vendor_scorecard(all_pos)

  latest_delivery = max(datetime.date.fromisoformat(po["actual_delivery_date"]) for po in all_pos)
  assert latest_delivery < WINDOW_END, (
      f"Latest delivery {latest_delivery} must be before WINDOW_END {WINDOW_END}"
  )
  print(f"Wrote seed CSVs to {DATA_DIR}")


if __name__ == "__main__":
  main()
