"""Generate synthetic seed CSV data for Customer Care: WISMO & Order Inquiries."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_wismo_inquiries():
    headers = ["inquiry_id", "order_id", "customer_id", "inquiry_date", "channel", "carrier_code", "order_age_days", "status_at_inquiry", "resolution_type"]
    rows = [
        ["WIS-2001", "ORD-98401", "CUST-1001", "2026-08-05", "Live Chat", "FedEx", 4, "In Transit - Delayed", "Provided Tracking Link"],
        ["WIS-2002", "ORD-98402", "CUST-1002", "2026-08-05", "Voice", "UPS", 6, "Exception - Sorting Delay", "Issued $15 Goodwill Credit"],
        ["WIS-2003", "ORD-98403", "CUST-1003", "2026-08-04", "Mobile App", "USPS", 3, "Out for Delivery", "Self-Service Confirmation"],
        ["WIS-2004", "ORD-98404", "CUST-1004", "2026-08-04", "Chatbot", "FedEx", 5, "In Transit - Weather Delay", "Automated ETA Update"],
        ["WIS-2005", "ORD-98405", "CUST-1005", "2026-08-03", "Email", "DHL", 7, "Lost in Transit", "Dispatched Free Replacement"],
        ["WIS-2006", "ORD-98406", "CUST-1006", "2026-08-02", "Voice", "UPS", 5, "Delivered - Front Porch", "Verified Delivery Photo"],
    ]
    with open(DATA_DIR / "wismo_inquiries.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_carrier_tracking_events():
    headers = ["tracking_number", "order_id", "carrier_code", "event_timestamp", "event_type", "event_location", "is_delayed", "delay_reason"]
    rows = [
        ["TRK-FDX-101", "ORD-98401", "FedEx", "2026-08-04 14:22:00", "Hub Scan", "Memphis TN Hub", True, "Severe Weather Congestion"],
        ["TRK-UPS-102", "ORD-98402", "UPS", "2026-08-04 09:15:00", "Sorting Exception", "Louisville KY DC", True, "Mechanical Belt Sort Failure"],
        ["TRK-USP-103", "ORD-98403", "USPS", "2026-08-04 08:30:00", "Out for Delivery", "Chicago IL Local", False, "None"],
        ["TRK-FDX-104", "ORD-98404", "FedEx", "2026-08-03 18:45:00", "In Transit", "Dallas TX Hub", True, "Highway Transport Delay"],
        ["TRK-DHL-105", "ORD-98405", "DHL", "2026-08-02 11:10:00", "Customs Hold", "Cincinnati OH Gateway", True, "Documentation Review"],
    ]
    with open(DATA_DIR / "carrier_tracking_events.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_automated_deflections():
    headers = ["date", "channel", "total_tracking_requests", "self_service_deflected_count", "bot_resolved_count", "escalated_to_agent_count", "deflection_rate_pct"]
    channels = [
        ("Web Tracking Portal", 450, 390, 0, 60, 86.7),
        ("Mobile App Tracker", 380, 340, 0, 40, 89.5),
        ("AI Chatbot", 220, 0, 160, 60, 72.7),
        ("SMS Notification", 310, 280, 0, 30, 90.3),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for ch, tot, ss, bot, esc, rate in channels:
            v_tot = tot + (day % 4) * 8 - 12
            v_esc = esc + (day % 3) * 2 - 2
            v_def = v_tot - v_esc
            v_rate = round((v_def / v_tot) * 100.0, 1)
            v_ss = v_def if bot == 0 else 0
            v_bot = v_def if bot > 0 else 0
            rows.append([d_str, ch, v_tot, v_ss, v_bot, v_esc, v_rate])
    with open(DATA_DIR / "automated_deflections.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_appeasement_credits():
    headers = ["appeasement_id", "order_id", "customer_id", "issue_date", "credit_amount", "appeasement_type", "delay_duration_days", "approved_by_agent_id"]
    rows = [
        ["APP-501", "ORD-98402", "CUST-1002", "2026-08-05", 15.00, "Gift Card", 3, "AGT-101"],
        ["APP-502", "ORD-98380", "CUST-1008", "2026-08-04", 10.00, "Shipping Refund", 2, "AGT-104"],
        ["APP-503", "ORD-98345", "CUST-1012", "2026-08-03", 25.00, "Courtesy Promo Code", 4, "AGT-103"],
        ["APP-504", "ORD-98310", "CUST-1015", "2026-08-02", 20.00, "Gift Card", 3, "AGT-102"],
        ["APP-505", "ORD-98290", "CUST-1020", "2026-08-01", 12.50, "Shipping Refund", 2, "AGT-105"],
    ]
    with open(DATA_DIR / "appeasement_credits.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_wismo_inquiries()
    generate_carrier_tracking_events()
    generate_automated_deflections()
    generate_appeasement_credits()
    print("wismo_order_tracking_resolution seed data generated.")

if __name__ == "__main__":
    main()
