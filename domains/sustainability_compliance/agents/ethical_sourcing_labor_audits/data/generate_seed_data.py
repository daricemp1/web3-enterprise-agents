#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Ethical Sourcing & Labor Audits agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

SOCIAL_AUDITS = [
    {"vendor_id": "VEND-1001", "facility_location": "Vietnam - Binh Duong Facility", "audit_date": "2026-03-12", "audit_firm": "Bureau Veritas", "audit_type": "SMETA 4-Pillar", "audit_score": 94.5, "audit_rating": "A - Full Compliance", "re_audit_due_date": "2028-03-12"},
    {"vendor_id": "VEND-1001", "facility_location": "Cambodia - Phnom Penh Plant", "audit_date": "2026-04-18", "audit_firm": "Intertek", "audit_type": "SMETA 4-Pillar", "audit_score": 88.0, "audit_rating": "B - Minor Corrective Action", "re_audit_due_date": "2027-04-18"},
    {"vendor_id": "VEND-1002", "facility_location": "USA - Ohio Packaging Works", "audit_date": "2026-01-20", "audit_firm": "SGS Global", "audit_type": "Sedex 2-Pillar", "audit_score": 98.0, "audit_rating": "A - Full Compliance", "re_audit_due_date": "2029-01-20"},
    {"vendor_id": "VEND-1003", "facility_location": "Mexico - Monterrey Clean Plant", "audit_date": "2026-02-14", "audit_firm": "Elevance Audit", "audit_type": "SMETA 4-Pillar", "audit_score": 91.5, "audit_rating": "A - Full Compliance", "re_audit_due_date": "2028-02-14"},
    {"vendor_id": "VEND-1004", "facility_location": "Taiwan - Hsinchu Tech Park", "audit_date": "2026-05-10", "audit_firm": "TUV Rheinland", "audit_type": "RBA Validated Audit", "audit_score": 95.0, "audit_rating": "A - Full Compliance", "re_audit_due_date": "2028-05-10"},
    {"vendor_id": "VEND-1004", "facility_location": "Malaysia - Penang Assembly", "audit_date": "2026-06-05", "audit_firm": "SGS Global", "audit_type": "RBA Validated Audit", "audit_score": 84.0, "audit_rating": "B - Minor Corrective Action", "re_audit_due_date": "2027-06-05"},
]

SEDEX_SCORES = [
    {"vendor_id": "VEND-1001", "smeta_pillar": "Labor Standards", "labor_standards_score": 92.0, "health_safety_score": 94.0, "environment_score": 96.0, "business_ethics_score": 95.0, "overall_sedex_grade": "A"},
    {"vendor_id": "VEND-1002", "smeta_pillar": "Health & Safety", "labor_standards_score": 98.0, "health_safety_score": 99.0, "environment_score": 97.0, "business_ethics_score": 98.0, "overall_sedex_grade": "A+"},
    {"vendor_id": "VEND-1003", "smeta_pillar": "Environment", "labor_standards_score": 90.0, "health_safety_score": 92.0, "environment_score": 94.0, "business_ethics_score": 91.0, "overall_sedex_grade": "A"},
    {"vendor_id": "VEND-1004", "smeta_pillar": "Business Ethics", "labor_standards_score": 86.0, "health_safety_score": 88.0, "environment_score": 89.0, "business_ethics_score": 87.0, "overall_sedex_grade": "B"},
]

ZERO_TOLERANCE = [
    {"violation_id": "ZT-2025-001", "vendor_id": "VEND-1001", "facility_country": "Cambodia", "violation_category": "Overtime Policy Discrepancy", "discovery_date": "2025-11-10", "root_cause": "Peak Season Shift Scheduling Misalignment", "immediate_action_taken": "Immediate shift capping at 60 hrs/week and back-pay disbursement", "remediation_status": "Closed & Verified"},
    {"violation_id": "ZT-2026-000", "vendor_id": "VEND-1004", "facility_country": "Malaysia", "violation_category": "Foreign Worker Passport Retention", "discovery_date": "2026-01-15", "root_cause": "3P Labor Agency Passport Holding Practice", "immediate_action_taken": "100% Passports returned immediately, agency contract terminated, individual secure lockers installed", "remediation_status": "Closed & Verified"},
]

CORRECTIVE_ACTIONS = [
    {"cap_id": "CAP-101", "vendor_id": "VEND-1001", "non_conformance_issue": "Emergency Exit Signage Blocked in Warehouse C", "severity": "Medium", "issue_date": "2026-04-18", "target_closure_date": "2026-05-18", "actual_closure_date": "2026-05-02", "verification_status": "Resolved & Closed"},
    {"cap_id": "CAP-102", "vendor_id": "VEND-1001", "non_conformance_issue": "Eye-Wash Station Inspection Log Gap", "severity": "Low", "issue_date": "2026-04-18", "target_closure_date": "2026-05-30", "actual_closure_date": "2026-05-10", "verification_status": "Resolved & Closed"},
    {"cap_id": "CAP-103", "vendor_id": "VEND-1004", "non_conformance_issue": "Chemical Secondary Containment Pallet Crack", "severity": "Medium", "issue_date": "2026-06-05", "target_closure_date": "2026-07-05", "actual_closure_date": "2026-06-20", "verification_status": "Resolved & Closed"},
    {"cap_id": "CAP-104", "vendor_id": "VEND-1004", "non_conformance_issue": "Noise Level Signage Missing in Stamping Bay", "severity": "Low", "issue_date": "2026-06-05", "target_closure_date": "2026-07-15", "actual_closure_date": "2026-07-01", "verification_status": "Resolved & Closed"},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(SOCIAL_AUDITS, "supplier_social_audits.csv")
    generate_csv(SEDEX_SCORES, "sedex_smeta_scores.csv")
    generate_csv(ZERO_TOLERANCE, "zero_tolerance_violations.csv")
    generate_csv(CORRECTIVE_ACTIONS, "corrective_action_plans.csv")

if __name__ == "__main__":
    main()
