"""Generate synthetic seed CSV data for Customer Care: Contact Center Performance & FCR."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_call_center_queues():
    headers = ["queue_id", "queue_name", "channel", "target_sla_seconds", "target_fcr_pct", "target_aht_seconds", "staffing_headcount"]
    rows = [
        ["Q-101", "E-Commerce Customer Support", "Voice", 30, 75.0, 360, 25],
        ["Q-102", "Billing & Payment Inquiries", "Voice", 45, 80.0, 420, 18],
        ["Q-103", "Shipping & Delivery Tracking", "Voice", 30, 70.0, 300, 22],
        ["Q-104", "Digital Live Chat Support", "Chat", 15, 82.0, 240, 30],
        ["Q-105", "Loyalty & Rewards Program", "Voice", 60, 85.0, 300, 12],
        ["Q-106", "VIP Priority Concierge", "Voice", 10, 90.0, 480, 10],
    ]
    with open(DATA_DIR / "call_center_queues.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_agent_interaction_metrics():
    headers = ["agent_id", "agent_name", "queue_id", "date", "total_calls_handled", "avg_handle_time_seconds", "occupancy_rate_pct", "hold_time_avg_seconds", "transfers_count"]
    agents = [
        ("AGT-101", "Sarah Jenkins", "Q-101", 42, 345, 83.5, 45, 3),
        ("AGT-102", "David Chen", "Q-101", 38, 380, 86.0, 60, 5),
        ("AGT-103", "Elena Rodriguez", "Q-102", 35, 410, 81.2, 50, 2),
        ("AGT-104", "Marcus Johnson", "Q-103", 48, 295, 84.8, 35, 4),
        ("AGT-105", "Aisha Patel", "Q-104", 65, 230, 88.5, 20, 6),
        ("AGT-106", "Brian Taylor", "Q-104", 58, 255, 85.0, 25, 4),
        ("AGT-107", "Rachel Kim", "Q-105", 40, 310, 79.5, 40, 1),
        ("AGT-108", "James Wilson", "Q-106", 28, 465, 82.0, 55, 1),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for agt_id, name, q_id, calls, aht, occ, hold, trans in agents:
            # Add slight daily variation
            v_calls = calls + (day % 5) - 2
            v_aht = aht + (day % 7) * 3 - 9
            v_occ = round(occ + ((day % 3) - 1) * 0.8, 1)
            rows.append([agt_id, name, q_id, d_str, v_calls, v_aht, v_occ, hold, trans])
    with open(DATA_DIR / "agent_interaction_metrics.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_first_contact_resolution():
    headers = ["queue_id", "date", "resolved_first_contact_count", "total_contacts_count", "repeat_contacts_72h_count", "fcr_rate_pct"]
    queues = [
        ("Q-101", 310, 400, 90, 77.5),
        ("Q-102", 235, 280, 45, 83.9),
        ("Q-103", 260, 360, 100, 72.2),
        ("Q-104", 520, 620, 100, 83.9),
        ("Q-105", 175, 200, 25, 87.5),
        ("Q-106", 110, 120, 10, 91.7),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for q_id, res_cnt, tot_cnt, rep_cnt, fcr in queues:
            v_res = res_cnt + (day % 6) * 4 - 10
            v_tot = tot_cnt + (day % 5) * 5 - 10
            v_rep = v_tot - v_res
            v_fcr = round((v_res / v_tot) * 100.0, 1)
            rows.append([q_id, d_str, v_res, v_tot, v_rep, v_fcr])
    with open(DATA_DIR / "first_contact_resolution.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_csat_survey_scores():
    headers = ["survey_id", "agent_id", "queue_id", "date", "csat_score", "nps_rating", "resolution_satisfied", "customer_verbatim"]
    rows = [
        ["SRV-1001", "AGT-101", "Q-101", "2026-08-05", 5, 10, True, "Sarah resolved my order address issue immediately. Excellent help!"],
        ["SRV-1002", "AGT-102", "Q-101", "2026-08-05", 3, 6, False, "Took too long to find my promo discount."],
        ["SRV-1003", "AGT-103", "Q-102", "2026-08-04", 5, 9, True, "Billing discrepancy corrected without hassle."],
        ["SRV-1004", "AGT-104", "Q-103", "2026-08-04", 4, 8, True, "Tracked down my delayed courier package."],
        ["SRV-1005", "AGT-105", "Q-104", "2026-08-03", 5, 10, True, "Super fast chat assistance on size exchange."],
        ["SRV-1006", "AGT-106", "Q-104", "2026-08-03", 4, 8, True, "Helpful chat guidance."],
        ["SRV-1007", "AGT-107", "Q-105", "2026-08-02", 5, 10, True, "Loyalty points credited promptly."],
        ["SRV-1008", "AGT-108", "Q-106", "2026-08-01", 5, 10, True, "Outstanding VIP white glove concierge service!"],
    ]
    with open(DATA_DIR / "csat_survey_scores.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_call_center_queues()
    generate_agent_interaction_metrics()
    generate_first_contact_resolution()
    generate_csat_survey_scores()
    print("contact_center_agent_performance seed data generated.")

if __name__ == "__main__":
    main()
