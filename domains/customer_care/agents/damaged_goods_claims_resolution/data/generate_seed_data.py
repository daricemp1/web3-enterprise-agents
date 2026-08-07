"""Generate synthetic seed CSV data for Customer Care: Damaged Goods Claims & Recovery."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_damage_photo_submissions():
    headers = ["claim_id", "order_id", "customer_id", "submission_date", "sku", "damage_type", "photo_verification_status", "claim_validity_confidence"]
    rows = [
        ["DMG-501", "ORD-89410", "CUST-1001", "2026-08-05", "SKU-006", "Broken Glass / Shattered", "Verified by Computer Vision AI", 0.98],
        ["DMG-502", "ORD-89380", "CUST-1002", "2026-08-04", "SKU-001", "Crushed Exterior Box & Torn Fabric", "Verified by Computer Vision AI", 0.94],
        ["DMG-503", "ORD-89320", "CUST-1003", "2026-08-03", "SKU-003", "Water / Liquid Damage to Electronics", "Verified by Agent", 0.91],
        ["DMG-504", "ORD-89290", "CUST-1004", "2026-08-02", "SKU-005", "Cracked Watch Bezel", "Verified by Computer Vision AI", 0.96],
        ["DMG-505", "ORD-89240", "CUST-1005", "2026-08-01", "SKU-002", "Scuffed & Punctured Shoe Leather", "Verified by Agent", 0.88],
    ]
    with open(DATA_DIR / "damage_photo_submissions.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_carrier_damage_claims():
    headers = ["carrier_claim_id", "internal_claim_id", "carrier_code", "tracking_number", "claim_filed_date", "claimed_amount", "carrier_payout_amount", "settlement_status", "turnaround_days"]
    rows = [
        ["CAR-CLM-101", "DMG-501", "FedEx", "TRK-FDX-8801", "2026-08-05", 45.00, 45.00, "Approved & Paid", 2],
        ["CAR-CLM-102", "DMG-502", "UPS", "TRK-UPS-8802", "2026-08-04", 145.00, 116.00, "Settled (80% Payout)", 3],
        ["CAR-CLM-103", "DMG-503", "USPS", "TRK-USP-8803", "2026-08-03", 95.00, 95.00, "Approved & Paid", 4],
        ["CAR-CLM-104", "DMG-504", "FedEx", "TRK-FDX-8804", "2026-08-02", 120.00, 120.00, "Approved & Paid", 2],
        ["CAR-CLM-105", "DMG-505", "DHL", "TRK-DHL-8805", "2026-08-01", 65.00, 52.00, "Settled (80% Payout)", 5],
    ]
    with open(DATA_DIR / "carrier_damage_claims.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_customer_replacement_orders():
    headers = ["replacement_order_id", "original_order_id", "customer_id", "sku", "replacement_approved_date", "replacement_dispatched_date", "dispatch_lead_time_hours", "shipping_expedited"]
    rows = [
        ["RPL-901", "ORD-89410", "CUST-1001", "SKU-006", "2026-08-05 10:15:00", "2026-08-05 16:30:00", 6.2, True],
        ["RPL-902", "ORD-89380", "CUST-1002", "SKU-001", "2026-08-04 11:30:00", "2026-08-04 19:00:00", 7.5, True],
        ["RPL-903", "ORD-89320", "CUST-1003", "SKU-003", "2026-08-03 14:00:00", "2026-08-03 21:15:00", 7.2, True],
        ["RPL-904", "ORD-89290", "CUST-1004", "SKU-005", "2026-08-02 09:45:00", "2026-08-02 15:30:00", 5.7, True],
        ["RPL-905", "ORD-89240", "CUST-1005", "SKU-002", "2026-08-01 13:00:00", "2026-08-01 22:00:00", 9.0, True],
    ]
    with open(DATA_DIR / "customer_replacement_orders.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_salvage_disposition():
    headers = ["salvage_id", "sku", "category", "damaged_units_count", "disposition_type", "salvage_recovery_amount", "original_retail_value"]
    rows = [
        ["SAL-401", "SKU-001", "Apparel & Outerwear", 28, "Liquidated / Secondary Market", 1120.00, 3920.00],
        ["SAL-402", "SKU-002", "Footwear", 18, "Liquidated / Secondary Market", 540.00, 1800.00],
        ["SAL-403", "SKU-003", "Consumer Electronics", 35, "Recycled E-Waste Recovery", 700.00, 4200.00],
        ["SAL-404", "SKU-005", "Wearable Tech", 22, "Refurbished Secondary Grade B", 1320.00, 3300.00],
        ["SAL-405", "SKU-006", "Home & Hydration", 15, "Destroyed & Scrapped", 0.00, 450.00],
    ]
    with open(DATA_DIR / "salvage_disposition.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_damage_photo_submissions()
    generate_carrier_damage_claims()
    generate_customer_replacement_orders()
    generate_salvage_disposition()
    print("damaged_goods_claims_resolution seed data generated.")

if __name__ == "__main__":
    main()
