"""Generate synthetic seed CSV data for Customer Care: Voice of Customer & NLP Sentiment."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_customer_feedback_transcripts():
    headers = ["feedback_id", "customer_id", "channel", "feedback_date", "category", "sentiment_score", "sentiment_label", "key_phrases", "transcript_summary"]
    rows = [
        ["FBD-301", "CUST-1001", "Voice", "2026-08-05", "Sizing & Fit", -0.65, "Negative", "runs too small; tight sleeves; size chart incorrect", "Customer ordered Size M jacket but fits like XS."],
        ["FBD-302", "CUST-1002", "Chat", "2026-08-05", "Delivery Speed", 0.85, "Positive", "arrived 2 days early; perfect packaging; driver polite", "Delighted by early weekend delivery."],
        ["FBD-303", "CUST-1003", "Survey", "2026-08-04", "Product Quality", -0.80, "Negative", "seam tearing; loose threads; cheap material", "Shirt hem came undone after initial wash."],
        ["FBD-304", "CUST-1004", "Mobile App", "2026-08-04", "Checkout Experience", 0.70, "Positive", "one-click pay; super smooth; easy return pickup", "Pleased with Apple Pay integration."],
        ["FBD-305", "CUST-1005", "Voice", "2026-08-03", "Customer Support", 0.90, "Positive", "agent was fantastic; instant refund; courteous", "Agent credited missing promo instantly."],
        ["FBD-306", "CUST-1006", "Email", "2026-08-02", "Delivery Delay", -0.75, "Negative", "late 5 days; missed birthday; tracking stuck", "Gift delayed beyond promised date."],
    ]
    with open(DATA_DIR / "customer_feedback_transcripts.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_nps_sentiment_topics():
    headers = ["topic_id", "topic_name", "category", "date", "mention_count", "net_sentiment_score", "promoter_mentions", "detractor_mentions", "sentiment_trend"]
    topics = [
        ("TOP-101", "Apparel Sizing Consistency", "Product", 185, -0.42, 35, 110, "Declining"),
        ("TOP-102", "On-Time Shipping Reliability", "Logistics", 240, 0.28, 140, 70, "Improving"),
        ("TOP-103", "In-Store Return Convenience", "Store Ops", 195, 0.65, 150, 20, "Stable"),
        ("TOP-104", "Customer Support Courtesy", "Care", 280, 0.72, 220, 30, "Improving"),
        ("TOP-105", "Website Search & Filter Accuracy", "Digital", 140, 0.15, 75, 50, "Stable"),
        ("TOP-106", "Product Durability & Fabric Quality", "Product", 160, -0.35, 40, 95, "Declining"),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for t_id, name, cat, cnt, score, prom, det, trend in topics:
            v_cnt = cnt + (day % 5) * 4 - 8
            v_score = round(score + ((day % 3) - 1) * 0.03, 2)
            rows.append([t_id, name, cat, d_str, v_cnt, v_score, prom, det, trend])
    with open(DATA_DIR / "nps_sentiment_topics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_product_defect_signals():
    headers = ["signal_id", "sku", "product_name", "defect_category", "complaint_frequency_7d", "sentiment_drop_pct", "alert_severity", "first_detected_date"]
    rows = [
        ["SIG-401", "SKU-001", "Waterproof Shell Jacket", "Zipper Seizing / Breakage", 38, 28.5, "High", "2026-07-28"],
        ["SIG-402", "SKU-003", "Wireless Noise-Cancelling Earbuds", "Battery Rapid Drain", 45, 34.0, "Critical", "2026-07-25"],
        ["SIG-403", "SKU-004", "Organic Cotton Casual Tee", "Collar Stitching Unravel", 22, 16.2, "Medium", "2026-08-01"],
        ["SIG-404", "SKU-006", "Stainless Steel Thermal Mug", "Lid Seal Leakage", 18, 14.0, "Low", "2026-08-02"],
    ]
    with open(DATA_DIR / "product_defect_signals.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_channel_sentiment_trends():
    headers = ["channel", "date", "positive_pct", "neutral_pct", "negative_pct", "avg_nps_score", "total_responses"]
    channels = [
        ("Voice", 62.0, 18.0, 20.0, 48.0, 320),
        ("Web Live Chat", 74.0, 14.0, 12.0, 62.0, 480),
        ("Mobile App Feedback", 78.0, 12.0, 10.0, 68.0, 290),
        ("Social Media Mentions", 54.0, 22.0, 24.0, 35.0, 210),
        ("Post-Purchase Email Survey", 70.0, 16.0, 14.0, 56.0, 650),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for ch, pos, neu, neg, nps, resp in channels:
            v_pos = round(pos + ((day % 4) - 1.5) * 0.8, 1)
            v_neg = round(neg - ((day % 3) - 1.0) * 0.6, 1)
            v_neu = round(100.0 - v_pos - v_neg, 1)
            v_nps = round(nps + ((day % 5) - 2) * 1.2, 1)
            v_resp = resp + (day % 7) * 10 - 30
            rows.append([ch, d_str, v_pos, v_neu, v_neg, v_nps, v_resp])
    with open(DATA_DIR / "channel_sentiment_trends.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_customer_feedback_transcripts()
    generate_nps_sentiment_topics()
    generate_product_defect_signals()
    generate_channel_sentiment_trends()
    print("voice_of_customer_sentiment_nlp seed data generated.")

if __name__ == "__main__":
    main()
