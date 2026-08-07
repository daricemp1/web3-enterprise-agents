#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Carbon Footprint & Scope Emissions agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

SCOPE1_DATA = [
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-01", "natural_gas_therms": 4200, "fleet_diesel_gallons": 1100, "refrigerant_loss_lbs": 12.5, "scope1_mt_co2e": 34.2},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-02", "natural_gas_therms": 3950, "fleet_diesel_gallons": 1050, "refrigerant_loss_lbs": 10.0, "scope1_mt_co2e": 31.8},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-03", "natural_gas_therms": 3100, "fleet_diesel_gallons": 1200, "refrigerant_loss_lbs": 15.0, "scope1_mt_co2e": 29.5},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-04", "natural_gas_therms": 2200, "fleet_diesel_gallons": 1150, "refrigerant_loss_lbs": 8.5, "scope1_mt_co2e": 23.1},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-05", "natural_gas_therms": 1400, "fleet_diesel_gallons": 1300, "refrigerant_loss_lbs": 18.0, "scope1_mt_co2e": 21.4},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-06", "natural_gas_therms": 950, "fleet_diesel_gallons": 1350, "refrigerant_loss_lbs": 22.0, "scope1_mt_co2e": 20.8},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-01", "natural_gas_therms": 3800, "fleet_diesel_gallons": 980, "refrigerant_loss_lbs": 14.0, "scope1_mt_co2e": 31.5},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-02", "natural_gas_therms": 3400, "fleet_diesel_gallons": 950, "refrigerant_loss_lbs": 11.0, "scope1_mt_co2e": 28.2},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-03", "natural_gas_therms": 2600, "fleet_diesel_gallons": 1100, "refrigerant_loss_lbs": 16.0, "scope1_mt_co2e": 25.8},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-04", "natural_gas_therms": 1800, "fleet_diesel_gallons": 1050, "refrigerant_loss_lbs": 9.0, "scope1_mt_co2e": 20.2},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-05", "natural_gas_therms": 1100, "fleet_diesel_gallons": 1200, "refrigerant_loss_lbs": 19.5, "scope1_mt_co2e": 19.6},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-06", "natural_gas_therms": 800, "fleet_diesel_gallons": 1250, "refrigerant_loss_lbs": 25.0, "scope1_mt_co2e": 19.9},
    {"facility_id": "STORE-103", "facility_type": "Retail Store", "reporting_month": "2026-01", "natural_gas_therms": 4500, "fleet_diesel_gallons": 850, "refrigerant_loss_lbs": 8.0, "scope1_mt_co2e": 32.7},
    {"facility_id": "STORE-103", "facility_type": "Retail Store", "reporting_month": "2026-02", "natural_gas_therms": 4100, "fleet_diesel_gallons": 800, "refrigerant_loss_lbs": 7.5, "scope1_mt_co2e": 29.8},
    {"facility_id": "STORE-103", "facility_type": "Retail Store", "reporting_month": "2026-03", "natural_gas_therms": 3300, "fleet_diesel_gallons": 900, "refrigerant_loss_lbs": 10.0, "scope1_mt_co2e": 26.2},
    {"facility_id": "STORE-103", "facility_type": "Retail Store", "reporting_month": "2026-04", "natural_gas_therms": 2500, "fleet_diesel_gallons": 920, "refrigerant_loss_lbs": 6.0, "scope1_mt_co2e": 21.4},
    {"facility_id": "STORE-103", "facility_type": "Retail Store", "reporting_month": "2026-05", "natural_gas_therms": 1600, "fleet_diesel_gallons": 1000, "refrigerant_loss_lbs": 12.0, "scope1_mt_co2e": 18.5},
    {"facility_id": "STORE-103", "facility_type": "Retail Store", "reporting_month": "2026-06", "natural_gas_therms": 1050, "fleet_diesel_gallons": 1080, "refrigerant_loss_lbs": 15.0, "scope1_mt_co2e": 17.2},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-01", "natural_gas_therms": 12500, "fleet_diesel_gallons": 18500, "refrigerant_loss_lbs": 45.0, "scope1_mt_co2e": 258.4},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-02", "natural_gas_therms": 11800, "fleet_diesel_gallons": 17900, "refrigerant_loss_lbs": 40.0, "scope1_mt_co2e": 247.9},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-03", "natural_gas_therms": 9400, "fleet_diesel_gallons": 19200, "refrigerant_loss_lbs": 50.0, "scope1_mt_co2e": 249.2},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-04", "natural_gas_therms": 6200, "fleet_diesel_gallons": 18800, "refrigerant_loss_lbs": 38.0, "scope1_mt_co2e": 226.5},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-05", "natural_gas_therms": 3800, "fleet_diesel_gallons": 20100, "refrigerant_loss_lbs": 55.0, "scope1_mt_co2e": 228.8},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-06", "natural_gas_therms": 2400, "fleet_diesel_gallons": 20800, "refrigerant_loss_lbs": 62.0, "scope1_mt_co2e": 231.1},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-01", "natural_gas_therms": 9800, "fleet_diesel_gallons": 14200, "refrigerant_loss_lbs": 35.0, "scope1_mt_co2e": 198.6},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-02", "natural_gas_therms": 9100, "fleet_diesel_gallons": 13800, "refrigerant_loss_lbs": 30.0, "scope1_mt_co2e": 189.5},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-03", "natural_gas_therms": 7200, "fleet_diesel_gallons": 15100, "refrigerant_loss_lbs": 42.0, "scope1_mt_co2e": 194.2},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-04", "natural_gas_therms": 4500, "fleet_diesel_gallons": 14700, "refrigerant_loss_lbs": 28.0, "scope1_mt_co2e": 175.4},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-05", "natural_gas_therms": 2800, "fleet_diesel_gallons": 15900, "refrigerant_loss_lbs": 48.0, "scope1_mt_co2e": 179.8},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-06", "natural_gas_therms": 1900, "fleet_diesel_gallons": 16400, "refrigerant_loss_lbs": 56.0, "scope1_mt_co2e": 183.0},
]

SCOPE2_DATA = [
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-01", "grid_kwh_consumed": 85000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 32.7, "market_based_mt_co2e": 16.3, "recs_applied_mwh": 42.5},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-02", "grid_kwh_consumed": 79000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 30.4, "market_based_mt_co2e": 15.2, "recs_applied_mwh": 39.5},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-03", "grid_kwh_consumed": 82000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 31.6, "market_based_mt_co2e": 15.8, "recs_applied_mwh": 41.0},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-04", "grid_kwh_consumed": 88000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 33.9, "market_based_mt_co2e": 13.5, "recs_applied_mwh": 52.8},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-05", "grid_kwh_consumed": 98000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 37.7, "market_based_mt_co2e": 15.1, "recs_applied_mwh": 58.8},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "reporting_month": "2026-06", "grid_kwh_consumed": 112000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 43.1, "market_based_mt_co2e": 17.2, "recs_applied_mwh": 67.2},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-01", "grid_kwh_consumed": 92000, "grid_emission_factor_kg_kwh": 0.420, "location_based_mt_co2e": 38.6, "market_based_mt_co2e": 19.3, "recs_applied_mwh": 46.0},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-02", "grid_kwh_consumed": 86000, "grid_emission_factor_kg_kwh": 0.420, "location_based_mt_co2e": 36.1, "market_based_mt_co2e": 18.1, "recs_applied_mwh": 43.0},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-03", "grid_kwh_consumed": 95000, "grid_emission_factor_kg_kwh": 0.420, "location_based_mt_co2e": 39.9, "market_based_mt_co2e": 20.0, "recs_applied_mwh": 47.5},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-04", "grid_kwh_consumed": 105000, "grid_emission_factor_kg_kwh": 0.420, "location_based_mt_co2e": 44.1, "market_based_mt_co2e": 17.6, "recs_applied_mwh": 63.0},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-05", "grid_kwh_consumed": 125000, "grid_emission_factor_kg_kwh": 0.420, "location_based_mt_co2e": 52.5, "market_based_mt_co2e": 21.0, "recs_applied_mwh": 75.0},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "reporting_month": "2026-06", "grid_kwh_consumed": 142000, "grid_emission_factor_kg_kwh": 0.420, "location_based_mt_co2e": 59.6, "market_based_mt_co2e": 23.8, "recs_applied_mwh": 85.2},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-01", "grid_kwh_consumed": 380000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 146.3, "market_based_mt_co2e": 58.5, "recs_applied_mwh": 228.0},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-02", "grid_kwh_consumed": 360000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 138.6, "market_based_mt_co2e": 55.4, "recs_applied_mwh": 216.0},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-03", "grid_kwh_consumed": 395000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 152.1, "market_based_mt_co2e": 60.8, "recs_applied_mwh": 237.0},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-04", "grid_kwh_consumed": 420000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 161.7, "market_based_mt_co2e": 48.5, "recs_applied_mwh": 294.0},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-05", "grid_kwh_consumed": 475000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 182.9, "market_based_mt_co2e": 54.9, "recs_applied_mwh": 332.5},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "reporting_month": "2026-06", "grid_kwh_consumed": 530000, "grid_emission_factor_kg_kwh": 0.385, "location_based_mt_co2e": 204.1, "market_based_mt_co2e": 61.2, "recs_applied_mwh": 371.0},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-01", "grid_kwh_consumed": 290000, "grid_emission_factor_kg_kwh": 0.395, "location_based_mt_co2e": 114.6, "market_based_mt_co2e": 45.8, "recs_applied_mwh": 174.0},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-02", "grid_kwh_consumed": 275000, "grid_emission_factor_kg_kwh": 0.395, "location_based_mt_co2e": 108.6, "market_based_mt_co2e": 43.4, "recs_applied_mwh": 165.0},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-03", "grid_kwh_consumed": 305000, "grid_emission_factor_kg_kwh": 0.395, "location_based_mt_co2e": 120.5, "market_based_mt_co2e": 48.2, "recs_applied_mwh": 183.0},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-04", "grid_kwh_consumed": 330000, "grid_emission_factor_kg_kwh": 0.395, "location_based_mt_co2e": 130.4, "market_based_mt_co2e": 39.1, "recs_applied_mwh": 231.0},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-05", "grid_kwh_consumed": 370000, "grid_emission_factor_kg_kwh": 0.395, "location_based_mt_co2e": 146.2, "market_based_mt_co2e": 43.8, "recs_applied_mwh": 259.0},
    {"facility_id": "DC-102", "facility_type": "Distribution Center", "reporting_month": "2026-06", "grid_kwh_consumed": 415000, "grid_emission_factor_kg_kwh": 0.395, "location_based_mt_co2e": 163.9, "market_based_mt_co2e": 49.2, "recs_applied_mwh": 290.5},
]

SCOPE3_DATA = [
    {"vendor_id": "VEND-1001", "category": "Apparel", "reporting_quarter": "2026-Q1", "purchased_goods_mt_co2e": 1450.5, "upstream_freight_mt_co2e": 320.2, "packaging_mt_co2e": 115.8, "total_scope3_mt_co2e": 1886.5, "carbon_intensity_per_dollar": 0.42},
    {"vendor_id": "VEND-1001", "category": "Apparel", "reporting_quarter": "2026-Q2", "purchased_goods_mt_co2e": 1580.0, "upstream_freight_mt_co2e": 345.0, "packaging_mt_co2e": 122.0, "total_scope3_mt_co2e": 2047.0, "carbon_intensity_per_dollar": 0.41},
    {"vendor_id": "VEND-1002", "category": "Packaging", "reporting_quarter": "2026-Q1", "purchased_goods_mt_co2e": 820.4, "upstream_freight_mt_co2e": 190.5, "packaging_mt_co2e": 280.6, "total_scope3_mt_co2e": 1291.5, "carbon_intensity_per_dollar": 0.35},
    {"vendor_id": "VEND-1002", "category": "Packaging", "reporting_quarter": "2026-Q2", "purchased_goods_mt_co2e": 790.0, "upstream_freight_mt_co2e": 180.0, "packaging_mt_co2e": 260.0, "total_scope3_mt_co2e": 1230.0, "carbon_intensity_per_dollar": 0.33},
    {"vendor_id": "VEND-1003", "category": "Home & Personal Care", "reporting_quarter": "2026-Q1", "purchased_goods_mt_co2e": 1120.0, "upstream_freight_mt_co2e": 240.0, "packaging_mt_co2e": 195.0, "total_scope3_mt_co2e": 1555.0, "carbon_intensity_per_dollar": 0.38},
    {"vendor_id": "VEND-1003", "category": "Home & Personal Care", "reporting_quarter": "2026-Q2", "purchased_goods_mt_co2e": 1180.0, "upstream_freight_mt_co2e": 255.0, "packaging_mt_co2e": 205.0, "total_scope3_mt_co2e": 1640.0, "carbon_intensity_per_dollar": 0.37},
    {"vendor_id": "VEND-1004", "category": "Electronics & Appliances", "reporting_quarter": "2026-Q1", "purchased_goods_mt_co2e": 2350.0, "upstream_freight_mt_co2e": 580.0, "packaging_mt_co2e": 310.0, "total_scope3_mt_co2e": 3240.0, "carbon_intensity_per_dollar": 0.58},
    {"vendor_id": "VEND-1004", "category": "Electronics & Appliances", "reporting_quarter": "2026-Q2", "purchased_goods_mt_co2e": 2490.0, "upstream_freight_mt_co2e": 610.0, "packaging_mt_co2e": 325.0, "total_scope3_mt_co2e": 3425.0, "carbon_intensity_per_dollar": 0.56},
]

NET_ZERO_DATA = [
    {"target_year": 2026, "base_year": 2020, "target_reduction_pct": 25.0, "actual_reduction_pct_ytd": 26.8, "total_emissions_mt_co2e": 18450.0, "target_status": "On Track", "offset_credits_retired": 2500},
    {"target_year": 2028, "base_year": 2020, "target_reduction_pct": 40.0, "actual_reduction_pct_ytd": 26.8, "total_emissions_mt_co2e": 14760.0, "target_status": "On Track", "offset_credits_retired": 0},
    {"target_year": 2030, "base_year": 2020, "target_reduction_pct": 55.0, "actual_reduction_pct_ytd": 26.8, "total_emissions_mt_co2e": 11070.0, "target_status": "Planned", "offset_credits_retired": 0},
    {"target_year": 2035, "base_year": 2020, "target_reduction_pct": 80.0, "actual_reduction_pct_ytd": 26.8, "total_emissions_mt_co2e": 4920.0, "target_status": "Planned", "offset_credits_retired": 0},
    {"target_year": 2040, "base_year": 2020, "target_reduction_pct": 100.0, "actual_reduction_pct_ytd": 26.8, "total_emissions_mt_co2e": 0.0, "target_status": "Net-Zero Target", "offset_credits_retired": 0},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(SCOPE1_DATA, "scope1_fleet_facilities.csv")
    generate_csv(SCOPE2_DATA, "scope2_electricity_grid.csv")
    generate_csv(SCOPE3_DATA, "scope3_supply_chain_lifecycle.csv")
    generate_csv(NET_ZERO_DATA, "net_zero_targets.csv")

if __name__ == "__main__":
    main()
