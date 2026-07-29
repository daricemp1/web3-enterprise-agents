#!/usr/bin/env python3
"""Generates synthetic BigQuery seed data (data/*.csv) for the Returns & Reverse Logistics agent.

Anchors date windows around WINDOW_END = '2026-07-24' and uses standard CSV module.
"""
from __future__ import annotations

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

STORES_CHANNELS = [
    {
        "channel_id": "CHN-001",
        "channel_name": "E-Commerce Storefront",
        "channel_type": "Online",
        "region": "National",
        "channel_manager": "Sarah Jenkins",
    },
    {
        "channel_id": "CHN-002",
        "channel_name": "Midwest Flagship Stores",
        "channel_type": "Retail Store",
        "region": "Midwest",
        "channel_manager": "David Miller",
    },
    {
        "channel_id": "CHN-003",
        "channel_name": "South Regional Outlets",
        "channel_type": "Retail Store",
        "region": "South",
        "channel_manager": "Amanda Vance",
    },
    {
        "channel_id": "CHN-004",
        "channel_name": "West Coast Boutique",
        "channel_type": "Retail Store",
        "region": "West",
        "channel_manager": "Carlos Gomez",
    },
    {
        "channel_id": "CHN-005",
        "channel_name": "App Mobile Application",
        "channel_type": "Mobile",
        "region": "National",
        "channel_manager": "Elena Rostova",
    },
]

RETURNS_MONTHLY = [
    # 2026-05
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-05",
        "gross_sales_units": 40000,
        "returned_units": 7600,
        "returned_value_dollars": 380000.00,
        "return_rate_pct": 19.0,
        "avg_restock_turnaround_days": 7.2,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-05",
        "gross_sales_units": 30000,
        "returned_units": 2550,
        "returned_value_dollars": 114750.00,
        "return_rate_pct": 8.5,
        "avg_restock_turnaround_days": 2.3,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-05",
        "gross_sales_units": 26000,
        "returned_units": 2600,
        "returned_value_dollars": 117000.00,
        "return_rate_pct": 10.0,
        "avg_restock_turnaround_days": 2.6,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-05",
        "gross_sales_units": 20000,
        "returned_units": 1500,
        "returned_value_dollars": 75000.00,
        "return_rate_pct": 7.5,
        "avg_restock_turnaround_days": 2.0,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-05",
        "gross_sales_units": 34000,
        "returned_units": 5780,
        "returned_value_dollars": 260100.00,
        "return_rate_pct": 17.0,
        "avg_restock_turnaround_days": 6.1,
    },
    # 2026-06
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-06",
        "gross_sales_units": 42000,
        "returned_units": 8400,
        "returned_value_dollars": 420000.00,
        "return_rate_pct": 20.0,
        "avg_restock_turnaround_days": 6.8,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-06",
        "gross_sales_units": 31000,
        "returned_units": 2728,
        "returned_value_dollars": 122760.00,
        "return_rate_pct": 8.8,
        "avg_restock_turnaround_days": 2.2,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-06",
        "gross_sales_units": 27000,
        "returned_units": 2754,
        "returned_value_dollars": 123930.00,
        "return_rate_pct": 10.2,
        "avg_restock_turnaround_days": 2.5,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-06",
        "gross_sales_units": 21000,
        "returned_units": 1638,
        "returned_value_dollars": 81900.00,
        "return_rate_pct": 7.8,
        "avg_restock_turnaround_days": 1.9,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-06",
        "gross_sales_units": 36000,
        "returned_units": 6300,
        "returned_value_dollars": 283500.00,
        "return_rate_pct": 17.5,
        "avg_restock_turnaround_days": 5.9,
    },
    # 2026-07
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "gross_sales_units": 45000,
        "returned_units": 9450,
        "returned_value_dollars": 472500.00,
        "return_rate_pct": 21.0,
        "avg_restock_turnaround_days": 6.5,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "gross_sales_units": 32000,
        "returned_units": 2880,
        "returned_value_dollars": 129600.00,
        "return_rate_pct": 9.0,
        "avg_restock_turnaround_days": 2.1,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-07",
        "gross_sales_units": 28000,
        "returned_units": 2940,
        "returned_value_dollars": 132300.00,
        "return_rate_pct": 10.5,
        "avg_restock_turnaround_days": 2.4,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-07",
        "gross_sales_units": 22000,
        "returned_units": 1760,
        "returned_value_dollars": 88000.00,
        "return_rate_pct": 8.0,
        "avg_restock_turnaround_days": 1.8,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "gross_sales_units": 38000,
        "returned_units": 6840,
        "returned_value_dollars": 307800.00,
        "return_rate_pct": 18.0,
        "avg_restock_turnaround_days": 5.8,
    },
]

RETURN_REASONS = [
    # 2026-07
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "category": "Apparel",
        "return_reason": "Wrong Size",
        "units_returned": 4200,
        "return_cost_dollars": 210000.00,
    },
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "category": "Apparel",
        "return_reason": "Item Not as Pictured",
        "units_returned": 2100,
        "return_cost_dollars": 105000.00,
    },
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "category": "Footwear",
        "return_reason": "Wrong Size",
        "units_returned": 1800,
        "return_cost_dollars": 108000.00,
    },
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "category": "Electronics",
        "return_reason": "Defective/Damaged",
        "units_returned": 1350,
        "return_cost_dollars": 135000.00,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "category": "Apparel",
        "return_reason": "Wrong Size",
        "units_returned": 1200,
        "return_cost_dollars": 54000.00,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "category": "Home Goods",
        "return_reason": "Buyer Remorse",
        "units_returned": 850,
        "return_cost_dollars": 34000.00,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "category": "Electronics",
        "return_reason": "Defective/Damaged",
        "units_returned": 830,
        "return_cost_dollars": 41500.00,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-07",
        "category": "Apparel",
        "return_reason": "Wrong Size",
        "units_returned": 1400,
        "return_cost_dollars": 63000.00,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-07",
        "category": "Footwear",
        "return_reason": "Buyer Remorse",
        "units_returned": 940,
        "return_cost_dollars": 47000.00,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-07",
        "category": "Apparel",
        "return_reason": "Wrong Size",
        "units_returned": 900,
        "return_cost_dollars": 45000.00,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-07",
        "category": "Home Goods",
        "return_reason": "Defective/Damaged",
        "units_returned": 860,
        "return_cost_dollars": 43000.00,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "category": "Apparel",
        "return_reason": "Wrong Size",
        "units_returned": 3100,
        "return_cost_dollars": 139500.00,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "category": "Electronics",
        "return_reason": "Defective/Damaged",
        "units_returned": 1900,
        "return_cost_dollars": 114000.00,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "category": "Footwear",
        "return_reason": "Item Not as Pictured",
        "units_returned": 1840,
        "return_cost_dollars": 92000.00,
    },
]

REVERSE_DISPOSITION = [
    # 2026-07
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "disposition_type": "Restock for Resale",
        "units_count": 5200,
        "recovered_value_dollars": 260000.00,
        "policy_abuse_flag_count": 45,
    },
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "disposition_type": "Refurbish/Repair",
        "units_count": 1800,
        "recovered_value_dollars": 72000.00,
        "policy_abuse_flag_count": 12,
    },
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "disposition_type": "Liquidation/Jobber",
        "units_count": 1400,
        "recovered_value_dollars": 28000.00,
        "policy_abuse_flag_count": 8,
    },
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "disposition_type": "Recycle/Scrap",
        "units_count": 650,
        "recovered_value_dollars": 0.00,
        "policy_abuse_flag_count": 3,
    },
    {
        "channel_id": "CHN-001",
        "fiscal_month": "2026-07",
        "disposition_type": "Return to Vendor (RTV)",
        "units_count": 400,
        "recovered_value_dollars": 20000.00,
        "policy_abuse_flag_count": 2,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "disposition_type": "Restock for Resale",
        "units_count": 2100,
        "recovered_value_dollars": 94500.00,
        "policy_abuse_flag_count": 15,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "disposition_type": "Refurbish/Repair",
        "units_count": 450,
        "recovered_value_dollars": 18000.00,
        "policy_abuse_flag_count": 4,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "disposition_type": "Liquidation/Jobber",
        "units_count": 230,
        "recovered_value_dollars": 4600.00,
        "policy_abuse_flag_count": 2,
    },
    {
        "channel_id": "CHN-002",
        "fiscal_month": "2026-07",
        "disposition_type": "Recycle/Scrap",
        "units_count": 100,
        "recovered_value_dollars": 0.00,
        "policy_abuse_flag_count": 0,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-07",
        "disposition_type": "Restock for Resale",
        "units_count": 2150,
        "recovered_value_dollars": 96750.00,
        "policy_abuse_flag_count": 18,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-07",
        "disposition_type": "Refurbish/Repair",
        "units_count": 500,
        "recovered_value_dollars": 20000.00,
        "policy_abuse_flag_count": 5,
    },
    {
        "channel_id": "CHN-003",
        "fiscal_month": "2026-07",
        "disposition_type": "Liquidation/Jobber",
        "units_count": 200,
        "recovered_value_dollars": 4000.00,
        "policy_abuse_flag_count": 1,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-07",
        "disposition_type": "Restock for Resale",
        "units_count": 1300,
        "recovered_value_dollars": 65000.00,
        "policy_abuse_flag_count": 8,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-07",
        "disposition_type": "Refurbish/Repair",
        "units_count": 300,
        "recovered_value_dollars": 12000.00,
        "policy_abuse_flag_count": 2,
    },
    {
        "channel_id": "CHN-004",
        "fiscal_month": "2026-07",
        "disposition_type": "Liquidation/Jobber",
        "units_count": 160,
        "recovered_value_dollars": 3200.00,
        "policy_abuse_flag_count": 1,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "disposition_type": "Restock for Resale",
        "units_count": 4100,
        "recovered_value_dollars": 184500.00,
        "policy_abuse_flag_count": 32,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "disposition_type": "Refurbish/Repair",
        "units_count": 1500,
        "recovered_value_dollars": 60000.00,
        "policy_abuse_flag_count": 10,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "disposition_type": "Liquidation/Jobber",
        "units_count": 840,
        "recovered_value_dollars": 16800.00,
        "policy_abuse_flag_count": 5,
    },
    {
        "channel_id": "CHN-005",
        "fiscal_month": "2026-07",
        "disposition_type": "Recycle/Scrap",
        "units_count": 400,
        "recovered_value_dollars": 0.00,
        "policy_abuse_flag_count": 2,
    },
]


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]) -> None:
    filepath = DATA_DIR / filename
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    write_csv(
        "stores_channels.csv",
        [
            "channel_id",
            "channel_name",
            "channel_type",
            "region",
            "channel_manager",
        ],
        STORES_CHANNELS,
    )
    write_csv(
        "returns_monthly.csv",
        [
            "channel_id",
            "fiscal_month",
            "gross_sales_units",
            "returned_units",
            "returned_value_dollars",
            "return_rate_pct",
            "avg_restock_turnaround_days",
        ],
        RETURNS_MONTHLY,
    )
    write_csv(
        "return_reasons.csv",
        [
            "channel_id",
            "fiscal_month",
            "category",
            "return_reason",
            "units_returned",
            "return_cost_dollars",
        ],
        RETURN_REASONS,
    )
    write_csv(
        "reverse_disposition.csv",
        [
            "channel_id",
            "fiscal_month",
            "disposition_type",
            "units_count",
            "recovered_value_dollars",
            "policy_abuse_flag_count",
        ],
        REVERSE_DISPOSITION,
    )
    print(f"Generated 4 seed data CSV files in {DATA_DIR}")


if __name__ == "__main__":
    main()
