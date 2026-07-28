#!/usr/bin/env python3
"""Generates synthetic seed CSV data for Finance: Store P&L & Operating Costs agent.

Generates 4 CSV files under domains/finance/agents/store_pnl_operating_costs/data/:
1. stores.csv (store_id, store_name, region, store_square_feet, store_manager)
2. monthly_pnl.csv (store_id, fiscal_month, gross_sales, net_sales, cogs, gross_profit, store_labor_cost, store_rent_cost, utilities_cost, maintenance_cost, marketing_allocation, store_ebitda)
3. opex_categories.csv (store_id, fiscal_month, opex_category, budgeted_amount, actual_amount, variance_amount, variance_pct)
4. profitability_targets.csv (region, fiscal_year, target_ebitda_pct, target_opex_to_sales_pct)

Usage:
    uv run python domains/finance/agents/store_pnl_operating_costs/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DATE_ANCHOR = datetime.date(2026, 7, 24)

STORES = [
    {
        "store_id": "STORE-001",
        "store_name": "Downtown Flagship",
        "region": "West",
        "store_square_feet": 25000,
        "store_manager": "Alice Smith",
    },
    {
        "store_id": "STORE-002",
        "store_name": "Suburban Plaza",
        "region": "West",
        "store_square_feet": 18000,
        "store_manager": "Bob Jones",
    },
    {
        "store_id": "STORE-003",
        "store_name": "Metro Center",
        "region": "Midwest",
        "store_square_feet": 30000,
        "store_manager": "Carol White",
    },
    {
        "store_id": "STORE-004",
        "store_name": "City Galleria",
        "region": "East",
        "store_square_feet": 22000,
        "store_manager": "David Brown",
    },
]

MONTHS = ["2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06"]

OPEX_CATEGORIES = ["Rent", "Utilities", "Labor", "Maintenance", "Supplies"]

PROFITABILITY_TARGETS = [
    {"region": "West", "fiscal_year": 2026, "target_ebitda_pct": 16.0, "target_opex_to_sales_pct": 28.0},
    {"region": "Midwest", "fiscal_year": 2026, "target_ebitda_pct": 14.0, "target_opex_to_sales_pct": 30.0},
    {"region": "East", "fiscal_year": 2026, "target_ebitda_pct": 15.0, "target_opex_to_sales_pct": 29.0},
    {"region": "South", "fiscal_year": 2026, "target_ebitda_pct": 13.5, "target_opex_to_sales_pct": 31.0},
]


def write_stores() -> None:
    with open(DATA_DIR / "stores.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["store_id", "store_name", "region", "store_square_feet", "store_manager"])
        for store in STORES:
            writer.writerow([
                store["store_id"],
                store["store_name"],
                store["region"],
                store["store_square_feet"],
                store["store_manager"],
            ])


def write_monthly_pnl(rng: random.Random) -> None:
    with open(DATA_DIR / "monthly_pnl.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "store_id",
            "fiscal_month",
            "gross_sales",
            "net_sales",
            "cogs",
            "gross_profit",
            "store_labor_cost",
            "store_rent_cost",
            "utilities_cost",
            "maintenance_cost",
            "marketing_allocation",
            "store_ebitda",
        ])

        # Base numbers per store
        base_sales = {
            "STORE-001": 320000.00,
            "STORE-002": 210000.00,
            "STORE-003": 380000.00,
            "STORE-004": 260000.00,
        }

        for store in STORES:
            store_id = store["store_id"]
            base = base_sales[store_id]
            sqft = store["store_square_feet"]

            for m in MONTHS:
                # Add slight monthly variation
                var_factor = 1.0 + rng.uniform(-0.05, 0.05)
                gross_sales = round(base * var_factor, 2)
                discount_pct = rng.uniform(0.02, 0.05)
                net_sales = round(gross_sales * (1 - discount_pct), 2)
                cogs = round(net_sales * rng.uniform(0.50, 0.54), 2)
                gross_profit = round(net_sales - cogs, 2)

                labor = round(net_sales * rng.uniform(0.15, 0.18), 2)
                rent = round(sqft * 0.85, 2)  # Fixed rent based on square footage
                utilities = round(sqft * 0.18 + rng.uniform(-200, 200), 2)
                maint = round(sqft * 0.08 + rng.uniform(-100, 150), 2)
                mktg = round(net_sales * 0.02, 2)

                total_opex = labor + rent + utilities + maint + mktg
                ebitda = round(gross_profit - total_opex, 2)

                writer.writerow([
                    store_id,
                    m,
                    f"{gross_sales:.2f}",
                    f"{net_sales:.2f}",
                    f"{cogs:.2f}",
                    f"{gross_profit:.2f}",
                    f"{labor:.2f}",
                    f"{rent:.2f}",
                    f"{utilities:.2f}",
                    f"{maint:.2f}",
                    f"{mktg:.2f}",
                    f"{ebitda:.2f}",
                ])


def write_opex_categories(rng: random.Random) -> None:
    with open(DATA_DIR / "opex_categories.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "store_id",
            "fiscal_month",
            "opex_category",
            "budgeted_amount",
            "actual_amount",
            "variance_amount",
            "variance_pct",
        ])

        base_budgets = {
            "Rent": 18000.00,
            "Utilities": 4500.00,
            "Labor": 38000.00,
            "Maintenance": 2500.00,
            "Supplies": 1500.00,
        }

        for store in STORES:
            store_id = store["store_id"]
            sqft_scale = store["store_square_feet"] / 20000.0

            for m in MONTHS:
                for category in OPEX_CATEGORIES:
                    budget = round(base_budgets[category] * sqft_scale, 2)
                    # Actual variance between -8% and +12%
                    variance_factor = rng.uniform(-0.08, 0.12)
                    actual = round(budget * (1.0 + variance_factor), 2)
                    variance_amount = round(actual - budget, 2)
                    variance_pct = round((variance_amount / budget) * 100.0, 2)

                    writer.writerow([
                        store_id,
                        m,
                        category,
                        f"{budget:.2f}",
                        f"{actual:.2f}",
                        f"{variance_amount:.2f}",
                        f"{variance_pct:.2f}",
                    ])


def write_profitability_targets() -> None:
    with open(DATA_DIR / "profitability_targets.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["region", "fiscal_year", "target_ebitda_pct", "target_opex_to_sales_pct"])
        for target in PROFITABILITY_TARGETS:
            writer.writerow([
                target["region"],
                target["fiscal_year"],
                f"{target['target_ebitda_pct']:.2f}",
                f"{target['target_opex_to_sales_pct']:.2f}",
            ])


def main() -> None:
    rng = random.Random(42)
    write_stores()
    write_monthly_pnl(rng)
    write_opex_categories(rng)
    write_profitability_targets()
    print(f"Generated 4 seed data CSVs in {DATA_DIR}")


if __name__ == "__main__":
    main()
