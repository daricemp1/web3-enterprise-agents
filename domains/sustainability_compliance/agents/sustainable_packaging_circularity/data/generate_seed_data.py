#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Sustainable Packaging & Circularity agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

PACKAGING_SPECS = [
    {"sku": "SKU-001", "packaging_component": "Garment Polybag", "material_type": "Bio-based PLA", "total_weight_grams": 15.2, "is_curbside_recyclable": False, "forest_certified_fsc": False, "plastic_resin_code": "7-OTHER"},
    {"sku": "SKU-001", "packaging_component": "Hangtag & Cord", "material_type": "Recycled Kraft Paper", "total_weight_grams": 4.5, "is_curbside_recyclable": True, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
    {"sku": "SKU-002", "packaging_component": "Outer Shipper Bag", "material_type": "100% Recycled Ocean Plastic", "total_weight_grams": 28.0, "is_curbside_recyclable": True, "forest_certified_fsc": False, "plastic_resin_code": "4-LDPE"},
    {"sku": "SKU-002", "packaging_component": "Inner Protective Sleeve", "material_type": "FSC Certified Glassine", "total_weight_grams": 8.0, "is_curbside_recyclable": True, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
    {"sku": "SKU-003", "packaging_component": "Molded Pulp Tray", "material_type": "Bagasse Sugarcane Fiber", "total_weight_grams": 45.0, "is_curbside_recyclable": True, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
    {"sku": "SKU-003", "packaging_component": "Display Carton", "material_type": "FSC Recycled Corrugate", "total_weight_grams": 65.0, "is_curbside_recyclable": True, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
    {"sku": "SKU-004", "packaging_component": "Detergent Bottle", "material_type": "100% Post-Consumer HDPE", "total_weight_grams": 82.0, "is_curbside_recyclable": True, "forest_certified_fsc": False, "plastic_resin_code": "2-HDPE"},
    {"sku": "SKU-004", "packaging_component": "Dispensing Cap", "material_type": "Monomaterial Polypropylene", "total_weight_grams": 14.0, "is_curbside_recyclable": True, "forest_certified_fsc": False, "plastic_resin_code": "5-PP"},
    {"sku": "SKU-005", "packaging_component": "Appliance Cushion", "material_type": "Mushroom Mycelium Foam", "total_weight_grams": 110.0, "is_curbside_recyclable": False, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
    {"sku": "SKU-005", "packaging_component": "Master Carton", "material_type": "FSC Double-Wall Kraft", "total_weight_grams": 240.0, "is_curbside_recyclable": True, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
    {"sku": "SKU-006", "packaging_component": "Tumbler Box", "material_type": "FSC Recycled Folding Board", "total_weight_grams": 35.0, "is_curbside_recyclable": True, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
    {"sku": "SKU-006", "packaging_component": "Protective Wrapper", "material_type": "FSC Tissue Paper", "total_weight_grams": 3.0, "is_curbside_recyclable": True, "forest_certified_fsc": True, "plastic_resin_code": "N/A"},
]

PCR_CONTENT = [
    {"sku": "SKU-001", "category": "Apparel", "vendor_id": "VEND-1001", "primary_pcr_pct": 50.0, "secondary_corrugate_pcr_pct": 85.0, "target_pcr_pct": 60.0, "compliance_status": "Meeting Target"},
    {"sku": "SKU-002", "category": "Apparel", "vendor_id": "VEND-1001", "primary_pcr_pct": 100.0, "secondary_corrugate_pcr_pct": 90.0, "target_pcr_pct": 80.0, "compliance_status": "Exceeding Target"},
    {"sku": "SKU-003", "category": "Kitchenware", "vendor_id": "VEND-1003", "primary_pcr_pct": 75.0, "secondary_corrugate_pcr_pct": 85.0, "target_pcr_pct": 70.0, "compliance_status": "Exceeding Target"},
    {"sku": "SKU-004", "category": "Home Cleaning", "vendor_id": "VEND-1003", "primary_pcr_pct": 100.0, "secondary_corrugate_pcr_pct": 100.0, "target_pcr_pct": 100.0, "compliance_status": "Fully Compliant"},
    {"sku": "SKU-005", "category": "Electronics", "vendor_id": "VEND-1004", "primary_pcr_pct": 35.0, "secondary_corrugate_pcr_pct": 70.0, "target_pcr_pct": 50.0, "compliance_status": "Under Review"},
    {"sku": "SKU-006", "category": "Drinkware", "vendor_id": "VEND-1002", "primary_pcr_pct": 80.0, "secondary_corrugate_pcr_pct": 95.0, "target_pcr_pct": 75.0, "compliance_status": "Exceeding Target"},
]

SINGLE_USE_PLASTIC = [
    {"quarter": "2026-Q1", "store_id_or_dc": "DC-101", "plastic_polybags_eliminated": 245000, "eps_foam_replaced_units": 45000, "plastic_bubble_avoided_sqft": 185000, "virgin_plastic_reduction_tons": 18.5},
    {"quarter": "2026-Q2", "store_id_or_dc": "DC-101", "plastic_polybags_eliminated": 290000, "eps_foam_replaced_units": 52000, "plastic_bubble_avoided_sqft": 210000, "virgin_plastic_reduction_tons": 21.8},
    {"quarter": "2026-Q1", "store_id_or_dc": "DC-102", "plastic_polybags_eliminated": 180000, "eps_foam_replaced_units": 34000, "plastic_bubble_avoided_sqft": 140000, "virgin_plastic_reduction_tons": 14.2},
    {"quarter": "2026-Q2", "store_id_or_dc": "DC-102", "plastic_polybags_eliminated": 215000, "eps_foam_replaced_units": 39000, "plastic_bubble_avoided_sqft": 165000, "virgin_plastic_reduction_tons": 16.9},
    {"quarter": "2026-Q1", "store_id_or_dc": "STORE-101", "plastic_polybags_eliminated": 45000, "eps_foam_replaced_units": 0, "plastic_bubble_avoided_sqft": 12000, "virgin_plastic_reduction_tons": 2.4},
    {"quarter": "2026-Q2", "store_id_or_dc": "STORE-101", "plastic_polybags_eliminated": 52000, "eps_foam_replaced_units": 0, "plastic_bubble_avoided_sqft": 15000, "virgin_plastic_reduction_tons": 2.8},
    {"quarter": "2026-Q1", "store_id_or_dc": "STORE-102", "plastic_polybags_eliminated": 48000, "eps_foam_replaced_units": 0, "plastic_bubble_avoided_sqft": 14000, "virgin_plastic_reduction_tons": 2.6},
    {"quarter": "2026-Q2", "store_id_or_dc": "STORE-102", "plastic_polybags_eliminated": 56000, "eps_foam_replaced_units": 0, "plastic_bubble_avoided_sqft": 18000, "virgin_plastic_reduction_tons": 3.1},
]

REUSABLE_TOTES = [
    {"tote_id": "TOTE-001", "current_dc_id": "DC-101", "assigned_store_id": "STORE-101", "cycle_turns_count": 84, "initial_deployment_date": "2025-03-15", "condition_status": "Excellent", "plastic_weight_saved_lbs": 336.0},
    {"tote_id": "TOTE-002", "current_dc_id": "DC-101", "assigned_store_id": "STORE-101", "cycle_turns_count": 92, "initial_deployment_date": "2025-02-10", "condition_status": "Good", "plastic_weight_saved_lbs": 368.0},
    {"tote_id": "TOTE-003", "current_dc_id": "DC-101", "assigned_store_id": "STORE-102", "cycle_turns_count": 76, "initial_deployment_date": "2025-04-01", "condition_status": "Good", "plastic_weight_saved_lbs": 304.0},
    {"tote_id": "TOTE-004", "current_dc_id": "DC-101", "assigned_store_id": "STORE-103", "cycle_turns_count": 68, "initial_deployment_date": "2025-05-12", "condition_status": "Excellent", "plastic_weight_saved_lbs": 272.0},
    {"tote_id": "TOTE-005", "current_dc_id": "DC-102", "assigned_store_id": "STORE-104", "cycle_turns_count": 110, "initial_deployment_date": "2024-11-20", "condition_status": "Fair - Maintenance Needed", "plastic_weight_saved_lbs": 440.0},
    {"tote_id": "TOTE-006", "current_dc_id": "DC-102", "assigned_store_id": "STORE-105", "cycle_turns_count": 95, "initial_deployment_date": "2025-01-18", "condition_status": "Good", "plastic_weight_saved_lbs": 380.0},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(PACKAGING_SPECS, "packaging_material_specs.csv")
    generate_csv(PCR_CONTENT, "pcr_recycled_content_pct.csv")
    generate_csv(SINGLE_USE_PLASTIC, "single_use_plastic_elimination.csv")
    generate_csv(REUSABLE_TOTES, "reusable_tote_cycles.csv")

if __name__ == "__main__":
    main()
