"""Generates synthetic seed data CSV files for the Warehouse & DC Operations agent.

Anchors date windows around 2026-07-24 and uses stdlib csv module to write seed files.
"""
import csv
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

FACILITIES = [
    {
        "dc_id": "DC-001",
        "dc_name": "Midwest Regional DC",
        "region": "Midwest",
        "total_square_feet": 450000,
        "capacity_pallets": 35000,
        "facility_type": "Regional DC",
    },
    {
        "dc_id": "DC-002",
        "dc_name": "South Omnichannel Hub",
        "region": "South",
        "total_square_feet": 600000,
        "capacity_pallets": 50000,
        "facility_type": "Omnichannel Hub",
    },
    {
        "dc_id": "DC-003",
        "dc_name": "West Coast Import DC",
        "region": "West Coast",
        "total_square_feet": 500000,
        "capacity_pallets": 40000,
        "facility_type": "Import Facility",
    },
]

DAILY_THROUGHPUT = [
    {
        "dc_id": "DC-001",
        "date": "2026-07-24",
        "inbound_shipments_count": 25,
        "inbound_units_received": 12500,
        "outbound_shipments_count": 40,
        "outbound_units_shipped": 18000,
        "dock_to_stock_hours": 3.5,
        "avg_dock_turn_minutes": 45,
    },
    {
        "dc_id": "DC-002",
        "date": "2026-07-24",
        "inbound_shipments_count": 38,
        "inbound_units_received": 24000,
        "outbound_shipments_count": 65,
        "outbound_units_shipped": 32000,
        "dock_to_stock_hours": 2.8,
        "avg_dock_turn_minutes": 38,
    },
    {
        "dc_id": "DC-003",
        "date": "2026-07-24",
        "inbound_shipments_count": 18,
        "inbound_units_received": 15000,
        "outbound_shipments_count": 22,
        "outbound_units_shipped": 14000,
        "dock_to_stock_hours": 5.2,
        "avg_dock_turn_minutes": 75,
    },
]

PICK_PACK_PERFORMANCE = [
    {
        "dc_id": "DC-001",
        "date": "2026-07-24",
        "zone": "Bulk Storage",
        "units_picked": 4000,
        "pick_accuracy_pct": 98.8,
        "pick_units_per_hour": 75,
        "mispack_count": 8,
    },
    {
        "dc_id": "DC-001",
        "date": "2026-07-24",
        "zone": "High-Speed Pick",
        "units_picked": 8500,
        "pick_accuracy_pct": 99.4,
        "pick_units_per_hour": 145,
        "mispack_count": 12,
    },
    {
        "dc_id": "DC-001",
        "date": "2026-07-24",
        "zone": "Cold Storage",
        "units_picked": 1500,
        "pick_accuracy_pct": 97.5,
        "pick_units_per_hour": 50,
        "mispack_count": 5,
    },
    {
        "dc_id": "DC-002",
        "date": "2026-07-24",
        "zone": "Bulk Storage",
        "units_picked": 6500,
        "pick_accuracy_pct": 99.1,
        "pick_units_per_hour": 85,
        "mispack_count": 6,
    },
    {
        "dc_id": "DC-002",
        "date": "2026-07-24",
        "zone": "High-Speed Pick",
        "units_picked": 15000,
        "pick_accuracy_pct": 99.7,
        "pick_units_per_hour": 160,
        "mispack_count": 10,
    },
    {
        "dc_id": "DC-002",
        "date": "2026-07-24",
        "zone": "Cold Storage",
        "units_picked": 2500,
        "pick_accuracy_pct": 98.2,
        "pick_units_per_hour": 55,
        "mispack_count": 4,
    },
    {
        "dc_id": "DC-003",
        "date": "2026-07-24",
        "zone": "Bulk Storage",
        "units_picked": 5000,
        "pick_accuracy_pct": 98.0,
        "pick_units_per_hour": 70,
        "mispack_count": 10,
    },
    {
        "dc_id": "DC-003",
        "date": "2026-07-24",
        "zone": "High-Speed Pick",
        "units_picked": 7000,
        "pick_accuracy_pct": 99.0,
        "pick_units_per_hour": 130,
        "mispack_count": 15,
    },
    {
        "dc_id": "DC-003",
        "date": "2026-07-24",
        "zone": "Cold Storage",
        "units_picked": 1000,
        "pick_accuracy_pct": 96.8,
        "pick_units_per_hour": 45,
        "mispack_count": 7,
    },
]

CAPACITY_UTILIZATION = [
    {
        "dc_id": "DC-001",
        "date": "2026-07-24",
        "active_pallet_positions": 31500,
        "max_pallet_positions": 35000,
        "utilization_pct": 90.0,
        "overflow_trailer_count": 3,
        "capacity_alert_flag": True,
    },
    {
        "dc_id": "DC-002",
        "date": "2026-07-24",
        "active_pallet_positions": 39000,
        "max_pallet_positions": 50000,
        "utilization_pct": 78.0,
        "overflow_trailer_count": 0,
        "capacity_alert_flag": False,
    },
    {
        "dc_id": "DC-003",
        "date": "2026-07-24",
        "active_pallet_positions": 37600,
        "max_pallet_positions": 40000,
        "utilization_pct": 94.0,
        "overflow_trailer_count": 7,
        "capacity_alert_flag": True,
    },
]


def write_csv(filename: str, fieldnames: list[str], rows: list[dict]):
  filepath = DATA_DIR / filename
  with open(filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def main():
  write_csv(
      "facilities.csv",
      [
          "dc_id",
          "dc_name",
          "region",
          "total_square_feet",
          "capacity_pallets",
          "facility_type",
      ],
      FACILITIES,
  )
  write_csv(
      "daily_throughput.csv",
      [
          "dc_id",
          "date",
          "inbound_shipments_count",
          "inbound_units_received",
          "outbound_shipments_count",
          "outbound_units_shipped",
          "dock_to_stock_hours",
          "avg_dock_turn_minutes",
      ],
      DAILY_THROUGHPUT,
  )
  write_csv(
      "pick_pack_performance.csv",
      [
          "dc_id",
          "date",
          "zone",
          "units_picked",
          "pick_accuracy_pct",
          "pick_units_per_hour",
          "mispack_count",
      ],
      PICK_PACK_PERFORMANCE,
  )
  write_csv(
      "capacity_utilization.csv",
      [
          "dc_id",
          "date",
          "active_pallet_positions",
          "max_pallet_positions",
          "utilization_pct",
          "overflow_trailer_count",
          "capacity_alert_flag",
      ],
      CAPACITY_UTILIZATION,
  )
  print(f"Generated 4 seed data CSV files in {DATA_DIR}")


if __name__ == "__main__":
  main()
