#!/usr/bin/env python3
"""Generates this agent's synthetic BigQuery seed data (data/*.csv).

Run once; the output is committed as static CSVs, not regenerated at load time.

Usage:
    uv run python domains/merchandising/agents/sell_through_inventory_health/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DATE_ANCHOR = datetime.date(2026, 7, 24)

STORES = ["STORE-001", "STORE-002", "STORE-003", "STORE-004"]

PRODUCTS = [
    {"product_id": "SKU-001", "product_name": "Down Parka", "category": "Men's Outerwear",
     "sub_category": "Jackets & Parkas", "unit_cost": 100.00, "unit_retail_price": 180.00},
    {"product_id": "SKU-002", "product_name": "Rain Jacket", "category": "Men's Outerwear",
     "sub_category": "Jackets & Parkas", "unit_cost": 50.00, "unit_retail_price": 90.00},
    {"product_id": "SKU-003", "product_name": "Fleece Vest", "category": "Men's Outerwear",
     "sub_category": "Vests", "unit_cost": 35.00, "unit_retail_price": 65.00},
    {"product_id": "SKU-004", "product_name": "Running Shoe", "category": "Women's Footwear",
     "sub_category": "Athletic", "unit_cost": 50.00, "unit_retail_price": 95.00},
    {"product_id": "SKU-005", "product_name": "Ankle Boot", "category": "Women's Footwear",
     "sub_category": "Boots", "unit_cost": 60.00, "unit_retail_price": 110.00},
    {"product_id": "SKU-006", "product_name": "Sandal", "category": "Women's Footwear",
     "sub_category": "Sandals", "unit_cost": 18.00, "unit_retail_price": 35.00},
]


def write_product_catalog() -> None:
    with open(DATA_DIR / "product_catalog.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "product_id", "product_name", "category", "sub_category",
            "unit_cost", "unit_retail_price",
        ])
        for product in PRODUCTS:
            writer.writerow([
                product["product_id"], product["product_name"], product["category"],
                product["sub_category"], product["unit_cost"], product["unit_retail_price"],
            ])


def write_store_inventory(rng: random.Random) -> None:
    with open(DATA_DIR / "store_inventory.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "store_id", "product_id", "on_hand_units", "allocated_units", "in_transit_units",
        ])
        for store_id in STORES:
            # Store 001 fast turn, Store 003 slow/overstocked
            store_mult = 0.8 if store_id == "STORE-001" else (1.5 if store_id == "STORE-003" else 1.0)
            for product in PRODUCTS:
                base_oh = 80 if product["category"] == "Men's Outerwear" else 120
                on_hand = int(base_oh * store_mult + rng.randint(-10, 10))
                allocated = int(on_hand * 0.2)
                in_transit = int(on_hand * 0.15)
                writer.writerow([store_id, product["product_id"], on_hand, allocated, in_transit])


def write_sell_through_weekly(rng: random.Random) -> None:
    # 4 weeks ending up to 2026-07-24
    weeks = [DATE_ANCHOR - datetime.timedelta(weeks=i) for i in reversed(range(4))]
    with open(DATA_DIR / "sell_through_weekly.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "store_id", "product_id", "week_ending_date", "units_received",
            "units_sold", "sell_through_pct", "weeks_of_supply",
        ])
        for store_id in STORES:
            # STORE-001 turns fast (low weeks of supply ~3-4), STORE-003 turns slow (~8-10)
            store_speed = 1.3 if store_id == "STORE-001" else (0.7 if store_id == "STORE-003" else 1.0)
            for product in PRODUCTS:
                is_outerwear = product["category"] == "Men's Outerwear"
                # Outerwear sell-through higher (~75-85%), Footwear lower (~50-62%)
                base_st_target = 0.80 if is_outerwear else 0.55
                for week in weeks:
                    received = rng.randint(80, 120)
                    st_rate = min(0.95, max(0.40, base_st_target * store_speed + rng.uniform(-0.04, 0.04)))
                    sold = int(round(received * st_rate))
                    sell_through_pct = round((sold / received) * 100.0, 2)
                    
                    # WOS = on_hand / weekly_sales
                    on_hand_approx = (150 if is_outerwear else 200) / store_speed
                    wos = round(on_hand_approx / max(1, sold), 2)
                    
                    writer.writerow([
                        store_id, product["product_id"], week.isoformat(),
                        received, sold, sell_through_pct, wos,
                    ])


def write_aging_inventory_summary(rng: random.Random) -> None:
    buckets = ["0-30", "31-60", "61-90", "90+"]
    with open(DATA_DIR / "aging_inventory_summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "store_id", "product_id", "aging_bucket_days", "aging_units",
            "aging_cost_value", "markdown_risk_flag",
        ])
        for store_id in STORES:
            for product in PRODUCTS:
                # Ankle Boot (SKU-005) & Sandal (SKU-006) have high aging in 90+ bucket across stores
                is_aging_risk_sku = product["product_id"] in ("SKU-005", "SKU-006")
                
                for bucket in buckets:
                    if bucket == "0-30":
                        units = rng.randint(40, 70)
                    elif bucket == "31-60":
                        units = rng.randint(20, 40)
                    elif bucket == "61-90":
                        units = rng.randint(10, 25)
                    else:  # 90+
                        if is_aging_risk_sku:
                            units = rng.randint(35, 60)
                        else:
                            units = rng.randint(2, 8)
                    
                    cost_val = round(units * product["unit_cost"], 2)
                    markdown_risk = "true" if (bucket == "90+" and units >= 30) else "false"
                    
                    writer.writerow([
                        store_id, product["product_id"], bucket,
                        units, cost_val, markdown_risk,
                    ])


def main() -> None:
    rng = random.Random(42)
    write_product_catalog()
    write_store_inventory(rng)
    write_sell_through_weekly(rng)
    write_aging_inventory_summary(rng)
    print(f"Wrote seed CSVs to {DATA_DIR}")


if __name__ == "__main__":
    main()
