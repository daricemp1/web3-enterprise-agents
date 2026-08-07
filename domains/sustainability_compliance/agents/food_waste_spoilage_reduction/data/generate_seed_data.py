#!/usr/bin/env python3
"""Generates synthetic BigQuery seed CSV data for ESG: Food Waste Reduction & Diversion agent."""
from __future__ import annotations
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

SPOILAGE_DATA = [
    {"store_id": "STORE-101", "sku": "SKU-001", "category": "Fresh Produce", "log_date": "2026-06-15", "spoiled_units": 45, "shrink_cost_usd": 135.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
    {"store_id": "STORE-101", "sku": "SKU-002", "category": "Dairy & Chilled", "log_date": "2026-06-18", "spoiled_units": 28, "shrink_cost_usd": 98.00, "spoilage_reason": "Broken Seal Packaging", "temperature_excursion_flag": False},
    {"store_id": "STORE-101", "sku": "SKU-003", "category": "Bakery & Deli", "log_date": "2026-06-20", "spoiled_units": 60, "shrink_cost_usd": 180.00, "spoilage_reason": "Daily Overproduction", "temperature_excursion_flag": False},
    {"store_id": "STORE-101", "sku": "SKU-004", "category": "Meat & Seafood", "log_date": "2026-06-22", "spoiled_units": 15, "shrink_cost_usd": 225.00, "spoilage_reason": "Cold Storage Defrost", "temperature_excursion_flag": True},
    {"store_id": "STORE-102", "sku": "SKU-001", "category": "Fresh Produce", "log_date": "2026-06-16", "spoiled_units": 52, "shrink_cost_usd": 156.00, "spoilage_reason": "Bruising / Handling", "temperature_excursion_flag": False},
    {"store_id": "STORE-102", "sku": "SKU-002", "category": "Dairy & Chilled", "log_date": "2026-06-19", "spoiled_units": 34, "shrink_cost_usd": 119.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
    {"store_id": "STORE-102", "sku": "SKU-003", "category": "Bakery & Deli", "log_date": "2026-06-21", "spoiled_units": 48, "shrink_cost_usd": 144.00, "spoilage_reason": "Daily Overproduction", "temperature_excursion_flag": False},
    {"store_id": "STORE-102", "sku": "SKU-004", "category": "Meat & Seafood", "log_date": "2026-06-24", "spoiled_units": 12, "shrink_cost_usd": 180.00, "spoilage_reason": "Packaging Leak", "temperature_excursion_flag": False},
    {"store_id": "STORE-103", "sku": "SKU-001", "category": "Fresh Produce", "log_date": "2026-06-17", "spoiled_units": 38, "shrink_cost_usd": 114.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
    {"store_id": "STORE-103", "sku": "SKU-002", "category": "Dairy & Chilled", "log_date": "2026-06-20", "spoiled_units": 22, "shrink_cost_usd": 77.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
    {"store_id": "STORE-103", "sku": "SKU-003", "category": "Bakery & Deli", "log_date": "2026-06-23", "spoiled_units": 55, "shrink_cost_usd": 165.00, "spoilage_reason": "Daily Overproduction", "temperature_excursion_flag": False},
    {"store_id": "STORE-103", "sku": "SKU-004", "category": "Meat & Seafood", "log_date": "2026-06-26", "spoiled_units": 18, "shrink_cost_usd": 270.00, "spoilage_reason": "Cold Chain Delay", "temperature_excursion_flag": True},
    {"store_id": "STORE-104", "sku": "SKU-001", "category": "Fresh Produce", "log_date": "2026-07-02", "spoiled_units": 65, "shrink_cost_usd": 195.00, "spoilage_reason": "Overstocking", "temperature_excursion_flag": False},
    {"store_id": "STORE-104", "sku": "SKU-002", "category": "Dairy & Chilled", "log_date": "2026-07-05", "spoiled_units": 30, "shrink_cost_usd": 105.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
    {"store_id": "STORE-104", "sku": "SKU-003", "category": "Bakery & Deli", "log_date": "2026-07-08", "spoiled_units": 70, "shrink_cost_usd": 210.00, "spoilage_reason": "Daily Overproduction", "temperature_excursion_flag": False},
    {"store_id": "STORE-104", "sku": "SKU-004", "category": "Meat & Seafood", "log_date": "2026-07-11", "spoiled_units": 10, "shrink_cost_usd": 150.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
    {"store_id": "STORE-105", "sku": "SKU-001", "category": "Fresh Produce", "log_date": "2026-07-04", "spoiled_units": 40, "shrink_cost_usd": 120.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
    {"store_id": "STORE-105", "sku": "SKU-002", "category": "Dairy & Chilled", "log_date": "2026-07-07", "spoiled_units": 25, "shrink_cost_usd": 87.50, "spoilage_reason": "Damage in Transit", "temperature_excursion_flag": False},
    {"store_id": "STORE-105", "sku": "SKU-003", "category": "Bakery & Deli", "log_date": "2026-07-10", "spoiled_units": 50, "shrink_cost_usd": 150.00, "spoilage_reason": "Daily Overproduction", "temperature_excursion_flag": False},
    {"store_id": "STORE-105", "sku": "SKU-004", "category": "Meat & Seafood", "log_date": "2026-07-13", "spoiled_units": 14, "shrink_cost_usd": 210.00, "spoilage_reason": "Shelf Life Expiration", "temperature_excursion_flag": False},
]

MARKDOWN_RESCUES = [
    {"store_id": "STORE-101", "sku": "SKU-001", "rescue_date": "2026-06-14", "original_price": 5.99, "markdown_price": 2.99, "units_sold_before_expiry": 120, "rescue_revenue_usd": 358.80, "waste_avoided_lbs": 180.0},
    {"store_id": "STORE-101", "sku": "SKU-002", "rescue_date": "2026-06-17", "original_price": 4.50, "markdown_price": 2.25, "units_sold_before_expiry": 85, "rescue_revenue_usd": 191.25, "waste_avoided_lbs": 95.0},
    {"store_id": "STORE-101", "sku": "SKU-004", "rescue_date": "2026-06-21", "original_price": 14.99, "markdown_price": 7.49, "units_sold_before_expiry": 42, "rescue_revenue_usd": 314.58, "waste_avoided_lbs": 63.0},
    {"store_id": "STORE-102", "sku": "SKU-001", "rescue_date": "2026-06-15", "original_price": 5.99, "markdown_price": 2.99, "units_sold_before_expiry": 145, "rescue_revenue_usd": 433.55, "waste_avoided_lbs": 217.5},
    {"store_id": "STORE-102", "sku": "SKU-002", "rescue_date": "2026-06-18", "original_price": 4.50, "markdown_price": 2.25, "units_sold_before_expiry": 98, "rescue_revenue_usd": 220.50, "waste_avoided_lbs": 110.0},
    {"store_id": "STORE-102", "sku": "SKU-004", "rescue_date": "2026-06-23", "original_price": 14.99, "markdown_price": 7.49, "units_sold_before_expiry": 50, "rescue_revenue_usd": 374.50, "waste_avoided_lbs": 75.0},
    {"store_id": "STORE-103", "sku": "SKU-001", "rescue_date": "2026-06-16", "original_price": 5.99, "markdown_price": 2.99, "units_sold_before_expiry": 110, "rescue_revenue_usd": 328.90, "waste_avoided_lbs": 165.0},
    {"store_id": "STORE-103", "sku": "SKU-002", "rescue_date": "2026-06-19", "original_price": 4.50, "markdown_price": 2.25, "units_sold_before_expiry": 75, "rescue_revenue_usd": 168.75, "waste_avoided_lbs": 82.5},
    {"store_id": "STORE-103", "sku": "SKU-004", "rescue_date": "2026-06-25", "original_price": 14.99, "markdown_price": 7.49, "units_sold_before_expiry": 38, "rescue_revenue_usd": 284.62, "waste_avoided_lbs": 57.0},
    {"store_id": "STORE-104", "sku": "SKU-001", "rescue_date": "2026-07-01", "original_price": 5.99, "markdown_price": 2.99, "units_sold_before_expiry": 160, "rescue_revenue_usd": 478.40, "waste_avoided_lbs": 240.0},
    {"store_id": "STORE-104", "sku": "SKU-002", "rescue_date": "2026-07-04", "original_price": 4.50, "markdown_price": 2.25, "units_sold_before_expiry": 105, "rescue_revenue_usd": 236.25, "waste_avoided_lbs": 118.0},
    {"store_id": "STORE-104", "sku": "SKU-004", "rescue_date": "2026-07-10", "original_price": 14.99, "markdown_price": 7.49, "units_sold_before_expiry": 62, "rescue_revenue_usd": 464.38, "waste_avoided_lbs": 93.0},
    {"store_id": "STORE-105", "sku": "SKU-001", "rescue_date": "2026-07-03", "original_price": 5.99, "markdown_price": 2.99, "units_sold_before_expiry": 130, "rescue_revenue_usd": 388.70, "waste_avoided_lbs": 195.0},
    {"store_id": "STORE-105", "sku": "SKU-002", "rescue_date": "2026-07-06", "original_price": 4.50, "markdown_price": 2.25, "units_sold_before_expiry": 90, "rescue_revenue_usd": 202.50, "waste_avoided_lbs": 101.0},
    {"store_id": "STORE-105", "sku": "SKU-004", "rescue_date": "2026-07-12", "original_price": 14.99, "markdown_price": 7.49, "units_sold_before_expiry": 45, "rescue_revenue_usd": 337.05, "waste_avoided_lbs": 67.5},
]

FOOD_BANK_DONATIONS = [
    {"store_id": "STORE-101", "charity_partner": "Greater Chicago Food Depository", "donation_date": "2026-06-16", "category": "Produce & Bakery", "donation_weight_lbs": 850.0, "estimated_meal_count": 708, "tax_deduction_value_usd": 1530.00},
    {"store_id": "STORE-101", "charity_partner": "Greater Chicago Food Depository", "donation_date": "2026-06-23", "category": "Dairy & Pantry", "donation_weight_lbs": 620.0, "estimated_meal_count": 516, "tax_deduction_value_usd": 1116.00},
    {"store_id": "STORE-101", "charity_partner": "Greater Chicago Food Depository", "donation_date": "2026-06-30", "category": "Fresh Prepared", "donation_weight_lbs": 490.0, "estimated_meal_count": 408, "tax_deduction_value_usd": 882.00},
    {"store_id": "STORE-102", "charity_partner": "North Texas Food Bank", "donation_date": "2026-06-17", "category": "Produce & Bakery", "donation_weight_lbs": 980.0, "estimated_meal_count": 816, "tax_deduction_value_usd": 1764.00},
    {"store_id": "STORE-102", "charity_partner": "North Texas Food Bank", "donation_date": "2026-06-24", "category": "Dairy & Pantry", "donation_weight_lbs": 740.0, "estimated_meal_count": 616, "tax_deduction_value_usd": 1332.00},
    {"store_id": "STORE-102", "charity_partner": "North Texas Food Bank", "donation_date": "2026-07-01", "category": "Fresh Prepared", "donation_weight_lbs": 560.0, "estimated_meal_count": 466, "tax_deduction_value_usd": 1008.00},
    {"store_id": "STORE-103", "charity_partner": "Food Lifeline Western WA", "donation_date": "2026-06-18", "category": "Produce & Bakery", "donation_weight_lbs": 780.0, "estimated_meal_count": 650, "tax_deduction_value_usd": 1404.00},
    {"store_id": "STORE-103", "charity_partner": "Food Lifeline Western WA", "donation_date": "2026-06-25", "category": "Dairy & Pantry", "donation_weight_lbs": 580.0, "estimated_meal_count": 483, "tax_deduction_value_usd": 1044.00},
    {"store_id": "STORE-104", "charity_partner": "Atlanta Community Food Bank", "donation_date": "2026-07-02", "category": "Produce & Bakery", "donation_weight_lbs": 1120.0, "estimated_meal_count": 933, "tax_deduction_value_usd": 2016.00},
    {"store_id": "STORE-104", "charity_partner": "Atlanta Community Food Bank", "donation_date": "2026-07-09", "category": "Dairy & Pantry", "donation_weight_lbs": 810.0, "estimated_meal_count": 675, "tax_deduction_value_usd": 1458.00},
    {"store_id": "STORE-105", "charity_partner": "Greater Boston Food Bank", "donation_date": "2026-07-05", "category": "Produce & Bakery", "donation_weight_lbs": 890.0, "estimated_meal_count": 741, "tax_deduction_value_usd": 1602.00},
    {"store_id": "STORE-105", "charity_partner": "Greater Boston Food Bank", "donation_date": "2026-07-12", "category": "Dairy & Pantry", "donation_weight_lbs": 670.0, "estimated_meal_count": 558, "tax_deduction_value_usd": 1206.00},
]

DIVERSION_DATA = [
    {"store_id": "STORE-101", "month": "2026-01", "landfill_tons": 8.5, "composted_tons": 24.2, "organic_digestion_tons": 12.8, "diversion_rate_pct": 81.3, "waste_disposal_cost_usd": 1850.00},
    {"store_id": "STORE-101", "month": "2026-02", "landfill_tons": 7.8, "composted_tons": 25.0, "organic_digestion_tons": 13.5, "diversion_rate_pct": 83.2, "waste_disposal_cost_usd": 1720.00},
    {"store_id": "STORE-101", "month": "2026-03", "landfill_tons": 7.2, "composted_tons": 26.5, "organic_digestion_tons": 14.1, "diversion_rate_pct": 84.9, "waste_disposal_cost_usd": 1650.00},
    {"store_id": "STORE-101", "month": "2026-04", "landfill_tons": 6.5, "composted_tons": 28.0, "organic_digestion_tons": 15.0, "diversion_rate_pct": 86.9, "waste_disposal_cost_usd": 1540.00},
    {"store_id": "STORE-101", "month": "2026-05", "landfill_tons": 6.0, "composted_tons": 29.5, "organic_digestion_tons": 15.8, "diversion_rate_pct": 88.3, "waste_disposal_cost_usd": 1480.00},
    {"store_id": "STORE-101", "month": "2026-06", "landfill_tons": 5.5, "composted_tons": 31.0, "organic_digestion_tons": 16.5, "diversion_rate_pct": 89.6, "waste_disposal_cost_usd": 1410.00},
    {"store_id": "STORE-102", "month": "2026-01", "landfill_tons": 9.2, "composted_tons": 22.0, "organic_digestion_tons": 11.5, "diversion_rate_pct": 78.4, "waste_disposal_cost_usd": 2010.00},
    {"store_id": "STORE-102", "month": "2026-02", "landfill_tons": 8.5, "composted_tons": 23.5, "organic_digestion_tons": 12.2, "diversion_rate_pct": 80.8, "waste_disposal_cost_usd": 1880.00},
    {"store_id": "STORE-102", "month": "2026-03", "landfill_tons": 7.9, "composted_tons": 25.1, "organic_digestion_tons": 13.0, "diversion_rate_pct": 82.8, "waste_disposal_cost_usd": 1790.00},
    {"store_id": "STORE-102", "month": "2026-04", "landfill_tons": 7.1, "composted_tons": 26.8, "organic_digestion_tons": 14.2, "diversion_rate_pct": 85.2, "waste_disposal_cost_usd": 1680.00},
    {"store_id": "STORE-102", "month": "2026-05", "landfill_tons": 6.6, "composted_tons": 28.2, "organic_digestion_tons": 15.0, "diversion_rate_pct": 86.7, "waste_disposal_cost_usd": 1590.00},
    {"store_id": "STORE-102", "month": "2026-06", "landfill_tons": 6.0, "composted_tons": 29.8, "organic_digestion_tons": 16.0, "diversion_rate_pct": 88.4, "waste_disposal_cost_usd": 1510.00},
]

def generate_csv(data: list[dict], filename: str):
    path = DATA_DIR / filename
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {path}")

def main():
    generate_csv(SPOILAGE_DATA, "perishable_spoilage_logs.csv")
    generate_csv(MARKDOWN_RESCUES, "dynamic_markdown_rescues.csv")
    generate_csv(FOOD_BANK_DONATIONS, "food_bank_donations_lbs.csv")
    generate_csv(DIVERSION_DATA, "compost_landfill_diversion.csv")

if __name__ == "__main__":
    main()
