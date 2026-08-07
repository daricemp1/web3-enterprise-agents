#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Extended Producer Responsibility (EPR) & Resale agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

EPR_FEES = [
    {"state_or_jurisdiction": "California (SB 54)", "fiscal_quarter": "2026-Q1", "packaging_category": "Rigid Plastic Containers", "total_weight_tons": 450.0, "epr_rate_per_ton_usd": 185.00, "total_fee_assessed_usd": 83250.00, "compliance_filing_status": "Submitted & Paid"},
    {"state_or_jurisdiction": "California (SB 54)", "fiscal_quarter": "2026-Q1", "packaging_category": "Flexible Film & Polybags", "total_weight_tons": 280.0, "epr_rate_per_ton_usd": 240.00, "total_fee_assessed_usd": 67200.00, "compliance_filing_status": "Submitted & Paid"},
    {"state_or_jurisdiction": "California (SB 54)", "fiscal_quarter": "2026-Q1", "packaging_category": "Paper Corrugate & Boxboard", "total_weight_tons": 1250.0, "epr_rate_per_ton_usd": 45.00, "total_fee_assessed_usd": 56250.00, "compliance_filing_status": "Submitted & Paid"},
    {"state_or_jurisdiction": "Colorado (HB 22-1355)", "fiscal_quarter": "2026-Q1", "packaging_category": "All Packaging Substrates", "total_weight_tons": 680.0, "epr_rate_per_ton_usd": 92.00, "total_fee_assessed_usd": 62560.00, "compliance_filing_status": "Submitted & Paid"},
    {"state_or_jurisdiction": "Oregon (RPA SB 582)", "fiscal_quarter": "2026-Q1", "packaging_category": "Plastic Packaging & Paper", "total_weight_tons": 540.0, "epr_rate_per_ton_usd": 115.00, "total_fee_assessed_usd": 62100.00, "compliance_filing_status": "Submitted & Paid"},
    {"state_or_jurisdiction": "Maine (LD 1541)", "fiscal_quarter": "2026-Q1", "packaging_category": "Municipal Solid Waste Packaging", "total_weight_tons": 310.0, "epr_rate_per_ton_usd": 128.00, "total_fee_assessed_usd": 39680.00, "compliance_filing_status": "Submitted & Paid"},
]

TAKE_BACK = [
    {"program_name": "Garment Circularity Loop", "month": "2026-01", "collection_channel": "Store Drop-off Bin", "product_category": "Apparel & Footwear", "weight_collected_lbs": 14500.0, "processed_for_recycling_lbs": 13800.0, "customer_voucher_rewards_usd": 7250.00},
    {"program_name": "Garment Circularity Loop", "month": "2026-02", "collection_channel": "Store Drop-off Bin", "product_category": "Apparel & Footwear", "weight_collected_lbs": 15800.0, "processed_for_recycling_lbs": 15100.0, "customer_voucher_rewards_usd": 7900.00},
    {"program_name": "Garment Circularity Loop", "month": "2026-03", "collection_channel": "Store Drop-off Bin", "product_category": "Apparel & Footwear", "weight_collected_lbs": 18200.0, "processed_for_recycling_lbs": 17400.0, "customer_voucher_rewards_usd": 9100.00},
    {"program_name": "Garment Circularity Loop", "month": "2026-04", "collection_channel": "Store Drop-off Bin", "product_category": "Apparel & Footwear", "weight_collected_lbs": 19500.0, "processed_for_recycling_lbs": 18700.0, "customer_voucher_rewards_usd": 9750.00},
    {"program_name": "Garment Circularity Loop", "month": "2026-05", "collection_channel": "Store Drop-off Bin", "product_category": "Apparel & Footwear", "weight_collected_lbs": 22400.0, "processed_for_recycling_lbs": 21500.0, "customer_voucher_rewards_usd": 11200.00},
    {"program_name": "Garment Circularity Loop", "month": "2026-06", "collection_channel": "Store Drop-off Bin", "product_category": "Apparel & Footwear", "weight_collected_lbs": 24800.0, "processed_for_recycling_lbs": 23900.0, "customer_voucher_rewards_usd": 12400.00},
    {"program_name": "Small Tech Trade-In", "month": "2026-01", "collection_channel": "Mail-in Prepaid Kit", "product_category": "Consumer Electronics", "weight_collected_lbs": 3800.0, "processed_for_recycling_lbs": 3600.0, "customer_voucher_rewards_usd": 14500.00},
    {"program_name": "Small Tech Trade-In", "month": "2026-02", "collection_channel": "Mail-in Prepaid Kit", "product_category": "Consumer Electronics", "weight_collected_lbs": 4200.0, "processed_for_recycling_lbs": 4000.0, "customer_voucher_rewards_usd": 16200.00},
    {"program_name": "Small Tech Trade-In", "month": "2026-03", "collection_channel": "Mail-in Prepaid Kit", "product_category": "Consumer Electronics", "weight_collected_lbs": 4900.0, "processed_for_recycling_lbs": 4700.0, "customer_voucher_rewards_usd": 19000.00},
    {"program_name": "Small Tech Trade-In", "month": "2026-04", "collection_channel": "Mail-in Prepaid Kit", "product_category": "Consumer Electronics", "weight_collected_lbs": 5300.0, "processed_for_recycling_lbs": 5100.0, "customer_voucher_rewards_usd": 20800.00},
    {"program_name": "Small Tech Trade-In", "month": "2026-05", "collection_channel": "Mail-in Prepaid Kit", "product_category": "Consumer Electronics", "weight_collected_lbs": 6100.0, "processed_for_recycling_lbs": 5850.0, "customer_voucher_rewards_usd": 24000.00},
    {"program_name": "Small Tech Trade-In", "month": "2026-06", "collection_channel": "Mail-in Prepaid Kit", "product_category": "Consumer Electronics", "weight_collected_lbs": 6700.0, "processed_for_recycling_lbs": 6450.0, "customer_voucher_rewards_usd": 26500.00},
]

RESALE_INVENTORY = [
    {"item_id": "RESALE-1001", "original_sku": "SKU-002", "product_category": "Apparel", "resale_condition_grade": "Like New - Refurbished", "refurb_cost_usd": 12.50, "resale_price_usd": 68.00, "recommerce_channel": "Digital Pre-Loved Marketplace", "resale_status": "Sold"},
    {"item_id": "RESALE-1002", "original_sku": "SKU-002", "product_category": "Apparel", "resale_condition_grade": "Gently Used", "refurb_cost_usd": 8.00, "resale_price_usd": 52.00, "recommerce_channel": "Digital Pre-Loved Marketplace", "resale_status": "Sold"},
    {"item_id": "RESALE-1003", "original_sku": "SKU-005", "product_category": "Electronics", "resale_condition_grade": "Certified Factory Reconditioned", "refurb_cost_usd": 28.00, "resale_price_usd": 129.00, "recommerce_channel": "Store Pre-Owned Kiosk", "resale_status": "Sold"},
    {"item_id": "RESALE-1004", "original_sku": "SKU-005", "product_category": "Electronics", "resale_condition_grade": "Certified Factory Reconditioned", "refurb_cost_usd": 28.00, "resale_price_usd": 129.00, "recommerce_channel": "Store Pre-Owned Kiosk", "resale_status": "Available"},
    {"item_id": "RESALE-1005", "original_sku": "SKU-006", "product_category": "Drinkware", "resale_condition_grade": "Open Box - Sanitized", "refurb_cost_usd": 3.50, "resale_price_usd": 22.00, "recommerce_channel": "Digital Pre-Loved Marketplace", "resale_status": "Sold"},
]

CIRCULAR_REVENUE = [
    {"fiscal_month": "2026-01", "recovery_channel": "Digital Recommerce", "units_recovered": 1250, "gross_recovery_revenue_usd": 48500.00, "processing_cost_usd": 14200.00, "net_circular_profit_usd": 34300.00, "tons_diverted_from_landfill": 9.2},
    {"fiscal_month": "2026-02", "recovery_channel": "Digital Recommerce", "units_recovered": 1420, "gross_recovery_revenue_usd": 54800.00, "processing_cost_usd": 15800.00, "net_circular_profit_usd": 39000.00, "tons_diverted_from_landfill": 10.5},
    {"fiscal_month": "2026-03", "recovery_channel": "Digital Recommerce", "units_recovered": 1680, "gross_recovery_revenue_usd": 65200.00, "processing_cost_usd": 18400.00, "net_circular_profit_usd": 46800.00, "tons_diverted_from_landfill": 12.4},
    {"fiscal_month": "2026-04", "recovery_channel": "Digital Recommerce", "units_recovered": 1890, "gross_recovery_revenue_usd": 74100.00, "processing_cost_usd": 20500.00, "net_circular_profit_usd": 53600.00, "tons_diverted_from_landfill": 14.1},
    {"fiscal_month": "2026-05", "recovery_channel": "Digital Recommerce", "units_recovered": 2150, "gross_recovery_revenue_usd": 85600.00, "processing_cost_usd": 23200.00, "net_circular_profit_usd": 62400.00, "tons_diverted_from_landfill": 16.2},
    {"fiscal_month": "2026-06", "recovery_channel": "Digital Recommerce", "units_recovered": 2420, "gross_recovery_revenue_usd": 96500.00, "processing_cost_usd": 25800.00, "net_circular_profit_usd": 70700.00, "tons_diverted_from_landfill": 18.5},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(EPR_FEES, "epr_packaging_fees_paid.csv")
    generate_csv(TAKE_BACK, "take_back_program_tonnage.csv")
    generate_csv(RESALE_INVENTORY, "textile_electronic_resale.csv")
    generate_csv(CIRCULAR_REVENUE, "circular_recovery_revenue.csv")

if __name__ == "__main__":
    main()
