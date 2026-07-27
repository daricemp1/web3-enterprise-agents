"""Generates synthetic seed data CSV files for the Logistics Operations agent.

Ensures cross-agent entity alignment with SKU-001..SKU-006 and anchors date windows
around 2026-07-24.
"""
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

PRODUCT_CATALOG_CSV = """product_id,product_name,category,department,brand,launch_date,status
SKU-001,Down Parka,Apparel,Outerwear,AlpineGear,2025-09-01,ACTIVE
SKU-002,Rain Jacket,Apparel,Outerwear,WeatherShield,2025-03-15,ACTIVE
SKU-003,Hiking Boots,Footwear,Outdoor,TrailBlazer,2025-01-10,ACTIVE
SKU-004,Running Shoes,Footwear,Athletic,PaceSetter,2025-02-01,ACTIVE
SKU-005,Wool Socks,Apparel,Accessories,CozyStep,2024-10-01,ACTIVE
SKU-006,Thermal Base Layer,Apparel,Underwear,HeatTech,2024-11-15,ACTIVE
"""

CARRIERS_CSV = """carrier_id,carrier_name,transport_mode,sla_on_time_pct,avg_cost_per_mile
CARRIER-001,Apex Freight Systems,TRUCKLOAD,94.5,2.85
CARRIER-002,SwiftTrans Logistics,INTERMODAL,82.0,2.10
CARRIER-003,Coastal Express Cargo,LTL,78.5,3.40
CARRIER-004,National Parcel Post,PARCEL,96.0,4.15
"""

TRANSIT_LANES_CSV = """lane_id,origin_region,destination_region,standard_transit_days,avg_delay_hours
LANE-001,West Coast,Pacific Northwest,2.0,4.5
LANE-002,Midwest,East Coast,3.5,12.0
LANE-003,South,Northeast,4.0,18.5
LANE-004,West Coast,Southwest,1.5,1.0
"""

SHIPMENTS_CSV = """shipment_id,po_id,carrier_id,lane_id,sku_id,ship_date,expected_delivery_date,actual_delivery_date,status,quantity_shipped,freight_cost
SH-1001,PO-501,CARRIER-001,LANE-001,SKU-001,2026-07-15,2026-07-17,2026-07-17,DELIVERED_ON_TIME,500,1425.00
SH-1002,PO-502,CARRIER-002,LANE-002,SKU-002,2026-07-16,2026-07-19,2026-07-21,DELIVERED_LATE,300,1260.00
SH-1003,PO-503,CARRIER-003,LANE-003,SKU-003,2026-07-18,2026-07-22,2026-07-24,DELIVERED_LATE,400,2100.00
SH-1004,PO-504,CARRIER-001,LANE-004,SKU-004,2026-07-20,2026-07-21,2026-07-21,DELIVERED_ON_TIME,800,950.00
SH-1005,PO-505,CARRIER-002,LANE-002,SKU-005,2026-07-21,2026-07-24,2026-07-25,DELIVERED_LATE,1000,1470.00
SH-1006,PO-506,CARRIER-003,LANE-003,SKU-006,2026-07-22,2026-07-26,,IN_TRANSIT_DELAYED,600,2550.00
SH-1007,PO-507,CARRIER-004,LANE-001,SKU-004,2026-07-23,2026-07-25,,IN_TRANSIT_ON_SCHEDULE,250,830.00
"""


def main():
  (DATA_DIR / "product_catalog.csv").write_text(PRODUCT_CATALOG_CSV)
  (DATA_DIR / "carriers.csv").write_text(CARRIERS_CSV)
  (DATA_DIR / "transit_lanes.csv").write_text(TRANSIT_LANES_CSV)
  (DATA_DIR / "shipments.csv").write_text(SHIPMENTS_CSV)
  print(f"Generated 4 seed data CSVs in {DATA_DIR}")


if __name__ == "__main__":
  main()
