
import pandas as pd

shipments = pd.DataFrame([
    {'shipment_id': 'SHP-IN-101', 'carrier_name': 'Maersk Line', 'origin_port': 'Shanghai', 'destination_port': 'Port of Los Angeles', 'mode': 'Ocean', 'cwt_cost_usd': 42.50, 'target_cwt_usd': 38.00, 'transit_status': 'Delivered', 'on_time_flag': True},
    {'shipment_id': 'SHP-IN-102', 'carrier_name': 'MSC Mediterranean', 'origin_port': 'Ningbo', 'destination_port': 'Port of Long Beach', 'mode': 'Ocean', 'cwt_cost_usd': 46.20, 'target_cwt_usd': 39.50, 'transit_status': 'Delivered', 'on_time_flag': False},
    {'shipment_id': 'SHP-IN-103', 'carrier_name': 'Hapag-Lloyd', 'origin_port': 'Busan', 'destination_port': 'Port of Seattle', 'mode': 'Ocean', 'cwt_cost_usd': 39.80, 'target_cwt_usd': 39.00, 'transit_status': 'In-Transit', 'on_time_flag': True},
    {'shipment_id': 'SHP-IN-104', 'carrier_name': 'BNSF Rail', 'origin_port': 'Port of Los Angeles', 'destination_port': 'Chicago Inland Hub', 'mode': 'Intermodal Rail', 'cwt_cost_usd': 28.40, 'target_cwt_usd': 27.00, 'transit_status': 'Delivered', 'on_time_flag': True},
    {'shipment_id': 'SHP-IN-105', 'carrier_name': 'Union Pacific', 'origin_port': 'Port of Long Beach', 'destination_port': 'Dallas DC Hub', 'mode': 'Intermodal Rail', 'cwt_cost_usd': 31.00, 'target_cwt_usd': 28.50, 'transit_status': 'Delivered', 'on_time_flag': False}
])
shipments.to_csv('data/freight_shipments.csv', index=False)

lane_rates = pd.DataFrame([
    {'lane_id': 'LANE-SHA-LAX', 'origin': 'Shanghai', 'destination': 'Los Angeles', 'benchmark_cwt_usd': 38.00, 'spot_rate_cwt_usd': 43.50, 'variance_bps': 1447},
    {'lane_id': 'LANE-NGB-LGB', 'origin': 'Ningbo', 'destination': 'Long Beach', 'benchmark_cwt_usd': 39.50, 'spot_rate_cwt_usd': 46.20, 'variance_bps': 1696},
    {'lane_id': 'LANE-PUS-SEA', 'origin': 'Busan', 'destination': 'Seattle', 'benchmark_cwt_usd': 39.00, 'spot_rate_cwt_usd': 39.80, 'variance_bps': 205},
    {'lane_id': 'LANE-LAX-CHI', 'origin': 'Los Angeles', 'destination': 'Chicago Hub', 'benchmark_cwt_usd': 27.00, 'spot_rate_cwt_usd': 28.40, 'variance_bps': 518}
])
lane_rates.to_csv('data/lane_rate_benchmarks.csv', index=False)

dwell = pd.DataFrame([
    {'container_id': 'CNTR-88910', 'port_name': 'Port of Los Angeles', 'terminal': 'Pier 400', 'dwell_days': 3.2, 'free_time_days': 4.0, 'dwell_status': 'Within Free Time'},
    {'container_id': 'CNTR-88911', 'port_name': 'Port of Long Beach', 'terminal': 'Pier T', 'dwell_days': 6.5, 'free_time_days': 4.0, 'dwell_status': 'Excess Dwell'},
    {'container_id': 'CNTR-88912', 'port_name': 'Port of Seattle', 'terminal': 'Terminal 18', 'dwell_days': 2.8, 'free_time_days': 4.0, 'dwell_status': 'Within Free Time'},
    {'container_id': 'CNTR-88913', 'port_name': 'Port of Los Angeles', 'terminal': 'TraPac', 'dwell_days': 5.8, 'free_time_days': 4.0, 'dwell_status': 'Excess Dwell'}
])
dwell.to_csv('data/container_dwell_times.csv', index=False)

demurrage = pd.DataFrame([
    {'fee_id': 'DEM-2026-01', 'container_id': 'CNTR-88911', 'port_name': 'Port of Long Beach', 'carrier_name': 'MSC Mediterranean', 'excess_days': 2.5, 'daily_rate_usd': 250.0, 'total_demurrage_usd': 625.0, 'dispute_status': 'Paid'},
    {'fee_id': 'DEM-2026-02', 'container_id': 'CNTR-88913', 'port_name': 'Port of Los Angeles', 'carrier_name': 'Maersk Line', 'excess_days': 1.8, 'daily_rate_usd': 275.0, 'total_demurrage_usd': 495.0, 'dispute_status': 'Under Review'},
    {'fee_id': 'DEM-2026-03', 'container_id': 'CNTR-88918', 'port_name': 'Port of Long Beach', 'carrier_name': 'Hapag-Lloyd', 'excess_days': 4.0, 'daily_rate_usd': 250.0, 'total_demurrage_usd': 1000.0, 'dispute_status': 'Disputed - Carrier Fault'}
])
demurrage.to_csv('data/demurrage_fees.csv', index=False)
