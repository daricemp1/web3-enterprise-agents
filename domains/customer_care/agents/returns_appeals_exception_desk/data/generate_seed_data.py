"""Generate synthetic seed CSV data for Customer Care: Return Exceptions & Appeals."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_out_of_policy_returns():
    headers = ["appeal_id", "customer_id", "order_id", "sku", "appeal_date", "days_past_return_window", "reason_for_appeal", "decision", "override_manager_id"]
    rows = [
        ["APL-501", "CUST-1001", "ORD-89210", "SKU-001", "2026-08-05", 14, "Customer was traveling overseas for business", "Approved - Full Refund", "MGR-201"],
        ["APL-502", "CUST-1002", "ORD-89150", "SKU-002", "2026-08-04", 45, "Gift received without gift receipt", "Approved - Store Credit Only", "MGR-202"],
        ["APL-503", "CUST-1003", "ORD-88940", "SKU-003", "2026-08-03", 90, "No proof of purchase or packaging", "Denied", "MGR-201"],
        ["APL-504", "CUST-1004", "ORD-89300", "SKU-005", "2026-08-02", 8, "Item delivered defective upon opening", "Approved - Full Refund", "MGR-203"],
        ["APL-505", "CUST-1005", "ORD-89280", "SKU-004", "2026-08-01", 20, "Wrong color received; missed window due to illness", "Approved - Free Exchange", "MGR-202"],
    ]
    with open(DATA_DIR / "out_of_policy_returns.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_appeasement_exceptions():
    headers = ["exception_id", "appeal_id", "customer_id", "exception_type", "exception_amount", "date"]
    rows = [
        ["EXC-601", "APL-501", "CUST-1001", "Full Refund Override", 145.00, "2026-08-05"],
        ["EXC-602", "APL-502", "CUST-1002", "Store Credit Only", 85.00, "2026-08-04"],
        ["EXC-603", "APL-504", "CUST-1004", "Defective Unit Replacement & Waiver", 120.00, "2026-08-02"],
        ["EXC-604", "APL-505", "CUST-1005", "Restocking Fee Waived", 15.00, "2026-08-01"],
        ["EXC-605", "APL-490", "CUST-1008", "Keep Item Courtesy Credit", 40.00, "2026-07-28"],
    ]
    with open(DATA_DIR / "appeasement_exceptions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_serial_returner_flags():
    headers = ["customer_id", "return_rate_l12m_pct", "total_returns_count", "total_purchases_count", "wardrobing_risk_score", "is_flagged_for_abuse", "account_action_taken"]
    rows = [
        ["CUST-901", 78.5, 44, 56, 88, True, "Restricted to In-Store Returns Only"],
        ["CUST-902", 65.0, 26, 40, 72, True, "Warning Notification Sent"],
        ["CUST-903", 82.0, 50, 61, 94, True, "Free Return Shipping Revoked"],
        ["CUST-904", 25.0, 10, 40, 18, False, "None - Normal Profile"],
        ["CUST-905", 15.0, 6, 40, 10, False, "None - Normal Profile"],
    ]
    with open(DATA_DIR / "serial_returner_flags.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_concession_cost_summary():
    headers = ["date", "category", "total_appeals_reviewed", "approved_appeals_count", "total_concession_dollars", "budget_limit_dollars", "budget_variance_pct"]
    categories = [
        ("Apparel & Outerwear", 45, 34, 2850.00, 3000.00, -5.0),
        ("Footwear", 30, 22, 1980.00, 2000.00, -1.0),
        ("Consumer Electronics", 25, 18, 2650.00, 2500.00, 6.0),
        ("Home & Accessories", 20, 16, 920.00, 1000.00, -8.0),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for cat, tot, app, cost, bgt, var in categories:
            v_tot = tot + (day % 4) * 2 - 4
            v_app = int(v_tot * 0.76)
            v_cost = round(cost + (day % 5) * 40 - 80, 2)
            v_var = round(((v_cost - bgt) / bgt) * 100.0, 1)
            rows.append([d_str, cat, v_tot, v_app, v_cost, bgt, v_var])
    with open(DATA_DIR / "concession_cost_summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_out_of_policy_returns()
    generate_appeasement_exceptions()
    generate_serial_returner_flags()
    generate_concession_cost_summary()
    print("returns_appeals_exception_desk seed data generated.")

if __name__ == "__main__":
    main()
