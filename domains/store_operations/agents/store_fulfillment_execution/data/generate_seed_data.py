#!/usr/bin/env python3
"""Generates synthetic seed CSV data for Store Operations: Store Fulfillment & Execution agent.

Generates 4 CSV files under domains/store_operations/agents/store_fulfillment_execution/data/:
1. stores.csv (store_id STORE-001..STORE-004, store_name, region, district_manager, bopis_enabled_flag)
2. bopis_orders.csv (order_id ORD-001..ORD-020, store_id, order_timestamp, fulfillment_status, pick_ready_timestamp, customer_pickup_timestamp, fulfillment_time_minutes; date anchor 2026-07-24)
3. fulfillment_slas.csv (store_id, date, total_bopis_orders, orders_met_sla_count, sla_compliance_pct, avg_pick_time_minutes, avg_curbside_wait_minutes; date anchor 2026-07-24)
4. pick_accuracy_summary.csv (store_id, department, date, total_items_picked, mispicked_items_count, out_of_stock_cancellations, pick_accuracy_pct; date anchor 2026-07-24)

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
        "bopis_enabled_flag": "TRUE",
    },
    {
        "store_id": "STORE-002",
        "store_name": "Suburban Plaza",
        "region": "West",
        "district_manager": "Sarah Jenkins",
        "bopis_enabled_flag": "TRUE",
    },
    {
        "store_id": "STORE-003",
        "store_name": "Metro Center",
        "region": "Midwest",
        "district_manager": "Michael Chang",
        "bopis_enabled_flag": "TRUE",
    },
    {
        "store_id": "STORE-004",
        "store_name": "City Galleria",
        "region": "East",
        "district_manager": "David Ross",
        "bopis_enabled_flag": "TRUE",
    },
]

DEPARTMENTS = ["Grocery", "Apparel", "Electronics", "Home"]


def write_stores() -> None:
  with open(DATA_DIR / "stores.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "store_name",
        "region",
        "district_manager",
        "bopis_enabled_flag",
    ])
    for store in STORES:
      writer.writerow([
          store["store_id"],
          store["store_name"],
          store["region"],
          store["district_manager"],
          store["bopis_enabled_flag"],
      ])


def write_bopis_orders(rng: random.Random) -> None:
  statuses = ["Completed", "Completed", "Completed", "Picked", "Cancelled"]
  with open(DATA_DIR / "bopis_orders.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "order_id",
        "store_id",
        "order_timestamp",
        "fulfillment_status",
        "pick_ready_timestamp",
        "customer_pickup_timestamp",
        "fulfillment_time_minutes",
    ])
    for idx in range(1, 21):
      order_id = f"ORD-{idx:03d}"
      store_idx = (idx - 1) % len(STORES)
      store_id = STORES[store_idx]["store_id"]
      status = rng.choice(statuses)

      day_offset = (idx - 1) % 5
      base_dt = datetime.datetime.combine(
          WINDOW_END - datetime.timedelta(days=day_offset),
          datetime.time(8 + (idx % 10), (idx * 7) % 60),
      )
      order_ts = base_dt.isoformat() + "Z"

      if status in ["Completed", "Picked"]:
        pick_time_mins = rng.randint(12, 45)
        pick_dt = base_dt + datetime.timedelta(minutes=pick_time_mins)
        pick_ready_ts = pick_dt.isoformat() + "Z"
      else:
        pick_time_mins = rng.randint(15, 60)
        pick_ready_ts = ""

      if status == "Completed":
        pickup_wait_mins = rng.randint(3, 15)
        pickup_dt = pick_dt + datetime.timedelta(minutes=pickup_wait_mins)
        customer_pickup_ts = pickup_dt.isoformat() + "Z"
        fulfillment_mins = pick_time_mins + pickup_wait_mins
      else:
        customer_pickup_ts = ""
        fulfillment_mins = pick_time_mins

      writer.writerow([
          order_id,
          store_id,
          order_ts,
          status,
          pick_ready_ts,
          customer_pickup_ts,
          fulfillment_mins,
      ])


def write_fulfillment_slas(rng: random.Random) -> None:
  start_date = WINDOW_END - datetime.timedelta(days=WINDOW_DAYS - 1)
  with open(DATA_DIR / "fulfillment_slas.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "date",
        "total_bopis_orders",
        "orders_met_sla_count",
        "sla_compliance_pct",
        "avg_pick_time_minutes",
        "avg_curbside_wait_minutes",
    ])
    for day_offset in range(WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      for store in STORES:
        store_id = store["store_id"]
        total_orders = rng.randint(25, 60)
        met_sla = rng.randint(round(total_orders * 0.75), total_orders)
        sla_pct = round((met_sla / total_orders) * 100.0, 2)
        avg_pick_mins = round(rng.uniform(14.0, 28.0), 1)
        avg_curbside_wait_mins = round(rng.uniform(3.0, 9.5), 1)

        writer.writerow([
            store_id,
            current_date.isoformat(),
            total_orders,
            met_sla,
            sla_pct,
            avg_pick_mins,
            avg_curbside_wait_mins,
        ])


def write_pick_accuracy_summary(rng: random.Random) -> None:
  start_date = WINDOW_END - datetime.timedelta(days=WINDOW_DAYS - 1)
  with open(DATA_DIR / "pick_accuracy_summary.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "store_id",
        "department",
        "date",
        "total_items_picked",
        "mispicked_items_count",
        "out_of_stock_cancellations",
        "pick_accuracy_pct",
    ])
    for day_offset in range(WINDOW_DAYS):
      current_date = start_date + datetime.timedelta(days=day_offset)
      for store in STORES:
        store_id = store["store_id"]
        for dept in DEPARTMENTS:
          total_items = rng.randint(100, 350)
          mispicked = rng.randint(1, 12)
          oos_cancels = rng.randint(0, 6)
          accuracy_pct = round(
              ((total_items - mispicked) / total_items) * 100.0, 2
          )

          writer.writerow([
              store_id,
              dept,
              current_date.isoformat(),
              total_items,
              mispicked,
              oos_cancels,
              accuracy_pct,
          ])


def main() -> None:
  rng = random.Random(42)
  write_stores()
  write_bopis_orders(rng)
  write_fulfillment_slas(rng)
  write_pick_accuracy_summary(rng)
  print(f"Generated 4 seed data CSVs in {DATA_DIR}")


if __name__ == "__main__":
  main()
