#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Restricted Substances (RSL) & Chemical Safety agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

RSL_RESULTS = [
    {"test_id": "RSL-2026-001", "sku": "SKU-001", "vendor_id": "VEND-1001", "lab_name": "SGS Consumer Testing", "test_date": "2026-02-10", "chemical_substance_tested": "Formaldehyde", "detected_ppm": 4.2, "threshold_ppm": 16.0, "pass_fail_status": "Pass"},
    {"test_id": "RSL-2026-002", "sku": "SKU-001", "vendor_id": "VEND-1001", "lab_name": "SGS Consumer Testing", "test_date": "2026-02-10", "chemical_substance_tested": "Azo Dyes (Arylamines)", "detected_ppm": 0.0, "threshold_ppm": 20.0, "pass_fail_status": "Pass"},
    {"test_id": "RSL-2026-003", "sku": "SKU-002", "vendor_id": "VEND-1001", "lab_name": "Intertek Labtech", "test_date": "2026-03-15", "chemical_substance_tested": "Total PFAS (Fluorine)", "detected_ppm": 12.0, "threshold_ppm": 50.0, "pass_fail_status": "Pass - Approaching Threshold"},
    {"test_id": "RSL-2026-004", "sku": "SKU-002", "vendor_id": "VEND-1001", "lab_name": "Intertek Labtech", "test_date": "2026-03-15", "chemical_substance_tested": "Antimony Trioxide", "detected_ppm": 85.0, "threshold_ppm": 260.0, "pass_fail_status": "Pass"},
    {"test_id": "RSL-2026-005", "sku": "SKU-004", "vendor_id": "VEND-1003", "lab_name": "Bureau Veritas Clean", "test_date": "2026-04-12", "chemical_substance_tested": "1,4-Dioxane", "detected_ppm": 0.45, "threshold_ppm": 1.0, "pass_fail_status": "Pass"},
    {"test_id": "RSL-2026-006", "sku": "SKU-004", "vendor_id": "VEND-1003", "lab_name": "Bureau Veritas Clean", "test_date": "2026-04-12", "chemical_substance_tested": "Phthalates (DEHP, DBP)", "detected_ppm": 0.0, "threshold_ppm": 50.0, "pass_fail_status": "Pass"},
    {"test_id": "RSL-2026-007", "sku": "SKU-006", "vendor_id": "VEND-1002", "lab_name": "TUV SUD America", "test_date": "2026-05-08", "chemical_substance_tested": "Lead & Cadmium Extraction", "detected_ppm": 0.02, "threshold_ppm": 0.5, "pass_fail_status": "Pass"},
    {"test_id": "RSL-2026-008", "sku": "SKU-006", "vendor_id": "VEND-1002", "lab_name": "TUV SUD America", "test_date": "2026-05-08", "chemical_substance_tested": "BPA / Bisphenols", "detected_ppm": 0.0, "threshold_ppm": 0.1, "pass_fail_status": "Pass"},
]

CERTIFICATES = [
    {"cert_id": "CERT-OEKO-01", "vendor_id": "VEND-1001", "standard_name": "OEKO-TEX Standard 100 Class I", "issue_date": "2025-08-01", "expiration_date": "2026-08-01", "certification_body": "TESTEX Swiss Textile-Testing", "cert_status": "Active - Renewal In Progress", "audits_covered": "Apparel & Raw Fabrics"},
    {"cert_id": "CERT-GOTS-02", "vendor_id": "VEND-1001", "standard_name": "Global Organic Textile Standard (GOTS)", "issue_date": "2025-10-15", "expiration_date": "2026-10-15", "certification_body": "Control Union Certifications", "cert_status": "Active & Valid", "audits_covered": "Organic Cotton Line"},
    {"cert_id": "CERT-EPA-03", "vendor_id": "VEND-1003", "standard_name": "EPA Safer Choice Certified", "issue_date": "2025-06-20", "expiration_date": "2028-06-20", "certification_body": "US EPA Safer Choice Program", "cert_status": "Active & Valid", "audits_covered": "Eco Detergents & Cleaners"},
    {"cert_id": "CERT-CRADLE-04", "vendor_id": "VEND-1002", "standard_name": "Cradle to Cradle Certified Gold", "issue_date": "2025-11-01", "expiration_date": "2027-11-01", "certification_body": "C2CPII Institute", "cert_status": "Active & Valid", "audits_covered": "Drinkware & Food Packaging"},
]

PROP65_REACH = [
    {"screening_id": "SCR-2026-01", "sku": "SKU-001", "category": "Apparel", "svhc_substance_flag": False, "prop65_warning_required": False, "reach_annex_xvii_compliant": True, "safety_data_sheet_on_file": True},
    {"screening_id": "SCR-2026-02", "sku": "SKU-002", "category": "Apparel", "svhc_substance_flag": False, "prop65_warning_required": False, "reach_annex_xvii_compliant": True, "safety_data_sheet_on_file": True},
    {"screening_id": "SCR-2026-03", "sku": "SKU-003", "category": "Kitchenware", "svhc_substance_flag": False, "prop65_warning_required": False, "reach_annex_xvii_compliant": True, "safety_data_sheet_on_file": True},
    {"screening_id": "SCR-2026-04", "sku": "SKU-004", "category": "Home Cleaning", "svhc_substance_flag": False, "prop65_warning_required": False, "reach_annex_xvii_compliant": True, "safety_data_sheet_on_file": True},
    {"screening_id": "SCR-2026-05", "sku": "SKU-005", "category": "Electronics", "svhc_substance_flag": False, "prop65_warning_required": True, "reach_annex_xvii_compliant": True, "safety_data_sheet_on_file": True},
    {"screening_id": "SCR-2026-06", "sku": "SKU-006", "category": "Drinkware", "svhc_substance_flag": False, "prop65_warning_required": False, "reach_annex_xvii_compliant": True, "safety_data_sheet_on_file": True},
]

PHASEOUT_PLANS = [
    {"program_id": "PHASE-PFAS-01", "chemical_group": "PFAS Forever Chemicals (DWR coatings)", "target_phaseout_date": "2026-12-31", "affected_skus_count": 18, "safer_alternative_substance": "Bio-based Fluorine-Free Polyurethane DWR", "migration_progress_pct": 85.0, "phaseout_status": "On Track - Final Validation"},
    {"program_id": "PHASE-PVC-02", "chemical_group": "Polyvinyl Chloride (PVC) Packaging Blisters", "target_phaseout_date": "2026-09-30", "affected_skus_count": 34, "safer_alternative_substance": "Recycled PET / Molded Cellulose Fiber", "migration_progress_pct": 94.0, "phaseout_status": "Near Completion"},
    {"program_id": "PHASE-BPA-03", "chemical_group": "Bisphenol Epoxies in Can Liners", "target_phaseout_date": "2026-06-30", "affected_skus_count": 12, "safer_alternative_substance": "Acrylic & Polyester Non-BPA Resins", "migration_progress_pct": 100.0, "phaseout_status": "Completed & Verified"},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(RSL_RESULTS, "rsl_testing_results.csv")
    generate_csv(CERTIFICATES, "chemical_compliance_certificates.csv")
    generate_csv(PROP65_REACH, "prop65_reach_screenings.csv")
    generate_csv(PHASEOUT_PLANS, "hazardous_phaseout_plans.csv")

if __name__ == "__main__":
    main()
