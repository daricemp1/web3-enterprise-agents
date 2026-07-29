#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for Finance: Working Capital & Cash Flow agent.

Generates 4 CSV files under domains/finance/agents/working_capital_cashflow/data/:
1. cash_conversion_cycle.csv (fiscal_month, days_sales_outstanding_dso, days_inventory_outstanding_dio, days_payable_outstanding_dpo, cash_conversion_cycle_days, operating_cash_flow_dollars)
2. accounts_receivable_aging.csv (customer_account_id, customer_name, current_balance, aging_1_30_days, aging_31_60_days, aging_61_90_days, aging_over_90_days, bad_debt_risk_flag)
3. accounts_payable_aging.csv (vendor_id, vendor_name, payment_terms, current_due, aging_1_30_days, aging_31_60_days, aging_over_90_days, early_discount_eligible_dollars)
4. liquidity_forecast.csv (forecast_date, opening_cash_balance, projected_ar_collections, projected_ap_disbursements, projected_payroll_opex, closing_cash_balance)

Usage:
    uv run python domains/finance/agents/working_capital_cashflow/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
WINDOW_END = datetime.date(2026, 7, 24)

CASH_CONVERSION_CYCLE_DATA = [
    {
        "fiscal_month": "2026-01",
        "days_sales_outstanding_dso": 38.5,
        "days_inventory_outstanding_dio": 45.2,
        "days_payable_outstanding_dpo": 42.0,
        "cash_conversion_cycle_days": 41.7,
        "operating_cash_flow_dollars": 1250000.00,
    },
    {
        "fiscal_month": "2026-02",
        "days_sales_outstanding_dso": 39.1,
        "days_inventory_outstanding_dio": 44.8,
        "days_payable_outstanding_dpo": 41.5,
        "cash_conversion_cycle_days": 42.4,
        "operating_cash_flow_dollars": 1180000.00,
    },
    {
        "fiscal_month": "2026-03",
        "days_sales_outstanding_dso": 37.8,
        "days_inventory_outstanding_dio": 43.5,
        "days_payable_outstanding_dpo": 43.0,
        "cash_conversion_cycle_days": 38.3,
        "operating_cash_flow_dollars": 1420000.00,
    },
    {
        "fiscal_month": "2026-04",
        "days_sales_outstanding_dso": 36.5,
        "days_inventory_outstanding_dio": 42.0,
        "days_payable_outstanding_dpo": 44.0,
        "cash_conversion_cycle_days": 34.5,
        "operating_cash_flow_dollars": 1550000.00,
    },
    {
        "fiscal_month": "2026-05",
        "days_sales_outstanding_dso": 35.8,
        "days_inventory_outstanding_dio": 41.2,
        "days_payable_outstanding_dpo": 43.5,
        "cash_conversion_cycle_days": 33.5,
        "operating_cash_flow_dollars": 1680000.00,
    },
    {
        "fiscal_month": "2026-06",
        "days_sales_outstanding_dso": 35.0,
        "days_inventory_outstanding_dio": 40.5,
        "days_payable_outstanding_dpo": 45.0,
        "cash_conversion_cycle_days": 30.5,
        "operating_cash_flow_dollars": 1820000.00,
    },
]

AR_AGING_DATA = [
    {
        "customer_account_id": "CUST-101",
        "customer_name": "Apex Retail Group",
        "current_balance": 45000.00,
        "aging_1_30_days": 30000.00,
        "aging_31_60_days": 15000.00,
        "aging_61_90_days": 0.00,
        "aging_over_90_days": 0.00,
        "bad_debt_risk_flag": False,
    },
    {
        "customer_account_id": "CUST-102",
        "customer_name": "Summit Department Stores",
        "current_balance": 120000.00,
        "aging_1_30_days": 50000.00,
        "aging_31_60_days": 40000.00,
        "aging_61_90_days": 20000.00,
        "aging_over_90_days": 10000.00,
        "bad_debt_risk_flag": True,
    },
    {
        "customer_account_id": "CUST-103",
        "customer_name": "Beacon Superstores",
        "current_balance": 85000.00,
        "aging_1_30_days": 60000.00,
        "aging_31_60_days": 25000.00,
        "aging_61_90_days": 0.00,
        "aging_over_90_days": 0.00,
        "bad_debt_risk_flag": False,
    },
    {
        "customer_account_id": "CUST-104",
        "customer_name": "Cascade Outlets",
        "current_balance": 32000.00,
        "aging_1_30_days": 20000.00,
        "aging_31_60_days": 8000.00,
        "aging_61_90_days": 4000.00,
        "aging_over_90_days": 0.00,
        "bad_debt_risk_flag": False,
    },
    {
        "customer_account_id": "CUST-105",
        "customer_name": "Metro Hypermarket",
        "current_balance": 150000.00,
        "aging_1_30_days": 90000.00,
        "aging_31_60_days": 40000.00,
        "aging_61_90_days": 20000.00,
        "aging_over_90_days": 0.00,
        "bad_debt_risk_flag": False,
    },
    {
        "customer_account_id": "CUST-106",
        "customer_name": "Pinnacle Boutiques",
        "current_balance": 28000.00,
        "aging_1_30_days": 5000.00,
        "aging_31_60_days": 8000.00,
        "aging_61_90_days": 10000.00,
        "aging_over_90_days": 5000.00,
        "bad_debt_risk_flag": True,
    },
    {
        "customer_account_id": "CUST-107",
        "customer_name": "Urban Trends Co",
        "current_balance": 64000.00,
        "aging_1_30_days": 44000.00,
        "aging_31_60_days": 20000.00,
        "aging_61_90_days": 0.00,
        "aging_over_90_days": 0.00,
        "bad_debt_risk_flag": False,
    },
    {
        "customer_account_id": "CUST-108",
        "customer_name": "Horizon Retailers",
        "current_balance": 95000.00,
        "aging_1_30_days": 55000.00,
        "aging_31_60_days": 25000.00,
        "aging_61_90_days": 10000.00,
        "aging_over_90_days": 5000.00,
        "bad_debt_risk_flag": False,
    },
]

AP_AGING_DATA = [
    {
        "vendor_id": "VND-001",
        "vendor_name": "Apex Apparel",
        "payment_terms": "Net 60",
        "current_due": 75000.00,
        "aging_1_30_days": 45000.00,
        "aging_31_60_days": 30000.00,
        "aging_over_90_days": 0.00,
        "early_discount_eligible_dollars": 0.00,
    },
    {
        "vendor_id": "VND-002",
        "vendor_name": "Summit Outdoor",
        "payment_terms": "2/10 Net 30",
        "current_due": 110000.00,
        "aging_1_30_days": 80000.00,
        "aging_31_60_days": 30000.00,
        "aging_over_90_days": 0.00,
        "early_discount_eligible_dollars": 50000.00,
    },
    {
        "vendor_id": "VND-003",
        "vendor_name": "Cascade Gear",
        "payment_terms": "Net 30",
        "current_due": 52000.00,
        "aging_1_30_days": 35000.00,
        "aging_31_60_days": 17000.00,
        "aging_over_90_days": 0.00,
        "early_discount_eligible_dollars": 0.00,
    },
    {
        "vendor_id": "VND-004",
        "vendor_name": "Alpine Tech",
        "payment_terms": "2/10 Net 30",
        "current_due": 98000.00,
        "aging_1_30_days": 68000.00,
        "aging_31_60_days": 20000.00,
        "aging_over_90_days": 10000.00,
        "early_discount_eligible_dollars": 40000.00,
    },
    {
        "vendor_id": "VND-005",
        "vendor_name": "Pacific Threads",
        "payment_terms": "Net 30",
        "current_due": 44000.00,
        "aging_1_30_days": 30000.00,
        "aging_31_60_days": 14000.00,
        "aging_over_90_days": 0.00,
        "early_discount_eligible_dollars": 0.00,
    },
    {
        "vendor_id": "VND-006",
        "vendor_name": "Global Logistics Ltd",
        "payment_terms": "Net 15",
        "current_due": 65000.00,
        "aging_1_30_days": 45000.00,
        "aging_31_60_days": 15000.00,
        "aging_over_90_days": 5000.00,
        "early_discount_eligible_dollars": 0.00,
    },
]

LIQUIDITY_FORECAST_DATA = [
    {
        "forecast_date": "2026-07-24",
        "opening_cash_balance": 5000000.00,
        "projected_ar_collections": 850000.00,
        "projected_ap_disbursements": 620000.00,
        "projected_payroll_opex": 350000.00,
        "closing_cash_balance": 4880000.00,
    },
    {
        "forecast_date": "2026-07-31",
        "opening_cash_balance": 4880000.00,
        "projected_ar_collections": 920000.00,
        "projected_ap_disbursements": 580000.00,
        "projected_payroll_opex": 200000.00,
        "closing_cash_balance": 5020000.00,
    },
    {
        "forecast_date": "2026-08-07",
        "opening_cash_balance": 5020000.00,
        "projected_ar_collections": 780000.00,
        "projected_ap_disbursements": 710000.00,
        "projected_payroll_opex": 360000.00,
        "closing_cash_balance": 4730000.00,
    },
    {
        "forecast_date": "2026-08-14",
        "opening_cash_balance": 4730000.00,
        "projected_ar_collections": 890000.00,
        "projected_ap_disbursements": 640000.00,
        "projected_payroll_opex": 210000.00,
        "closing_cash_balance": 4770000.00,
    },
    {
        "forecast_date": "2026-08-21",
        "opening_cash_balance": 4770000.00,
        "projected_ar_collections": 950000.00,
        "projected_ap_disbursements": 690000.00,
        "projected_payroll_opex": 370000.00,
        "closing_cash_balance": 4660000.00,
    },
    {
        "forecast_date": "2026-08-28",
        "opening_cash_balance": 4660000.00,
        "projected_ar_collections": 910000.00,
        "projected_ap_disbursements": 600000.00,
        "projected_payroll_opex": 220000.00,
        "closing_cash_balance": 4750000.00,
    },
]


def write_cash_conversion_cycle() -> None:
    with open(DATA_DIR / "cash_conversion_cycle.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "fiscal_month",
            "days_sales_outstanding_dso",
            "days_inventory_outstanding_dio",
            "days_payable_outstanding_dpo",
            "cash_conversion_cycle_days",
            "operating_cash_flow_dollars",
        ])
        for row in CASH_CONVERSION_CYCLE_DATA:
            writer.writerow([
                row["fiscal_month"],
                f"{row['days_sales_outstanding_dso']:.1f}",
                f"{row['days_inventory_outstanding_dio']:.1f}",
                f"{row['days_payable_outstanding_dpo']:.1f}",
                f"{row['cash_conversion_cycle_days']:.1f}",
                f"{row['operating_cash_flow_dollars']:.2f}",
            ])


def write_accounts_receivable_aging() -> None:
    with open(DATA_DIR / "accounts_receivable_aging.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "customer_account_id",
            "customer_name",
            "current_balance",
            "aging_1_30_days",
            "aging_31_60_days",
            "aging_61_90_days",
            "aging_over_90_days",
            "bad_debt_risk_flag",
        ])
        for row in AR_AGING_DATA:
            writer.writerow([
                row["customer_account_id"],
                row["customer_name"],
                f"{row['current_balance']:.2f}",
                f"{row['aging_1_30_days']:.2f}",
                f"{row['aging_31_60_days']:.2f}",
                f"{row['aging_61_90_days']:.2f}",
                f"{row['aging_over_90_days']:.2f}",
                str(row["bad_debt_risk_flag"]).upper(),
            ])


def write_accounts_payable_aging() -> None:
    with open(DATA_DIR / "accounts_payable_aging.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "vendor_id",
            "vendor_name",
            "payment_terms",
            "current_due",
            "aging_1_30_days",
            "aging_31_60_days",
            "aging_over_90_days",
            "early_discount_eligible_dollars",
        ])
        for row in AP_AGING_DATA:
            writer.writerow([
                row["vendor_id"],
                row["vendor_name"],
                row["payment_terms"],
                f"{row['current_due']:.2f}",
                f"{row['aging_1_30_days']:.2f}",
                f"{row['aging_31_60_days']:.2f}",
                f"{row['aging_over_90_days']:.2f}",
                f"{row['early_discount_eligible_dollars']:.2f}",
            ])


def write_liquidity_forecast() -> None:
    with open(DATA_DIR / "liquidity_forecast.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "forecast_date",
            "opening_cash_balance",
            "projected_ar_collections",
            "projected_ap_disbursements",
            "projected_payroll_opex",
            "closing_cash_balance",
        ])
        for row in LIQUIDITY_FORECAST_DATA:
            writer.writerow([
                row["forecast_date"],
                f"{row['opening_cash_balance']:.2f}",
                f"{row['projected_ar_collections']:.2f}",
                f"{row['projected_ap_disbursements']:.2f}",
                f"{row['projected_payroll_opex']:.2f}",
                f"{row['closing_cash_balance']:.2f}",
            ])


def main() -> None:
    write_cash_conversion_cycle()
    write_accounts_receivable_aging()
    write_accounts_payable_aging()
    write_liquidity_forecast()
    print(f"Generated 4 seed CSV files in {DATA_DIR}")


if __name__ == "__main__":
    main()
