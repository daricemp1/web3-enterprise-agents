"""Generate synthetic seed CSV data for Customer Care: VIP & High-CLV Concierge."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_vip_customer_profiles():
    headers = ["customer_id", "customer_name", "tier_level", "annual_spend_ytd", "dedicated_concierge_agent_id", "lifetime_clv", "preferred_channel", "nps_score"]
    rows = [
        ["CUST-1001", "Victoria Sterling", "Diamond Card", 42500.00, "AGT-108", 128000.00, "Dedicated WhatsApp", 10],
        ["CUST-1002", "Alexander Montgomery", "Diamond Card", 38900.00, "AGT-108", 95000.00, "Private Phone Line", 9],
        ["CUST-1003", "Sophia Laurent", "Platinum Tier", 18500.00, "AGT-107", 45000.00, "SMS / Text", 10],
        ["CUST-1004", "Marcus Vance", "Platinum Tier", 22400.00, "AGT-107", 58000.00, "Private Phone Line", 9],
        ["CUST-1005", "Isabella Rossi", "Diamond Card", 51200.00, "AGT-108", 160000.00, "Dedicated WhatsApp", 10],
        ["CUST-1006", "Harrison Forde", "Platinum Tier", 16800.00, "AGT-107", 42000.00, "Email Concierge", 8],
    ]
    with open(DATA_DIR / "vip_customer_profiles.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_concierge_service_requests():
    headers = ["request_id", "customer_id", "request_type", "request_date", "response_time_minutes", "status", "sla_met"]
    rows = [
        ["VIP-101", "CUST-1001", "Personal Styling Consultation", "2026-08-05", 2.5, "Completed", True],
        ["VIP-102", "CUST-1005", "Rare Runway Item Sourcing", "2026-08-05", 3.1, "In Progress", True],
        ["VIP-103", "CUST-1002", "Priority Same-Day Delivery", "2026-08-04", 1.8, "Delivered", True],
        ["VIP-104", "CUST-1004", "Private In-Store Suite Fitting", "2026-08-03", 4.2, "Scheduled", True],
        ["VIP-105", "CUST-1003", "Custom Monogramming Order", "2026-08-02", 2.0, "Completed", True],
        ["VIP-106", "CUST-1006", "Order Reroute & Gift Packing", "2026-08-01", 3.8, "Completed", True],
    ]
    with open(DATA_DIR / "concierge_service_requests.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_dedicated_agent_sla():
    headers = ["agent_id", "agent_name", "date", "assigned_vip_count", "avg_first_response_mins", "target_sla_mins", "sla_adherence_pct", "client_satisfaction_score"]
    agents = [
        ("AGT-108", "James Wilson", 45, 2.4, 5.0, 98.2, 4.95),
        ("AGT-107", "Rachel Kim", 55, 3.1, 5.0, 96.5, 4.88),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for agt_id, name, vips, resp, tgt, adh, csat in agents:
            v_resp = round(resp + ((day % 3) - 1) * 0.2, 1)
            v_adh = round(adh + ((day % 4) - 1.5) * 0.4, 1)
            v_csat = round(csat + ((day % 3) - 1) * 0.02, 2)
            rows.append([agt_id, name, d_str, vips, v_resp, tgt, v_adh, v_csat])
    with open(DATA_DIR / "dedicated_agent_sla.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_assisted_sales_revenue():
    headers = ["transaction_id", "customer_id", "concierge_agent_id", "sale_date", "order_amount", "product_category", "commission_earned"]
    rows = [
        ["TX-VIP-901", "CUST-1001", "AGT-108", "2026-08-05", 4850.00, "Luxury Outerwear & Accessories", 145.50],
        ["TX-VIP-902", "CUST-1005", "AGT-108", "2026-08-04", 6200.00, "Fine Jewelry & Watches", 186.00],
        ["TX-VIP-903", "CUST-1002", "AGT-108", "2026-08-03", 3100.00, "Designer Footwear & Leather", 93.00],
        ["TX-VIP-904", "CUST-1003", "AGT-107", "2026-08-02", 2400.00, "Evening Wear & Dresses", 72.00],
        ["TX-VIP-905", "CUST-1004", "AGT-107", "2026-08-01", 1950.00, "Tailored Menswear", 58.50],
    ]
    with open(DATA_DIR / "assisted_sales_revenue.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_vip_customer_profiles()
    generate_concierge_service_requests()
    generate_dedicated_agent_sla()
    generate_assisted_sales_revenue()
    print("vip_clientele_concierge_support seed data generated.")

if __name__ == "__main__":
    main()
