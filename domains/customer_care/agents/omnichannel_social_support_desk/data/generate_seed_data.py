"""Generate synthetic seed CSV data for Customer Care: Social Support & Public Sentiment."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_social_media_tickets():
    headers = ["ticket_id", "platform", "post_timestamp", "author_handle", "post_type", "issue_category", "sentiment", "status"]
    rows = [
        ["SOC-101", "X / Twitter", "2026-08-05 14:10:00", "@sarah_fashionista", "Public Mention", "Delayed Delivery", "Negative", "Resolved via DM"],
        ["SOC-102", "Instagram", "2026-08-05 15:30:00", "@urban_runner_mike", "Post Comment", "Shoe Size Sizing", "Neutral", "Answered in Thread"],
        ["SOC-103", "TikTok", "2026-08-04 19:45:00", "@tech_reviewer_dan", "Video Mention", "Defective Earbud Battery", "Critical", "Executive Concierge Assigned"],
        ["SOC-104", "Facebook", "2026-08-04 11:20:00", "@jennifer_smith", "Direct Message", "Store Pickup Question", "Positive", "Resolved in DM"],
        ["SOC-105", "Reddit", "2026-08-03 09:15:00", "u/style_curator", "Subreddit Thread", "Return Policy Confusion", "Negative", "Clarified by Support Rep"],
    ]
    with open(DATA_DIR / "social_media_tickets.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_public_response_speed():
    headers = ["date", "platform", "total_mentions", "responded_within_15m_count", "avg_response_time_minutes", "target_sla_mins", "sla_compliance_pct"]
    platforms = [
        ("X / Twitter", 85, 80, 11.5, 15.0, 94.1),
        ("Instagram", 65, 58, 13.2, 15.0, 89.2),
        ("TikTok", 45, 38, 14.0, 15.0, 84.4),
        ("Facebook", 40, 38, 9.8, 15.0, 95.0),
        ("Reddit", 25, 22, 12.5, 15.0, 88.0),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for plat, tot, within, aht, tgt, comp in platforms:
            v_tot = tot + (day % 5) * 3 - 6
            v_within = within + (day % 4) * 2 - 4
            v_aht = round(aht + ((day % 3) - 1) * 0.5, 1)
            v_comp = round((v_within / v_tot) * 100.0, 1)
            rows.append([d_str, plat, v_tot, v_within, v_aht, tgt, v_comp])
    with open(DATA_DIR / "public_response_speed.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_escalation_sentiment_shift():
    headers = ["ticket_id", "platform", "initial_sentiment_score", "post_resolution_sentiment_score", "sentiment_shift_delta", "de_escalation_successful", "moved_to_dm"]
    rows = [
        ["SOC-101", "X / Twitter", -0.75, 0.60, 1.35, True, True],
        ["SOC-102", "Instagram", 0.05, 0.70, 0.65, True, False],
        ["SOC-103", "TikTok", -0.90, 0.40, 1.30, True, True],
        ["SOC-104", "Facebook", 0.20, 0.85, 0.65, True, True],
        ["SOC-105", "Reddit", -0.60, 0.35, 0.95, True, False],
    ]
    with open(DATA_DIR / "escalation_sentiment_shift.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_dm_commerce_inquiries():
    headers = ["dm_id", "platform", "customer_handle", "inquiry_date", "inquiry_intent", "converted_to_sale", "attributed_order_value"]
    rows = [
        ["DM-801", "Instagram", "@fashionista_claire", "2026-08-05", "Outfit Matching Advice", True, 285.00],
        ["DM-802", "Instagram", "@marcus_outdoor", "2026-08-04", "Stock Check in Soho Store", True, 195.00],
        ["DM-803", "TikTok", "@trendy_shopper", "2026-08-03", "Viral Jacket Sizing Inquiry", True, 145.00],
        ["DM-804", "X / Twitter", "@alex_tech_geek", "2026-08-02", "Wireless Earbud Specs", False, 0.00],
        ["DM-805", "Facebook", "@sarah_family", "2026-08-01", "Back to School Promo Discount", True, 340.00],
    ]
    with open(DATA_DIR / "dm_commerce_inquiries.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_social_media_tickets()
    generate_public_response_speed()
    generate_escalation_sentiment_shift()
    generate_dm_commerce_inquiries()
    print("omnichannel_social_support_desk seed data generated.")

if __name__ == "__main__":
    main()
