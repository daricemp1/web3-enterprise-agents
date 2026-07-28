#!/usr/bin/env python3
"""Generates synthetic seed CSV data for Marketing: Customer Lifecycle & Loyalty agent.

Generates 4 CSV files under domains/marketing/agents/customer_lifecycle_loyalty/data/:
1. customers.csv (customer_id CUST-001..CUST-010, signup_date, primary_store_id STORE-001..STORE-004, loyalty_tier [Bronze, Silver, Gold, Platinum])
2. rfm_segments.csv (customer_id, rfm_segment [Champions, Loyal, At-Risk, Hibernating], recency_days, frequency_score, monetary_value, churn_risk_score; date anchor 2026-07-24)
3. loyalty_tiers.csv (loyalty_tier, tier_member_count, avg_annual_spend, redemption_rate_pct; date anchor 2026-07-24)
4. clv_history.csv (customer_id, fiscal_year 2026, historical_clv, predicted_12m_clv, repeat_purchase_rate)

Usage:
    uv run python domains/marketing/agents/customer_lifecycle_loyalty/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
import datetime
import random
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DATE_ANCHOR = datetime.date(2026, 7, 24)

CUSTOMERS_DATA = [
    {"customer_id": "CUST-001", "signup_date": "2023-01-15", "primary_store_id": "STORE-001", "loyalty_tier": "Platinum"},
    {"customer_id": "CUST-002", "signup_date": "2023-04-22", "primary_store_id": "STORE-001", "loyalty_tier": "Gold"},
    {"customer_id": "CUST-003", "signup_date": "2024-02-10", "primary_store_id": "STORE-002", "loyalty_tier": "Gold"},
    {"customer_id": "CUST-004", "signup_date": "2024-06-05", "primary_store_id": "STORE-002", "loyalty_tier": "Silver"},
    {"customer_id": "CUST-005", "signup_date": "2024-09-18", "primary_store_id": "STORE-003", "loyalty_tier": "Silver"},
    {"customer_id": "CUST-006", "signup_date": "2025-01-11", "primary_store_id": "STORE-003", "loyalty_tier": "Silver"},
    {"customer_id": "CUST-007", "signup_date": "2025-03-30", "primary_store_id": "STORE-004", "loyalty_tier": "Bronze"},
    {"customer_id": "CUST-008", "signup_date": "2025-07-14", "primary_store_id": "STORE-004", "loyalty_tier": "Bronze"},
    {"customer_id": "CUST-009", "signup_date": "2025-11-02", "primary_store_id": "STORE-001", "loyalty_tier": "Bronze"},
    {"customer_id": "CUST-010", "signup_date": "2026-02-20", "primary_store_id": "STORE-002", "loyalty_tier": "Bronze"},
]

RFM_DATA = [
    {"customer_id": "CUST-001", "rfm_segment": "Champions", "recency_days": 4, "frequency_score": 5, "monetary_value": 4850.00, "churn_risk_score": 0.04},
    {"customer_id": "CUST-002", "rfm_segment": "Champions", "recency_days": 7, "frequency_score": 5, "monetary_value": 3120.00, "churn_risk_score": 0.06},
    {"customer_id": "CUST-003", "rfm_segment": "Loyal", "recency_days": 18, "frequency_score": 4, "monetary_value": 2450.00, "churn_risk_score": 0.12},
    {"customer_id": "CUST-004", "rfm_segment": "Loyal", "recency_days": 22, "frequency_score": 4, "monetary_value": 1680.00, "churn_risk_score": 0.15},
    {"customer_id": "CUST-005", "rfm_segment": "Loyal", "recency_days": 28, "frequency_score": 3, "monetary_value": 1250.00, "churn_risk_score": 0.20},
    {"customer_id": "CUST-006", "rfm_segment": "At-Risk", "recency_days": 54, "frequency_score": 2, "monetary_value": 890.00, "churn_risk_score": 0.62},
    {"customer_id": "CUST-007", "rfm_segment": "At-Risk", "recency_days": 68, "frequency_score": 2, "monetary_value": 520.00, "churn_risk_score": 0.71},
    {"customer_id": "CUST-008", "rfm_segment": "Hibernating", "recency_days": 115, "frequency_score": 1, "monetary_value": 340.00, "churn_risk_score": 0.88},
    {"customer_id": "CUST-009", "rfm_segment": "Hibernating", "recency_days": 140, "frequency_score": 1, "monetary_value": 210.00, "churn_risk_score": 0.92},
    {"customer_id": "CUST-010", "rfm_segment": "Loyal", "recency_days": 12, "frequency_score": 3, "monetary_value": 680.00, "churn_risk_score": 0.18},
]

LOYALTY_TIERS_DATA = [
    {"loyalty_tier": "Bronze", "tier_member_count": 12500, "avg_annual_spend": 280.50, "redemption_rate_pct": 18.5},
    {"loyalty_tier": "Silver", "tier_member_count": 5800, "avg_annual_spend": 720.00, "redemption_rate_pct": 36.2},
    {"loyalty_tier": "Gold", "tier_member_count": 2400, "avg_annual_spend": 1650.00, "redemption_rate_pct": 59.8},
    {"loyalty_tier": "Platinum", "tier_member_count": 650, "avg_annual_spend": 4200.00, "redemption_rate_pct": 81.4},
]

CLV_DATA = [
    {"customer_id": "CUST-001", "fiscal_year": 2026, "historical_clv": 5200.00, "predicted_12m_clv": 2400.00, "repeat_purchase_rate": 0.92},
    {"customer_id": "CUST-002", "fiscal_year": 2026, "historical_clv": 3400.00, "predicted_12m_clv": 1650.00, "repeat_purchase_rate": 0.85},
    {"customer_id": "CUST-003", "fiscal_year": 2026, "historical_clv": 2600.00, "predicted_12m_clv": 1300.00, "repeat_purchase_rate": 0.78},
    {"customer_id": "CUST-004", "fiscal_year": 2026, "historical_clv": 1800.00, "predicted_12m_clv": 950.00, "repeat_purchase_rate": 0.72},
    {"customer_id": "CUST-005", "fiscal_year": 2026, "historical_clv": 1350.00, "predicted_12m_clv": 720.00, "repeat_purchase_rate": 0.65},
    {"customer_id": "CUST-006", "fiscal_year": 2026, "historical_clv": 920.00, "predicted_12m_clv": 310.00, "repeat_purchase_rate": 0.42},
    {"customer_id": "CUST-007", "fiscal_year": 2026, "historical_clv": 560.00, "predicted_12m_clv": 180.00, "repeat_purchase_rate": 0.35},
    {"customer_id": "CUST-008", "fiscal_year": 2026, "historical_clv": 380.00, "predicted_12m_clv": 85.00, "repeat_purchase_rate": 0.22},
    {"customer_id": "CUST-009", "fiscal_year": 2026, "historical_clv": 230.00, "predicted_12m_clv": 45.00, "repeat_purchase_rate": 0.18},
    {"customer_id": "CUST-010", "fiscal_year": 2026, "historical_clv": 710.00, "predicted_12m_clv": 520.00, "repeat_purchase_rate": 0.60},
]


def write_customers() -> None:
    with open(DATA_DIR / "customers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "signup_date", "primary_store_id", "loyalty_tier"])
        for c in CUSTOMERS_DATA:
            writer.writerow([c["customer_id"], c["signup_date"], c["primary_store_id"], c["loyalty_tier"]])


def write_rfm_segments() -> None:
    with open(DATA_DIR / "rfm_segments.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "rfm_segment", "recency_days", "frequency_score", "monetary_value", "churn_risk_score"])
        for r in RFM_DATA:
            writer.writerow([
                r["customer_id"],
                r["rfm_segment"],
                r["recency_days"],
                r["frequency_score"],
                f"{r['monetary_value']:.2f}",
                f"{r['churn_risk_score']:.2f}",
            ])


def write_loyalty_tiers() -> None:
    with open(DATA_DIR / "loyalty_tiers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["loyalty_tier", "tier_member_count", "avg_annual_spend", "redemption_rate_pct"])
        for lt in LOYALTY_TIERS_DATA:
            writer.writerow([
                lt["loyalty_tier"],
                lt["tier_member_count"],
                f"{lt['avg_annual_spend']:.2f}",
                f"{lt['redemption_rate_pct']:.1f}",
            ])


def write_clv_history() -> None:
    with open(DATA_DIR / "clv_history.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "fiscal_year", "historical_clv", "predicted_12m_clv", "repeat_purchase_rate"])
        for clv in CLV_DATA:
            writer.writerow([
                clv["customer_id"],
                clv["fiscal_year"],
                f"{clv['historical_clv']:.2f}",
                f"{clv['predicted_12m_clv']:.2f}",
                f"{clv['repeat_purchase_rate']:.2f}",
            ])


def main() -> None:
    write_customers()
    write_rfm_segments()
    write_loyalty_tiers()
    write_clv_history()
    print(f"Generated 4 seed data CSVs in {DATA_DIR}")


if __name__ == "__main__":
    main()
