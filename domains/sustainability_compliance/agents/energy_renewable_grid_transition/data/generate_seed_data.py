#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Renewable Energy & Grid Transition agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

SOLAR_DATA = [
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "month": "2026-01", "solar_capacity_kw": 250.0, "generation_mwh": 28.5, "self_consumption_mwh": 25.0, "exported_grid_mwh": 3.5, "avoided_grid_cost_usd": 3850.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "month": "2026-02", "solar_capacity_kw": 250.0, "generation_mwh": 32.0, "self_consumption_mwh": 28.0, "exported_grid_mwh": 4.0, "avoided_grid_cost_usd": 4320.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "month": "2026-03", "solar_capacity_kw": 250.0, "generation_mwh": 42.5, "self_consumption_mwh": 36.0, "exported_grid_mwh": 6.5, "avoided_grid_cost_usd": 5740.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "month": "2026-04", "solar_capacity_kw": 250.0, "generation_mwh": 51.0, "self_consumption_mwh": 42.0, "exported_grid_mwh": 9.0, "avoided_grid_cost_usd": 6880.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "month": "2026-05", "solar_capacity_kw": 250.0, "generation_mwh": 62.5, "self_consumption_mwh": 48.0, "exported_grid_mwh": 14.5, "avoided_grid_cost_usd": 8440.00},
    {"facility_id": "STORE-101", "facility_type": "Retail Store", "month": "2026-06", "solar_capacity_kw": 250.0, "generation_mwh": 68.0, "self_consumption_mwh": 52.0, "exported_grid_mwh": 16.0, "avoided_grid_cost_usd": 9180.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "month": "2026-01", "solar_capacity_kw": 300.0, "generation_mwh": 38.0, "self_consumption_mwh": 32.0, "exported_grid_mwh": 6.0, "avoided_grid_cost_usd": 5130.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "month": "2026-02", "solar_capacity_kw": 300.0, "generation_mwh": 44.0, "self_consumption_mwh": 38.0, "exported_grid_mwh": 6.0, "avoided_grid_cost_usd": 5940.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "month": "2026-03", "solar_capacity_kw": 300.0, "generation_mwh": 58.0, "self_consumption_mwh": 48.0, "exported_grid_mwh": 10.0, "avoided_grid_cost_usd": 7830.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "month": "2026-04", "solar_capacity_kw": 300.0, "generation_mwh": 70.0, "self_consumption_mwh": 56.0, "exported_grid_mwh": 14.0, "avoided_grid_cost_usd": 9450.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "month": "2026-05", "solar_capacity_kw": 300.0, "generation_mwh": 82.0, "self_consumption_mwh": 65.0, "exported_grid_mwh": 17.0, "avoided_grid_cost_usd": 11070.00},
    {"facility_id": "STORE-102", "facility_type": "Retail Store", "month": "2026-06", "solar_capacity_kw": 300.0, "generation_mwh": 89.0, "self_consumption_mwh": 70.0, "exported_grid_mwh": 19.0, "avoided_grid_cost_usd": 12015.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "month": "2026-01", "solar_capacity_kw": 1200.0, "generation_mwh": 140.0, "self_consumption_mwh": 125.0, "exported_grid_mwh": 15.0, "avoided_grid_cost_usd": 18900.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "month": "2026-02", "solar_capacity_kw": 1200.0, "generation_mwh": 165.0, "self_consumption_mwh": 145.0, "exported_grid_mwh": 20.0, "avoided_grid_cost_usd": 22275.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "month": "2026-03", "solar_capacity_kw": 1200.0, "generation_mwh": 215.0, "self_consumption_mwh": 185.0, "exported_grid_mwh": 30.0, "avoided_grid_cost_usd": 29025.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "month": "2026-04", "solar_capacity_kw": 1200.0, "generation_mwh": 260.0, "self_consumption_mwh": 220.0, "exported_grid_mwh": 40.0, "avoided_grid_cost_usd": 35100.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "month": "2026-05", "solar_capacity_kw": 1200.0, "generation_mwh": 310.0, "self_consumption_mwh": 255.0, "exported_grid_mwh": 55.0, "avoided_grid_cost_usd": 41850.00},
    {"facility_id": "DC-101", "facility_type": "Distribution Center", "month": "2026-06", "solar_capacity_kw": 1200.0, "generation_mwh": 345.0, "self_consumption_mwh": 280.0, "exported_grid_mwh": 65.0, "avoided_grid_cost_usd": 46575.00},
]

PPA_CONTRACTS = [
    {"contract_id": "PPA-WIND-01", "ppa_project_name": "Prairie Wind Energy Center (ERCOT)", "energy_source": "Wind", "contracted_annual_mwh": 45000, "cod_year": 2024, "contract_term_years": 12, "ppa_strike_price_per_mwh": 32.50, "renewable_pct_total_load": 28.5},
    {"contract_id": "PPA-SOLAR-02", "ppa_project_name": "Solaria Desert Solar Array (CAISO)", "energy_source": "Utility Solar", "contracted_annual_mwh": 38000, "cod_year": 2025, "contract_term_years": 15, "ppa_strike_price_per_mwh": 36.00, "renewable_pct_total_load": 24.0},
    {"contract_id": "PPA-SOLAR-03", "ppa_project_name": "Appalachian Clean Power Project (PJM)", "energy_source": "Utility Solar", "contracted_annual_mwh": 25000, "cod_year": 2025, "contract_term_years": 10, "ppa_strike_price_per_mwh": 41.20, "renewable_pct_total_load": 15.8},
]

PEAK_SHAVING = [
    {"facility_id": "DC-101", "event_date": "2026-06-12", "peak_demand_kw": 1850.0, "shaved_demand_kw": 450.0, "response_program": "PJM Summer Capacity Demand Response", "incentive_earned_usd": 6750.00, "avoided_demand_charges_usd": 8100.00},
    {"facility_id": "DC-101", "event_date": "2026-06-24", "peak_demand_kw": 1920.0, "shaved_demand_kw": 500.0, "response_program": "PJM Summer Capacity Demand Response", "incentive_earned_usd": 7500.00, "avoided_demand_charges_usd": 9000.00},
    {"facility_id": "STORE-102", "event_date": "2026-06-18", "peak_demand_kw": 480.0, "shaved_demand_kw": 120.0, "response_program": "ERCOT 4CP Peak Reduction Program", "incentive_earned_usd": 2400.00, "avoided_demand_charges_usd": 3600.00},
    {"facility_id": "STORE-102", "event_date": "2026-06-28", "peak_demand_kw": 510.0, "shaved_demand_kw": 140.0, "response_program": "ERCOT 4CP Peak Reduction Program", "incentive_earned_usd": 2800.00, "avoided_demand_charges_usd": 4200.00},
]

BATTERY_STORAGE = [
    {"facility_id": "DC-101", "battery_system_id": "BATT-DC101-01", "storage_capacity_kwh": 2000.0, "round_trip_efficiency_pct": 89.5, "daily_cycles": 1.2, "dispatch_mode": "Peak Shaving & Arbitrage", "annual_energy_arbitrage_savings_usd": 48500.00},
    {"facility_id": "STORE-101", "battery_system_id": "BATT-ST101-01", "storage_capacity_kwh": 500.0, "round_trip_efficiency_pct": 91.0, "daily_cycles": 1.0, "dispatch_mode": "Solar Self-Consumption & Tariff Optimization", "annual_energy_arbitrage_savings_usd": 14200.00},
    {"facility_id": "STORE-102", "battery_system_id": "BATT-ST102-01", "storage_capacity_kwh": 600.0, "round_trip_efficiency_pct": 90.5, "daily_cycles": 1.1, "dispatch_mode": "4CP Coincident Peak Shaving", "annual_energy_arbitrage_savings_usd": 18900.00},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(SOLAR_DATA, "onsite_solar_generation.csv")
    generate_csv(PPA_CONTRACTS, "ppa_renewable_contracts.csv")
    generate_csv(PEAK_SHAVING, "peak_demand_shaving.csv")
    generate_csv(BATTERY_STORAGE, "battery_storage_kwh.csv")

if __name__ == "__main__":
    main()
