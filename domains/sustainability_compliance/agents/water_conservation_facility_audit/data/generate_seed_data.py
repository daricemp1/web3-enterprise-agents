#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Water Conservation & Facility Audits agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

WATER_METERS = [
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "meter_month": "2026-01", "potable_water_gallons": 45000, "recycled_water_gallons": 12000, "square_footage": 85000, "water_intensity_gal_per_sqft": 0.53, "water_utility_cost_usd": 680.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "meter_month": "2026-02", "potable_water_gallons": 42000, "recycled_water_gallons": 11500, "square_footage": 85000, "water_intensity_gal_per_sqft": 0.49, "water_utility_cost_usd": 640.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "meter_month": "2026-03", "potable_water_gallons": 48000, "recycled_water_gallons": 14000, "square_footage": 85000, "water_intensity_gal_per_sqft": 0.56, "water_utility_cost_usd": 725.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "meter_month": "2026-04", "potable_water_gallons": 52000, "recycled_water_gallons": 16000, "square_footage": 85000, "water_intensity_gal_per_sqft": 0.61, "water_utility_cost_usd": 790.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "meter_month": "2026-05", "potable_water_gallons": 59000, "recycled_water_gallons": 18500, "square_footage": 85000, "water_intensity_gal_per_sqft": 0.69, "water_utility_cost_usd": 895.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "meter_month": "2026-06", "potable_water_gallons": 68000, "recycled_water_gallons": 22000, "square_footage": 85000, "water_intensity_gal_per_sqft": 0.80, "water_utility_cost_usd": 1040.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "meter_month": "2026-01", "potable_water_gallons": 52000, "recycled_water_gallons": 8000, "square_footage": 95000, "water_intensity_gal_per_sqft": 0.55, "water_utility_cost_usd": 810.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "meter_month": "2026-02", "potable_water_gallons": 49000, "recycled_water_gallons": 7500, "square_footage": 95000, "water_intensity_gal_per_sqft": 0.52, "water_utility_cost_usd": 765.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "meter_month": "2026-03", "potable_water_gallons": 58000, "recycled_water_gallons": 9500, "square_footage": 95000, "water_intensity_gal_per_sqft": 0.61, "water_utility_cost_usd": 905.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "meter_month": "2026-04", "potable_water_gallons": 68000, "recycled_water_gallons": 12000, "square_footage": 95000, "water_intensity_gal_per_sqft": 0.72, "water_utility_cost_usd": 1060.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "meter_month": "2026-05", "potable_water_gallons": 82000, "recycled_water_gallons": 15000, "square_footage": 95000, "water_intensity_gal_per_sqft": 0.86, "water_utility_cost_usd": 1280.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "meter_month": "2026-06", "potable_water_gallons": 98000, "recycled_water_gallons": 19000, "square_footage": 95000, "water_intensity_gal_per_sqft": 1.03, "water_utility_cost_usd": 1530.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "meter_month": "2026-01", "potable_water_gallons": 185000, "recycled_water_gallons": 95000, "square_footage": 650000, "water_intensity_gal_per_sqft": 0.28, "water_utility_cost_usd": 2450.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "meter_month": "2026-02", "potable_water_gallons": 178000, "recycled_water_gallons": 92000, "square_footage": 650000, "water_intensity_gal_per_sqft": 0.27, "water_utility_cost_usd": 2360.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "meter_month": "2026-03", "potable_water_gallons": 195000, "recycled_water_gallons": 105000, "square_footage": 650000, "water_intensity_gal_per_sqft": 0.30, "water_utility_cost_usd": 2580.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "meter_month": "2026-04", "potable_water_gallons": 210000, "recycled_water_gallons": 118000, "square_footage": 650000, "water_intensity_gal_per_sqft": 0.32, "water_utility_cost_usd": 2780.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "meter_month": "2026-05", "potable_water_gallons": 235000, "recycled_water_gallons": 135000, "square_footage": 650000, "water_intensity_gal_per_sqft": 0.36, "water_utility_cost_usd": 3110.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "meter_month": "2026-06", "potable_water_gallons": 260000, "recycled_water_gallons": 152000, "square_footage": 650000, "water_intensity_gal_per_sqft": 0.40, "water_utility_cost_usd": 3440.00},
]

COOLING_TOWERS = [
    {"facility_id": "DC-101", "cooling_tower_id": "CT-DC101-A", "makeup_water_gallons": 125000, "blowdown_water_gallons": 25000, "cycles_of_concentration": 5.0, "water_treatment_type": "Electro-Chemical Non-Chemical", "water_efficiency_pct": 80.0},
    {"facility_id": "DC-101", "cooling_tower_id": "CT-DC101-B", "makeup_water_gallons": 118000, "blowdown_water_gallons": 23600, "cycles_of_concentration": 5.0, "water_treatment_type": "Electro-Chemical Non-Chemical", "water_efficiency_pct": 80.0},
    {"facility_id": "STORE-102", "cooling_tower_id": "CT-ST102-01", "makeup_water_gallons": 62000, "blowdown_water_gallons": 15500, "cycles_of_concentration": 4.0, "water_treatment_type": "Advanced Polymer & Biocide", "water_efficiency_pct": 75.0},
    {"facility_id": "STORE-104", "cooling_tower_id": "CT-ST104-01", "makeup_water_gallons": 74000, "blowdown_water_gallons": 16400, "cycles_of_concentration": 4.5, "water_treatment_type": "Automated Acid Dosing", "water_efficiency_pct": 77.8},
]

RAINWATER = [
    {"facility_id": "STORE-103", "harvest_month": "2026-01", "rainfall_inches": 5.8, "collection_volume_gallons": 48000, "irrigation_reused_gallons": 12000, "stormwater_retention_capacity_pct": 95.0},
    {"facility_id": "STORE-103", "harvest_month": "2026-02", "rainfall_inches": 4.6, "collection_volume_gallons": 38000, "irrigation_reused_gallons": 14000, "stormwater_retention_capacity_pct": 92.0},
    {"facility_id": "STORE-103", "harvest_month": "2026-03", "rainfall_inches": 5.1, "collection_volume_gallons": 42000, "irrigation_reused_gallons": 18000, "stormwater_retention_capacity_pct": 94.0},
    {"facility_id": "STORE-103", "harvest_month": "2026-04", "rainfall_inches": 3.4, "collection_volume_gallons": 28000, "irrigation_reused_gallons": 22000, "stormwater_retention_capacity_pct": 88.0},
    {"facility_id": "STORE-103", "harvest_month": "2026-05", "rainfall_inches": 2.2, "collection_volume_gallons": 18000, "irrigation_reused_gallons": 18000, "stormwater_retention_capacity_pct": 82.0},
    {"facility_id": "STORE-103", "harvest_month": "2026-06", "rainfall_inches": 1.8, "collection_volume_gallons": 15000, "irrigation_reused_gallons": 15000, "stormwater_retention_capacity_pct": 79.0},
]

WATERSHED_INDEX = [
    {"facility_id": "STORE-102", "region": "Southwest - Texas", "watershed_basin_name": "Trinity River Basin", "wri_aqueduct_stress_level": "Extremely High (>80%)", "baseline_water_stress_pct": 84.5, "drought_risk_category": "Severe (D3)", "audit_priority_tier": "Tier 1 - Immediate Audit"},
    {"facility_id": "STORE-104", "region": "Southeast - Georgia", "watershed_basin_name": "Chattahoochee River Basin", "wri_aqueduct_stress_level": "Medium-High (20-40%)", "baseline_water_stress_pct": 32.0, "drought_risk_category": "Moderate (D1)", "audit_priority_tier": "Tier 2 - Annual Review"},
    {"facility_id": "STORE-101", "region": "Midwest - Illinois", "watershed_basin_name": "Des Plaines River Basin", "wri_aqueduct_stress_level": "Low (<10%)", "baseline_water_stress_pct": 8.5, "drought_risk_category": "None (D0)", "audit_priority_tier": "Tier 3 - Standard Monitoring"},
    {"facility_id": "STORE-103", "region": "Pacific Northwest - WA", "watershed_basin_name": "Puget Sound Watershed", "wri_aqueduct_stress_level": "Low (<10%)", "baseline_water_stress_pct": 6.2, "drought_risk_category": "None (D0)", "audit_priority_tier": "Tier 3 - Standard Monitoring"},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(WATER_METERS, "facility_water_meters.csv")
    generate_csv(COOLING_TOWERS, "cooling_tower_efficiency.csv")
    generate_csv(RAINWATER, "rainwater_harvesting_logs.csv")
    generate_csv(WATERSHED_INDEX, "watershed_stress_index.csv")

if __name__ == "__main__":
    main()
