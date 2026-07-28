"""Generate synthetic seed CSV data for Marketing: Campaign Performance & ROI."""

import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent


def generate_campaigns() -> None:
    headers = ["campaign_id", "campaign_name", "start_date", "end_date", "target_audience", "budget_amount"]
    campaigns = [
        ["CMP-001", "Summer Fashion Blowout", "2026-06-25", "2026-07-25", "Young Adults 18-35", 50000.00],
        ["CMP-002", "Back-to-School Tech Prep", "2026-07-01", "2026-08-15", "College Students & Parents", 85000.00],
        ["CMP-003", "Home Comfort Refresh", "2026-07-10", "2026-08-10", "Homeowners 28-54", 40000.00],
        ["CMP-004", "VIP Loyalty Appreciation", "2026-07-15", "2026-07-22", "Gold & Platinum Loyalty Members", 20000.00],
        ["CMP-005", "Mid-Summer Clearance Flash Sale", "2026-07-20", "2026-07-24", "Bargain Seekers", 15000.00],
        ["CMP-006", "Omnichannel Mobile App Acquisition", "2026-07-01", "2026-07-31", "Mobile Shoppers", 30000.00],
    ]
    with open(DATA_DIR / "campaigns.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(campaigns)


def generate_ad_spend_channels() -> None:
    headers = ["campaign_id", "channel", "date", "ad_spend_amount", "impressions", "clicks"]
    base_date = datetime(2026, 7, 24)
    dates = [(base_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
    channels_meta = [
        ("Paid Search", 350.0, 12000, 480),
        ("Social Media", 400.0, 18000, 620),
        ("Email", 80.0, 5000, 450),
        ("Connected TV", 600.0, 25000, 310),
    ]

    records = []
    for d in dates:
        for cid in ["CMP-001", "CMP-002", "CMP-003", "CMP-004", "CMP-005", "CMP-006"]:
            for ch, spend, imp, clk in channels_meta:
                records.append([cid, ch, d, spend, imp, clk])

    with open(DATA_DIR / "ad_spend_channels.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)


def generate_campaign_conversions() -> None:
    headers = ["campaign_id", "date", "conversions_count", "attributed_revenue", "new_customers_acquired"]
    base_date = datetime(2026, 7, 24)
    dates = [(base_date - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]
    campaign_conv_meta = {
        "CMP-001": (45, 2250.00, 12),
        "CMP-002": (60, 4800.00, 18),
        "CMP-003": (30, 2100.00, 8),
        "CMP-004": (85, 5950.00, 5),
        "CMP-005": (110, 4400.00, 28),
        "CMP-006": (40, 1600.00, 22),
    }

    records = []
    for d in dates:
        for cid, (convs, rev, new_cust) in campaign_conv_meta.items():
            records.append([cid, d, convs, rev, new_cust])

    with open(DATA_DIR / "campaign_conversions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)


def generate_channel_roas_targets() -> None:
    headers = ["channel", "fiscal_quarter", "target_roas", "target_cac"]
    targets = [
        ["Paid Search", "2026-Q3", 4.5, 28.00],
        ["Social Media", "2026-Q3", 3.8, 32.00],
        ["Email", "2026-Q3", 12.0, 8.50],
        ["Connected TV", "2026-Q3", 2.5, 65.00],
    ]
    with open(DATA_DIR / "channel_roas_targets.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(targets)


def main() -> None:
    generate_campaigns()
    generate_ad_spend_channels()
    generate_campaign_conversions()
    generate_channel_roas_targets()
    print("Successfully generated all 4 campaign_performance_roi CSV files.")


if __name__ == "__main__":
    main()
