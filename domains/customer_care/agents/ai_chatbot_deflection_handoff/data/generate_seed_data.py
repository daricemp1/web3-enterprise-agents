"""Generate synthetic seed CSV data for Customer Care: AI Bot Containment & Escalations."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_bot_conversations():
    headers = ["conversation_id", "customer_id", "session_start", "duration_seconds", "top_intent", "turn_count", "containment_status", "final_sentiment"]
    rows = [
        ["BOT-701", "CUST-1001", "2026-08-05 10:14:22", 145, "WISMO Order Status", 4, "Contained", "Positive"],
        ["BOT-702", "CUST-1002", "2026-08-05 10:28:10", 320, "Return Item Exception", 8, "Transferred to Agent", "Negative"],
        ["BOT-703", "CUST-1003", "2026-08-05 11:05:44", 95, "Store Hours & Location", 2, "Contained", "Positive"],
        ["BOT-704", "CUST-1004", "2026-08-04 14:18:30", 210, "Promo Code Discount Error", 5, "Contained", "Neutral"],
        ["BOT-705", "CUST-1005", "2026-08-04 16:40:15", 410, "Damaged Goods Claim", 9, "Transferred to Agent", "Negative"],
        ["BOT-706", "CUST-1006", "2026-08-03 09:12:00", 60, "Product Availability Inquiry", 2, "Abandoned", "Neutral"],
    ]
    with open(DATA_DIR / "bot_conversations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_intent_recognition_accuracy():
    headers = ["intent_id", "intent_name", "category", "date", "total_trigger_count", "recognized_correctly_count", "accuracy_pct", "fallback_rate_pct"]
    intents = [
        ("INT-101", "WISMO / Order Status", "Logistics", 420, 405, 96.4, 3.6),
        ("INT-102", "Initiate Return / Exchange", "Returns", 310, 290, 93.5, 6.5),
        ("INT-103", "Store Hours & Inventory", "Stores", 180, 175, 97.2, 2.8),
        ("INT-104", "Payment & Billing Dispute", "Finance", 150, 132, 88.0, 12.0),
        ("INT-105", "Product Specs & Sizing", "Catalog", 220, 202, 91.8, 8.2),
        ("INT-106", "Speak with Human Agent", "Escalation", 260, 255, 98.1, 1.9),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for i_id, name, cat, tot, rec, acc, fb in intents:
            v_tot = tot + (day % 6) * 5 - 12
            v_rec = rec + (day % 5) * 4 - 10
            v_acc = round((v_rec / v_tot) * 100.0, 1)
            v_fb = round(100.0 - v_acc, 1)
            rows.append([i_id, name, cat, d_str, v_tot, v_rec, v_acc, v_fb])
    with open(DATA_DIR / "intent_recognition_accuracy.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_containment_deflections():
    headers = ["date", "total_bot_sessions", "contained_sessions", "containment_rate_pct", "target_containment_pct", "deflected_cost_savings"]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        tot = 1250 + (day % 7) * 25 - 75
        cont = int(tot * (0.67 + ((day % 4) - 1.5) * 0.015))
        rate = round((cont / tot) * 100.0, 1)
        savings = round(cont * 4.50, 2) # $4.50 cost saving per deflected contact
        rows.append([d_str, tot, cont, rate, 65.0, savings])
    with open(DATA_DIR / "containment_deflections.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_human_escalation_logs():
    headers = ["escalation_id", "conversation_id", "escalation_timestamp", "trigger_reason", "transferred_to_queue", "agent_resolution_time_seconds"]
    rows = [
        ["ESC-901", "BOT-702", "2026-08-05 10:33:30", "Sentiment Drop to Negative", "Q-101", 280],
        ["ESC-902", "BOT-705", "2026-08-04 16:47:00", "Complex Policy Exception", "Q-101", 340],
        ["ESC-903", "BOT-688", "2026-08-04 12:15:20", "User Explicitly Requested Human", "Q-104", 195],
        ["ESC-904", "BOT-660", "2026-08-03 15:22:10", "Intent Recognition Fallback Limit Reached", "Q-102", 420],
        ["ESC-905", "BOT-640", "2026-08-02 18:05:40", "High Value VIP Customer Detected", "Q-106", 180],
    ]
    with open(DATA_DIR / "human_escalation_logs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_bot_conversations()
    generate_intent_recognition_accuracy()
    generate_containment_deflections()
    generate_human_escalation_logs()
    print("ai_chatbot_deflection_handoff seed data generated.")

if __name__ == "__main__":
    main()
