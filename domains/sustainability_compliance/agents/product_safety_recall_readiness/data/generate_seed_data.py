#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Product Safety & Recall Execution agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

RECALL_NOTICES = [
    {"recall_id": "REC-2026-01", "sku": "SKU-005", "product_name": "EnergyStar Compact Smart Air Purifier", "cpsc_fda_recall_number": "CPSC-26-088", "announcement_date": "2026-04-10", "hazard_description": "Capacitor overheating risk in batch 2026A", "recall_classification": "Class II - Consumer Product", "affected_lot_numbers": "LOT-2026A-01 through LOT-2026A-08"},
    {"recall_id": "REC-2026-02", "sku": "SKU-003", "product_name": "Biodegradable Bamboo Kitchenware Set", "cpsc_fda_recall_number": "FDA-F-26-112", "announcement_date": "2026-05-18", "hazard_description": "Melamine resin migration above statutory limits", "recall_classification": "Class II - Food Contact Material", "affected_lot_numbers": "LOT-BAM-2025Q4"},
]

QUARANTINE_LOGS = [
    {"recall_id": "REC-2026-01", "store_id": "STORE-101", "quarantine_notice_timestamp": "2026-04-10 08:00:00", "shelf_cleared_timestamp": "2026-04-10 11:30:00", "units_quarantined": 34, "execution_time_hours": 3.5, "quarantine_verified_by": "Store Ops Lead A. Martinez"},
    {"recall_id": "REC-2026-01", "store_id": "STORE-102", "quarantine_notice_timestamp": "2026-04-10 08:00:00", "shelf_cleared_timestamp": "2026-04-10 12:15:00", "units_quarantined": 42, "execution_time_hours": 4.25, "quarantine_verified_by": "Store Ops Lead R. Jenkins"},
    {"recall_id": "REC-2026-01", "store_id": "STORE-103", "quarantine_notice_timestamp": "2026-04-10 08:00:00", "shelf_cleared_timestamp": "2026-04-10 11:00:00", "units_quarantined": 28, "execution_time_hours": 3.0, "quarantine_verified_by": "Store Ops Lead K. Nguyen"},
    {"recall_id": "REC-2026-01", "store_id": "STORE-104", "quarantine_notice_timestamp": "2026-04-10 08:00:00", "shelf_cleared_timestamp": "2026-04-10 13:00:00", "units_quarantined": 38, "execution_time_hours": 5.0, "quarantine_verified_by": "Store Ops Lead D. Washington"},
    {"recall_id": "REC-2026-01", "store_id": "STORE-105", "quarantine_notice_timestamp": "2026-04-10 08:00:00", "shelf_cleared_timestamp": "2026-04-10 12:45:00", "units_quarantined": 30, "execution_time_hours": 4.75, "quarantine_verified_by": "Store Ops Lead L. Sullivan"},
    {"recall_id": "REC-2026-02", "store_id": "STORE-101", "quarantine_notice_timestamp": "2026-05-18 09:00:00", "shelf_cleared_timestamp": "2026-05-18 12:00:00", "units_quarantined": 65, "execution_time_hours": 3.0, "quarantine_verified_by": "Store Ops Lead A. Martinez"},
    {"recall_id": "REC-2026-02", "store_id": "STORE-102", "quarantine_notice_timestamp": "2026-05-18 09:00:00", "shelf_cleared_timestamp": "2026-05-18 12:30:00", "units_quarantined": 72, "execution_time_hours": 3.5, "quarantine_verified_by": "Store Ops Lead R. Jenkins"},
    {"recall_id": "REC-2026-02", "store_id": "STORE-103", "quarantine_notice_timestamp": "2026-05-18 09:00:00", "shelf_cleared_timestamp": "2026-05-18 11:45:00", "units_quarantined": 58, "execution_time_hours": 2.75, "quarantine_verified_by": "Store Ops Lead K. Nguyen"},
    {"recall_id": "REC-2026-02", "store_id": "STORE-104", "quarantine_notice_timestamp": "2026-05-18 09:00:00", "shelf_cleared_timestamp": "2026-05-18 13:15:00", "units_quarantined": 80, "execution_time_hours": 4.25, "quarantine_verified_by": "Store Ops Lead D. Washington"},
    {"recall_id": "REC-2026-02", "store_id": "STORE-105", "quarantine_notice_timestamp": "2026-05-18 09:00:00", "shelf_cleared_timestamp": "2026-05-18 12:15:00", "units_quarantined": 60, "execution_time_hours": 3.25, "quarantine_verified_by": "Store Ops Lead L. Sullivan"},
]

CUSTOMER_NOTIFICATIONS = [
    {"recall_id": "REC-2026-01", "notification_channel": "Direct Email", "total_customers_contacted": 3450, "notification_sent_date": "2026-04-11", "open_read_rate_pct": 78.5, "refund_claim_count": 2180, "total_refunded_usd": 174400.00},
    {"recall_id": "REC-2026-01", "notification_channel": "SMS Alert", "total_customers_contacted": 2890, "notification_sent_date": "2026-04-11", "open_read_rate_pct": 92.4, "refund_claim_count": 1840, "total_refunded_usd": 147200.00},
    {"recall_id": "REC-2026-01", "notification_channel": "Mobile App Push", "total_customers_contacted": 4120, "notification_sent_date": "2026-04-11", "open_read_rate_pct": 84.1, "refund_claim_count": 2650, "total_refunded_usd": 212000.00},
    {"recall_id": "REC-2026-02", "notification_channel": "Direct Email", "total_customers_contacted": 5200, "notification_sent_date": "2026-05-19", "open_read_rate_pct": 74.2, "refund_claim_count": 3100, "total_refunded_usd": 77500.00},
    {"recall_id": "REC-2026-02", "notification_channel": "SMS Alert", "total_customers_contacted": 4400, "notification_sent_date": "2026-05-19", "open_read_rate_pct": 89.8, "refund_claim_count": 2850, "total_refunded_usd": 71250.00},
]

DESTRUCTION_LOGS = [
    {"recall_id": "REC-2026-01", "facility_id": "DC-101", "disposition_method": "Certified E-Waste Recycling & Shredding", "total_units_destroyed": 1450, "destruction_cert_date": "2026-05-15", "certified_vendor": "CleanLytx Eco-Recycling Corp", "salvage_recovery_usd": 8700.00},
    {"recall_id": "REC-2026-01", "facility_id": "DC-102", "disposition_method": "Certified E-Waste Recycling & Shredding", "total_units_destroyed": 980, "destruction_cert_date": "2026-05-18", "certified_vendor": "CleanLytx Eco-Recycling Corp", "salvage_recovery_usd": 5880.00},
    {"recall_id": "REC-2026-02", "facility_id": "DC-101", "disposition_method": "Industrial Fiber Composting & Thermal Incineration", "total_units_destroyed": 2200, "destruction_cert_date": "2026-06-20", "certified_vendor": "EnviroSafe Waste Disposal Inc", "salvage_recovery_usd": 0.00},
    {"recall_id": "REC-2026-02", "facility_id": "DC-102", "disposition_method": "Industrial Fiber Composting & Thermal Incineration", "total_units_destroyed": 1650, "destruction_cert_date": "2026-06-22", "certified_vendor": "EnviroSafe Waste Disposal Inc", "salvage_recovery_usd": 0.00},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(RECALL_NOTICES, "regulatory_recall_notices.csv")
    generate_csv(QUARANTINE_LOGS, "store_quarantine_execution.csv")
    generate_csv(CUSTOMER_NOTIFICATIONS, "customer_notification_reach.csv")
    generate_csv(DESTRUCTION_LOGS, "disposition_destruction_logs.csv")

if __name__ == "__main__":
    main()
