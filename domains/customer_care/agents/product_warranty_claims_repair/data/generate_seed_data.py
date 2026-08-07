"""Generate synthetic seed CSV data for Customer Care: Product Warranty & Claims."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_warranty_registrations():
    headers = ["registration_id", "customer_id", "sku", "product_name", "purchase_date", "warranty_type", "warranty_status", "coverage_end_date"]
    rows = [
        ["WAR-1001", "CUST-1001", "SKU-003", "Wireless Noise-Cancelling Earbuds", "2025-11-15", "Extended 2-Year", "Active", "2027-11-15"],
        ["WAR-1002", "CUST-1002", "SKU-001", "Waterproof Shell Jacket", "2026-01-10", "Standard Manufacturer", "Active", "2027-01-10"],
        ["WAR-1003", "CUST-1003", "SKU-005", "Smart Fitness Tracker Watch", "2025-08-20", "Accidental Protection", "Active", "2027-08-20"],
        ["WAR-1004", "CUST-1004", "SKU-002", "Trail Running Shoes", "2026-03-05", "Standard Manufacturer", "Active", "2026-09-05"],
        ["WAR-1005", "CUST-1005", "SKU-003", "Wireless Noise-Cancelling Earbuds", "2024-07-12", "Extended 2-Year", "Expired", "2026-07-12"],
        ["WAR-1006", "CUST-1006", "SKU-005", "Smart Fitness Tracker Watch", "2026-02-18", "Extended 2-Year", "Active", "2028-02-18"],
    ]
    with open(DATA_DIR / "warranty_registrations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_repair_claims_processed():
    headers = ["claim_id", "registration_id", "sku", "claim_date", "issue_description", "claim_status", "repair_center_id", "turnaround_days", "repair_cost"]
    rows = [
        ["CLM-801", "WAR-1001", "SKU-003", "2026-07-28", "Right earbud no audio output", "Completed / Returned", "RC-EAST-01", 4, 38.50],
        ["CLM-802", "WAR-1002", "SKU-001", "2026-07-30", "Waterproof seam seal delamination", "In Repair", "RC-MIDW-02", 3, 24.00],
        ["CLM-803", "WAR-1003", "SKU-005", "2026-08-01", "Cracked OLED display glass", "Replaced with New Unit", "RC-WEST-01", 2, 85.00],
        ["CLM-804", "WAR-1006", "SKU-005", "2026-08-02", "Heart rate sensor failure", "Approved - In Transit", "RC-EAST-01", 1, 45.00],
        ["CLM-805", "WAR-1004", "SKU-002", "2026-07-20", "Outsole tread detached", "Completed / Returned", "RC-MIDW-02", 5, 20.00],
    ]
    with open(DATA_DIR / "repair_claims_processed.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_vendor_warranty_recovery():
    headers = ["recovery_id", "vendor_id", "vendor_name", "claim_id", "billed_to_vendor_amount", "recovered_amount", "recovery_date", "settlement_status"]
    rows = [
        ["REC-901", "VEND-1001", "Apex Audio & Electronics", "CLM-801", 38.50, 38.50, "2026-08-02", "Settled 100%"],
        ["REC-902", "VEND-1002", "Summit Outdoor Gear Corp", "CLM-802", 24.00, 20.40, "2026-08-04", "Settled 85% - Net Dispute"],
        ["REC-903", "VEND-1001", "Apex Audio & Electronics", "CLM-803", 85.00, 85.00, "2026-08-05", "Settled 100%"],
        ["REC-904", "VEND-1003", "AeroTech Footwear Ltd", "CLM-805", 20.00, 18.00, "2026-07-28", "Settled 90%"],
        ["REC-905", "VEND-1004", "Nordic Living Essentials", "CLM-790", 42.00, 42.00, "2026-07-25", "Settled 100%"],
    ]
    with open(DATA_DIR / "vendor_warranty_recovery.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_replacement_costs():
    headers = ["sku", "product_category", "avg_unit_replacement_cost", "avg_repair_cost", "claims_volume_ytd", "total_warranty_expense_ytd"]
    rows = [
        ["SKU-001", "Apparel & Outerwear", 85.00, 24.00, 142, 5840.00],
        ["SKU-002", "Footwear", 65.00, 20.00, 188, 5210.00],
        ["SKU-003", "Consumer Electronics", 95.00, 38.50, 310, 16850.00],
        ["SKU-004", "Basics & Apparel", 22.00, 8.00, 65, 940.00],
        ["SKU-005", "Wearable Tech", 120.00, 48.00, 245, 18200.00],
        ["SKU-006", "Home & Hydration", 18.00, 6.00, 40, 420.00],
    ]
    with open(DATA_DIR / "replacement_costs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_warranty_registrations()
    generate_repair_claims_processed()
    generate_vendor_warranty_recovery()
    generate_replacement_costs()
    print("product_warranty_claims_repair seed data generated.")

if __name__ == "__main__":
    main()
