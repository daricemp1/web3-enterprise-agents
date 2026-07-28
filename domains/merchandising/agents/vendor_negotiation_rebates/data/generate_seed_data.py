#!/usr/bin/env python3
"""Generates this agent's synthetic BigQuery seed data (data/*.csv).

Run once; the output is committed as static CSVs, not regenerated at load time.

Usage:
    uv run python domains/merchandising/agents/vendor_negotiation_rebates/data/generate_seed_data.py
"""
from __future__ import annotations

import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

VENDORS = [
    {
        "vendor_id": "VND-001",
        "vendor_name": "Apex Apparel",
        "vendor_tier": "Strategic",
        "category_lead": "Outerwear",
        "payment_terms": "Net 60",
    },
    {
        "vendor_id": "VND-002",
        "vendor_name": "Summit Outdoor",
        "vendor_tier": "Strategic",
        "category_lead": "Footwear",
        "payment_terms": "2/10 Net 30",
    },
    {
        "vendor_id": "VND-003",
        "vendor_name": "Cascade Gear",
        "vendor_tier": "Preferred",
        "category_lead": "Apparel",
        "payment_terms": "Net 30",
    },
    {
        "vendor_id": "VND-004",
        "vendor_name": "Alpine Tech",
        "vendor_tier": "Preferred",
        "category_lead": "Outerwear",
        "payment_terms": "Net 60",
    },
    {
        "vendor_id": "VND-005",
        "vendor_name": "Pacific Threads",
        "vendor_tier": "Standard",
        "category_lead": "Accessories",
        "payment_terms": "Net 30",
    },
]

REBATE_AGREEMENTS = [
    {
        "agreement_id": "REB-001",
        "vendor_id": "VND-001",
        "fiscal_year": 2026,
        "tier_1_threshold_spend": 500000.00,
        "tier_1_rebate_pct": 3.0,
        "tier_2_threshold_spend": 1000000.00,
        "tier_2_rebate_pct": 5.0,
        "current_ytd_spend": 1250000.00,
        "current_rebate_tier": "Tier 2",
    },
    {
        "agreement_id": "REB-002",
        "vendor_id": "VND-002",
        "fiscal_year": 2026,
        "tier_1_threshold_spend": 400000.00,
        "tier_1_rebate_pct": 2.5,
        "tier_2_threshold_spend": 800000.00,
        "tier_2_rebate_pct": 4.5,
        "current_ytd_spend": 650000.00,
        "current_rebate_tier": "Tier 1",
    },
    {
        "agreement_id": "REB-003",
        "vendor_id": "VND-003",
        "fiscal_year": 2026,
        "tier_1_threshold_spend": 300000.00,
        "tier_1_rebate_pct": 2.0,
        "tier_2_threshold_spend": 600000.00,
        "tier_2_rebate_pct": 4.0,
        "current_ytd_spend": 450000.00,
        "current_rebate_tier": "Tier 1",
    },
    {
        "agreement_id": "REB-004",
        "vendor_id": "VND-004",
        "fiscal_year": 2026,
        "tier_1_threshold_spend": 500000.00,
        "tier_1_rebate_pct": 3.0,
        "tier_2_threshold_spend": 1000000.00,
        "tier_2_rebate_pct": 5.0,
        "current_ytd_spend": 350000.00,
        "current_rebate_tier": "Base",
    },
    {
        "agreement_id": "REB-005",
        "vendor_id": "VND-005",
        "fiscal_year": 2026,
        "tier_1_threshold_spend": 250000.00,
        "tier_1_rebate_pct": 1.5,
        "tier_2_threshold_spend": 500000.00,
        "tier_2_rebate_pct": 3.0,
        "current_ytd_spend": 520000.00,
        "current_rebate_tier": "Tier 2",
    },
]

COOP_MARKETING_FUNDS = [
    {
        "vendor_id": "VND-001",
        "campaign_id": "CMP-001",
        "fiscal_quarter": "2026-Q3",
        "committed_coop_amount": 50000.00,
        "claimed_coop_amount": 45000.00,
        "approved_coop_amount": 40000.00,
        "pending_claim_amount": 5000.00,
    },
    {
        "vendor_id": "VND-002",
        "campaign_id": "CMP-002",
        "fiscal_quarter": "2026-Q3",
        "committed_coop_amount": 40000.00,
        "claimed_coop_amount": 38000.00,
        "approved_coop_amount": 35000.00,
        "pending_claim_amount": 3000.00,
    },
    {
        "vendor_id": "VND-003",
        "campaign_id": "CMP-003",
        "fiscal_quarter": "2026-Q3",
        "committed_coop_amount": 30000.00,
        "claimed_coop_amount": 25000.00,
        "approved_coop_amount": 20000.00,
        "pending_claim_amount": 5000.00,
    },
    {
        "vendor_id": "VND-004",
        "campaign_id": "CMP-004",
        "fiscal_quarter": "2026-Q3",
        "committed_coop_amount": 25000.00,
        "claimed_coop_amount": 20000.00,
        "approved_coop_amount": 18000.00,
        "pending_claim_amount": 2000.00,
    },
]

VENDOR_SETTLEMENTS = [
    {
        "vendor_id": "VND-001",
        "fiscal_quarter": "2026-Q3",
        "earned_rebate_amount": 62500.00,
        "collected_rebate_amount": 56250.00,
        "outstanding_dispute_amount": 6250.00,
        "rebate_realization_pct": 90.00,
    },
    {
        "vendor_id": "VND-002",
        "fiscal_quarter": "2026-Q3",
        "earned_rebate_amount": 29250.00,
        "collected_rebate_amount": 24862.50,
        "outstanding_dispute_amount": 4387.50,
        "rebate_realization_pct": 85.00,
    },
    {
        "vendor_id": "VND-003",
        "fiscal_quarter": "2026-Q3",
        "earned_rebate_amount": 9000.00,
        "collected_rebate_amount": 7200.00,
        "outstanding_dispute_amount": 1800.00,
        "rebate_realization_pct": 80.00,
    },
    {
        "vendor_id": "VND-004",
        "fiscal_quarter": "2026-Q3",
        "earned_rebate_amount": 0.00,
        "collected_rebate_amount": 0.00,
        "outstanding_dispute_amount": 0.00,
        "rebate_realization_pct": 100.00,
    },
    {
        "vendor_id": "VND-005",
        "fiscal_quarter": "2026-Q3",
        "earned_rebate_amount": 15600.00,
        "collected_rebate_amount": 14820.00,
        "outstanding_dispute_amount": 780.00,
        "rebate_realization_pct": 95.00,
    },
]


def write_vendors() -> None:
    with open(DATA_DIR / "vendors.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "vendor_id", "vendor_name", "vendor_tier", "category_lead", "payment_terms"
        ])
        for v in VENDORS:
            writer.writerow([
                v["vendor_id"], v["vendor_name"], v["vendor_tier"],
                v["category_lead"], v["payment_terms"]
            ])


def write_rebate_agreements() -> None:
    with open(DATA_DIR / "rebate_agreements.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "agreement_id", "vendor_id", "fiscal_year", "tier_1_threshold_spend",
            "tier_1_rebate_pct", "tier_2_threshold_spend", "tier_2_rebate_pct",
            "current_ytd_spend", "current_rebate_tier"
        ])
        for r in REBATE_AGREEMENTS:
            writer.writerow([
                r["agreement_id"], r["vendor_id"], r["fiscal_year"],
                r["tier_1_threshold_spend"], r["tier_1_rebate_pct"],
                r["tier_2_threshold_spend"], r["tier_2_rebate_pct"],
                r["current_ytd_spend"], r["current_rebate_tier"]
            ])


def write_coop_marketing_funds() -> None:
    with open(DATA_DIR / "coop_marketing_funds.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "vendor_id", "campaign_id", "fiscal_quarter", "committed_coop_amount",
            "claimed_coop_amount", "approved_coop_amount", "pending_claim_amount"
        ])
        for c in COOP_MARKETING_FUNDS:
            writer.writerow([
                c["vendor_id"], c["campaign_id"], c["fiscal_quarter"],
                c["committed_coop_amount"], c["claimed_coop_amount"],
                c["approved_coop_amount"], c["pending_claim_amount"]
            ])


def write_vendor_settlements() -> None:
    with open(DATA_DIR / "vendor_settlements.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "vendor_id", "fiscal_quarter", "earned_rebate_amount",
            "collected_rebate_amount", "outstanding_dispute_amount",
            "rebate_realization_pct"
        ])
        for s in VENDOR_SETTLEMENTS:
            writer.writerow([
                s["vendor_id"], s["fiscal_quarter"], s["earned_rebate_amount"],
                s["collected_rebate_amount"], s["outstanding_dispute_amount"],
                s["rebate_realization_pct"]
            ])


def main() -> None:
    write_vendors()
    write_rebate_agreements()
    write_coop_marketing_funds()
    write_vendor_settlements()
    print(f"Wrote seed CSVs to {DATA_DIR}")


if __name__ == "__main__":
    main()
