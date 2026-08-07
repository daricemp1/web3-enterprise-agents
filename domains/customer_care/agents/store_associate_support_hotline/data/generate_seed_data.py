"""Generate synthetic seed CSV data for Customer Care: Store Helpdesk & POS Support."""
import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).parent

def generate_store_helpdesk_tickets():
    headers = ["ticket_id", "store_id", "ticket_created_timestamp", "category", "urgency", "status", "resolved_timestamp", "resolution_duration_minutes"]
    rows = [
        ["HD-1001", "STORE-101", "2026-08-05 08:30:00", "POS Terminal Freeze", "Critical", "Resolved", "2026-08-05 08:48:00", 18],
        ["HD-1002", "STORE-102", "2026-08-05 10:15:00", "Barcode Scanner Disconnected", "Medium", "Resolved", "2026-08-05 10:35:00", 20],
        ["HD-1003", "STORE-103", "2026-08-04 14:00:00", "PIN Pad EMV Failure", "High", "Resolved", "2026-08-04 14:24:00", 24],
        ["HD-1004", "STORE-104", "2026-08-04 16:20:00", "Store Backroom Wi-Fi Drop", "High", "Resolved", "2026-08-04 16:50:00", 30],
        ["HD-1005", "STORE-105", "2026-08-03 11:10:00", "Inventory Zebra Scanner Sync", "Low", "Resolved", "2026-08-03 11:45:00", 35],
        ["HD-1006", "STORE-101", "2026-08-02 09:00:00", "Receipt Printer Jam & Driver Bug", "Medium", "Resolved", "2026-08-02 09:22:00", 22],
    ]
    with open(DATA_DIR / "store_helpdesk_tickets.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_pos_hardware_outages():
    headers = ["outage_id", "store_id", "terminal_id", "outage_date", "hardware_type", "impacted_checkout_lanes", "lane_downtime_hours", "estimated_lost_transactions"]
    rows = [
        ["OUT-301", "STORE-101", "POS-01", "2026-08-05", "Mainboard Power Supply", 1, 1.2, 28],
        ["OUT-302", "STORE-102", "POS-04", "2026-08-04", "Ingenico PIN Pad Crash", 1, 0.8, 15],
        ["OUT-303", "STORE-103", "SCO-02", "2026-08-03", "Self-Checkout Weight Scale Fault", 1, 2.5, 65],
        ["OUT-304", "STORE-104", "POS-02", "2026-08-02", "Zebra 2D Scanner Failure", 1, 0.5, 10],
        ["OUT-305", "STORE-105", "POS-03", "2026-08-01", "Epson Thermal Printer Cutter Jam", 1, 0.6, 12],
    ]
    with open(DATA_DIR / "pos_hardware_outages.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_ticket_mttr_by_region():
    headers = ["region", "date", "total_store_tickets", "avg_mttr_minutes", "critical_p1_mttr_minutes", "target_mttr_minutes", "sla_met_pct"]
    regions = [
        ("Northeast", 48, 22.5, 18.0, 30.0, 95.8),
        ("Southeast", 42, 24.0, 19.5, 30.0, 93.5),
        ("Midwest", 38, 21.0, 16.5, 30.0, 97.2),
        ("West Coast", 55, 26.5, 22.0, 30.0, 90.9),
        ("Southwest", 34, 23.0, 17.5, 30.0, 94.1),
    ]
    base_date = datetime(2026, 8, 6)
    rows = []
    for day in range(30):
        d_str = (base_date - timedelta(days=day)).strftime("%Y-%m-%d")
        for reg, tot, mttr, p1_mttr, tgt, sla in regions:
            v_tot = tot + (day % 5) * 3 - 6
            v_mttr = round(mttr + ((day % 3) - 1) * 0.8, 1)
            v_p1 = round(p1_mttr + ((day % 3) - 1) * 0.6, 1)
            v_sla = round(sla + ((day % 4) - 1.5) * 0.5, 1)
            rows.append([reg, d_str, v_tot, v_mttr, v_p1, tgt, v_sla])
    with open(DATA_DIR / "ticket_mttr_by_region.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def generate_recurring_system_bugs():
    headers = ["bug_id", "system_component", "description", "incident_count_30d", "impacted_stores_count", "jira_fix_status", "workaround_provided"]
    rows = [
        ["BUG-401", "POS Checkout Client v4.2", "Memory leak during continuous coupon barcode scans", 64, 42, "In QA Testing - Patch v4.2.1", "Restart POS client during mid-day shift change"],
        ["BUG-402", "Payment Gateway Pinpad Driver", "Intermittent contactless NFC timeout on Apple Pay", 48, 35, "Under Engineering Investigation", "Prompt customer to insert physical chip"],
        ["BUG-403", "BOPIS Store Handheld App", "Inventory barcode scan latency exceeding 3 seconds", 38, 28, "Fix Scheduled for Release v2.8", "Clear local cache on Zebra handhelds"],
        ["BUG-404", "Gift Card Balance Inquire Module", "Timeout error on magnetic stripe swipe verification", 22, 18, "Patch Deployed to Production", "Manual numeric card entry via touch keyboard"],
    ]
    with open(DATA_DIR / "recurring_system_bugs.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def main():
    generate_store_helpdesk_tickets()
    generate_pos_hardware_outages()
    generate_ticket_mttr_by_region()
    generate_recurring_system_bugs()
    print("store_associate_support_hotline seed data generated.")

if __name__ == "__main__":
    main()
