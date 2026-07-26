#!/usr/bin/env python3
"""Generates this agent's synthetic BigQuery seed data (data/*.csv).

Run once; the output is committed as static CSVs, not regenerated at load time. See
docs/superpowers/specs/2026-07-26-inventory-planning-agent-design.md (local-only, gitignored,
not on a fresh clone) for the schema and data design this implements.

Per the cross-agent seed-data guidelines in `_shared/table_registry.yaml`'s header comment:
reuses the same SKU-001..006 and STORE-101/STORE-102 identifiers already established by
domains/merchandising/agents/{assortment_planning,pricing_promotions}, and anchors to the same
`WINDOW_END` date Assortment Planning uses. Adds two new warehouse identifiers (WH-001, WH-002)
-- the first agent in this repo to introduce a warehouse location dimension.

`demand_history` is a genuine daily time-series table, NOT a precomputed forecast -- this agent's
data_insights sub-agent is meant to call ADK's built-in `forecast` tool (BigQuery's AI.FORECAST,
TimesFM 2.0) live against this table, not read a pre-baked future-numbers table. The engineered
trends below (a strong upward trend for one sku/store, a decline for another) are what make that
live forecast produce an unambiguous qualitative signal (rising vs. falling demand), even though
this script cannot and does not control AI.FORECAST's exact output values.

Usage:
    uv run python domains/supply_chain/agents/inventory_planning/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

# Same anchor as domains/merchandising/agents/assortment_planning/data/generate_seed_data.py's
# SALES_WINDOW_END -- keeps all agents' synthetic data on one shared timeline.
WINDOW_END = datetime.date(2026, 7, 24)
HISTORY_WINDOW_DAYS = 60

STORES = ["STORE-101", "STORE-102"]  # reused from assortment_planning
WAREHOUSES = ["WH-001", "WH-002"]  # new in this agent

# Same 6 products already established by assortment_planning/pricing_promotions.
PRODUCTS = [
    {"product_id": "SKU-001", "product_name": "Down Parka", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "launch_date": "2024-01-15",
     "status": "active", "baseline_units": 6},
    {"product_id": "SKU-002", "product_name": "Rain Jacket", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "launch_date": "2024-01-15",
     "status": "active", "baseline_units": 8},
    {"product_id": "SKU-003", "product_name": "Fleece Vest", "category": "Men's Outerwear",
     "department": "Apparel", "brand": "Alpine Gear", "launch_date": "2024-01-15",
     "status": "active", "baseline_units": 10},
    {"product_id": "SKU-004", "product_name": "Running Shoe", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "launch_date": "2024-01-15",
     "status": "active", "baseline_units": 12},
    {"product_id": "SKU-005", "product_name": "Ankle Boot", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "launch_date": "2024-01-15",
     "status": "active", "baseline_units": 7},
    {"product_id": "SKU-006", "product_name": "Sandal", "category": "Women's Footwear",
     "department": "Footwear", "brand": "Strideline", "launch_date": "2024-01-15",
     "status": "active", "baseline_units": 9},
]

# Engineered demand trends, applied to specific (sku, store) pairs on top of the flat baseline.
# "rising": trend_factor grows from 1.0 to RISING_END_FACTOR across the window (stockout-risk
# scenario, paired with a deliberately low inventory_position override below).
# "declining": trend_factor shrinks from 1.0 to DECLINING_END_FACTOR (overstock scenario).
RISING_SKU_STORE = ("SKU-004", "STORE-101")
RISING_END_FACTOR = 3.0
DECLINING_SKU = "SKU-006"  # declines at BOTH stores, feeding the WH-001 overstock scenario
DECLINING_END_FACTOR = 0.35

STOCKOUT_LOCATION = "STORE-101"
STOCKOUT_SKU = "SKU-004"
STOCKOUT_ON_HAND = 8  # a few hours of cover against the rising trend above

OVERSTOCK_LOCATION = "WH-001"
OVERSTOCK_SKU = "SKU-006"
OVERSTOCK_ON_HAND = 600  # many weeks of cover against the declining trend above


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


def _trend_factor(sku_id: str, store_id: str, day_offset: int) -> float:
  progress = day_offset / (HISTORY_WINDOW_DAYS - 1)
  if (sku_id, store_id) == RISING_SKU_STORE:
    return 1.0 + (RISING_END_FACTOR - 1.0) * progress
  if sku_id == DECLINING_SKU:
    return 1.0 + (DECLINING_END_FACTOR - 1.0) * progress
  return 1.0


def write_demand_history(rng: random.Random) -> dict[tuple[str, str], float]:
  """Writes the daily demand time series and returns each (sku_id, store_id)'s average units
  sold over the final 14 days of the window, used to set realistic (non-engineered) inventory
  position defaults elsewhere.
  """
  start_date = WINDOW_END - datetime.timedelta(days=HISTORY_WINDOW_DAYS - 1)
  recent_totals: dict[tuple[str, str], list[float]] = {}

  with open(DATA_DIR / "demand_history.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "store_id", "sku_id", "units_sold"])

    for day_offset in range(HISTORY_WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      is_weekend = current_date.weekday() >= 5

      for store_id in STORES:
        for product in PRODUCTS:
          sku_id = product["product_id"]
          baseline = product["baseline_units"]
          units = baseline * 1.25 if is_weekend else baseline
          units *= _trend_factor(sku_id, store_id, day_offset)
          units = max(0, round(units + rng.uniform(-1.0, 1.0)))

          writer.writerow([current_date.isoformat(), store_id, sku_id, units])
          recent_totals.setdefault((sku_id, store_id), []).append(units)

  return {
      key: sum(values[-14:]) / len(values[-14:])
      for key, values in recent_totals.items()
  }


def write_inventory_position(recent_avg_daily: dict[tuple[str, str], float]) -> None:
  with open(DATA_DIR / "inventory_position.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["location_id", "location_type", "sku_id", "on_hand_units", "as_of_date"])

    for store_id in STORES:
      for product in PRODUCTS:
        sku_id = product["product_id"]
        if (store_id, sku_id) == (STOCKOUT_LOCATION, STOCKOUT_SKU):
          on_hand = STOCKOUT_ON_HAND
        else:
          # A plausible ~5 days of store-level cover against recent average daily demand.
          on_hand = max(4, round(recent_avg_daily.get((sku_id, store_id), 5.0) * 5))
        writer.writerow([store_id, "STORE", sku_id, on_hand, WINDOW_END.isoformat()])

    for warehouse_id in WAREHOUSES:
      for product in PRODUCTS:
        sku_id = product["product_id"]
        if (warehouse_id, sku_id) == (OVERSTOCK_LOCATION, OVERSTOCK_SKU):
          on_hand = OVERSTOCK_ON_HAND
        else:
          # A plausible ~25 days of network-wide (both stores) cover, split across 2 warehouses.
          network_daily = sum(recent_avg_daily.get((sku_id, s), 5.0) for s in STORES)
          on_hand = max(20, round(network_daily * 25 / len(WAREHOUSES)))
        writer.writerow([warehouse_id, "WAREHOUSE", sku_id, on_hand, WINDOW_END.isoformat()])


def main() -> None:
  rng = random.Random(42)
  write_product_catalog()
  recent_avg_daily = write_demand_history(rng)
  write_inventory_position(recent_avg_daily)
  print(f"Wrote seed CSVs to {DATA_DIR}")


if __name__ == "__main__":
  main()
