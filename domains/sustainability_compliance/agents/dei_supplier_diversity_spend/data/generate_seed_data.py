#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Supplier Diversity & Equity Spend agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

SUPPLIER_MASTER = [
    {"vendor_id": "VEND-1001", "vendor_name": "EcoTextile Manufacturing Partners", "diversity_category": "Minority-Owned Business Enterprise (MBE)", "certifying_agency": "National Minority Supplier Development Council (NMSDC)", "certification_exp_date": "2027-04-30", "state_hq": "CA", "ownership_pct": 51.0},
    {"vendor_id": "VEND-1002", "vendor_name": "GreenPackaging Innovations Inc", "diversity_category": "Women-Owned Business Enterprise (WBE)", "certifying_agency": "Women's Business Enterprise National Council (WBENC)", "certification_exp_date": "2027-06-15", "state_hq": "OH", "ownership_pct": 65.0},
    {"vendor_id": "VEND-1003", "vendor_name": "PureEarth Organic Naturals", "diversity_category": "Service-Disabled Veteran-Owned (SDVOSB)", "certifying_agency": "National Veteran Business Development Council (NVBDC)", "certification_exp_date": "2026-11-30", "state_hq": "TX", "ownership_pct": 100.0},
    {"vendor_id": "VEND-1004", "vendor_name": "CleanTech Electronics & Hardware Ltd", "diversity_category": "LGBTQ+ Owned Business Enterprise (LGBTBE)", "certifying_agency": "National LGBT Chamber of Commerce (NGLCC)", "certification_exp_date": "2027-01-20", "state_hq": "WA", "ownership_pct": 55.0},
]

PROCUREMENT_SPEND = [
    {"vendor_id": "VEND-1001", "quarter": "2026-Q1", "tier_level": "Tier 1 - Direct", "category": "Apparel", "net_procurement_spend_usd": 4250000.00, "total_spend_pct": 4.25, "invoice_count": 48},
    {"vendor_id": "VEND-1001", "quarter": "2026-Q2", "tier_level": "Tier 1 - Direct", "category": "Apparel", "net_procurement_spend_usd": 4850000.00, "total_spend_pct": 4.60, "invoice_count": 54},
    {"vendor_id": "VEND-1002", "quarter": "2026-Q1", "tier_level": "Tier 1 - Direct", "category": "Packaging", "net_procurement_spend_usd": 2850000.00, "total_spend_pct": 2.85, "invoice_count": 36},
    {"vendor_id": "VEND-1002", "quarter": "2026-Q2", "tier_level": "Tier 1 - Direct", "category": "Packaging", "net_procurement_spend_usd": 3120000.00, "total_spend_pct": 2.95, "invoice_count": 40},
    {"vendor_id": "VEND-1003", "quarter": "2026-Q1", "tier_level": "Tier 1 - Direct", "category": "Home & Personal Care", "net_procurement_spend_usd": 1950000.00, "total_spend_pct": 1.95, "invoice_count": 28},
    {"vendor_id": "VEND-1003", "quarter": "2026-Q2", "tier_level": "Tier 1 - Direct", "category": "Home & Personal Care", "net_procurement_spend_usd": 2180000.00, "total_spend_pct": 2.05, "invoice_count": 32},
    {"vendor_id": "VEND-1004", "quarter": "2026-Q1", "tier_level": "Tier 1 - Direct", "category": "Electronics", "net_procurement_spend_usd": 3450000.00, "total_spend_pct": 3.45, "invoice_count": 22},
    {"vendor_id": "VEND-1004", "quarter": "2026-Q2", "tier_level": "Tier 1 - Direct", "category": "Electronics", "net_procurement_spend_usd": 3900000.00, "total_spend_pct": 3.70, "invoice_count": 26},
]

DIVERSITY_TARGETS = [
    {"fiscal_year": 2026, "diversity_category": "Minority-Owned Business Enterprise (MBE)", "annual_spend_target_usd": 18000000.00, "ytd_actual_spend_usd": 9100000.00, "target_achievement_pct": 50.5, "target_status": "On Track"},
    {"fiscal_year": 2026, "diversity_category": "Women-Owned Business Enterprise (WBE)", "annual_spend_target_usd": 12000000.00, "ytd_actual_spend_usd": 5970000.00, "target_achievement_pct": 49.8, "target_status": "On Track"},
    {"fiscal_year": 2026, "diversity_category": "Service-Disabled Veteran-Owned (SDVOSB)", "annual_spend_target_usd": 8000000.00, "ytd_actual_spend_usd": 4130000.00, "target_achievement_pct": 51.6, "target_status": "Exceeding Target"},
    {"fiscal_year": 2026, "diversity_category": "LGBTQ+ Owned Business Enterprise (LGBTBE)", "annual_spend_target_usd": 14000000.00, "ytd_actual_spend_usd": 7350000.00, "target_achievement_pct": 52.5, "target_status": "Exceeding Target"},
]

INCUBATION_PROGRAMS = [
    {"cohort_id": "COHORT-2025", "vendor_id": "VEND-1002", "incubation_track": "Sustainable Retail Packaging Acceleration", "onboarding_start_date": "2025-03-01", "mentor_executive": "VP Supply Chain Operations", "graduation_status": "Graduated & Scaled to National", "post_incubation_revenue_growth_pct": 42.5},
    {"cohort_id": "COHORT-2025", "vendor_id": "VEND-1003", "incubation_track": "Eco-Friendly Consumer Goods Scaling", "onboarding_start_date": "2025-06-01", "mentor_executive": "VP Merchandising Home & Personal Care", "graduation_status": "Graduated & Scaled to National", "post_incubation_revenue_growth_pct": 38.0},
    {"cohort_id": "COHORT-2026", "vendor_id": "VEND-1001", "incubation_track": "Circular Fashion & Low-Carbon Textiles", "onboarding_start_date": "2026-01-15", "mentor_executive": "Chief Sustainability Officer", "graduation_status": "Active In-Progress", "post_incubation_revenue_growth_pct": 18.5},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(SUPPLIER_MASTER, "diverse_supplier_master.csv")
    generate_csv(PROCUREMENT_SPEND, "procurement_spend_by_tier.csv")
    generate_csv(DIVERSITY_TARGETS, "diversity_category_targets.csv")
    generate_csv(INCUBATION_PROGRAMS, "vendor_incubation_programs.csv")

if __name__ == "__main__":
    main()
