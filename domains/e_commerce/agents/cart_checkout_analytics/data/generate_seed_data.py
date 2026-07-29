"""Generates synthetic seed CSV data for E-Commerce: Cart & Checkout Analytics agent."""

import csv
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
WINDOW_END = datetime(2026, 7, 24)


def generate_digital_funnel() -> None:
    headers = [
        "device_type",
        "date",
        "sessions_count",
        "cart_addition_sessions",
        "checkout_initiated_sessions",
        "order_completed_sessions",
        "conversion_rate_pct",
    ]
    devices = [
        ("Desktop", 12000, 4800, 3100, 1860),
        ("Mobile Web", 18500, 5550, 2960, 1110),
        ("Mobile App", 9500, 4750, 3325, 2375),
        ("Tablet", 2200, 770, 462, 242),
    ]

    records = []
    for day_offset in range(14, -1, -1):
        dt_str = (WINDOW_END - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for dev, base_sess, base_cart, base_chk, base_ord in devices:
            mult = 1.0 + (0.02 * ((day_offset % 5) - 2))
            sess = int(base_sess * mult)
            cart = int(base_cart * mult)
            chk = int(base_chk * mult)
            ord_comp = int(base_ord * mult)
            cvr = round((ord_comp / sess) * 100.0, 2)
            records.append([dev, dt_str, sess, cart, chk, ord_comp, cvr])

    with open(DATA_DIR / "digital_funnel.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)


def generate_cart_abandonment() -> None:
    headers = [
        "checkout_stage",
        "date",
        "abandoned_carts_count",
        "abandoned_revenue_dollars",
        "abandonment_rate_pct",
        "primary_exit_reason",
    ]
    stages_meta = [
        ("Cart Summary", 1450, 123250.00, 32.5, "Comparison Shopping"),
        ("Shipping Information", 2100, 189000.00, 41.2, "Unexpected Shipping Costs"),
        ("Payment Info", 1680, 159600.00, 35.8, "Payment Gateway Failure"),
        ("Order Review", 620, 58900.00, 14.5, "High Taxes/Fees"),
    ]

    records = []
    for day_offset in range(14, -1, -1):
        dt_str = (WINDOW_END - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for stage, base_count, base_rev, base_rate, exit_reason in stages_meta:
            mult = 1.0 + (0.015 * ((day_offset % 4) - 2))
            cnt = int(base_count * mult)
            rev = round(base_rev * mult, 2)
            rate = round(base_rate + (0.3 * ((day_offset % 3) - 1)), 2)
            records.append([stage, dt_str, cnt, rev, rate, exit_reason])

    with open(DATA_DIR / "cart_abandonment.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)


def generate_payment_exceptions() -> None:
    headers = [
        "payment_gateway",
        "date",
        "total_transactions",
        "failed_transactions",
        "decline_rate_pct",
        "gateway_error_code",
    ]
    gateways_meta = [
        ("Stripe", 14200, 426, 3.00, "ERR_INSUFFICIENT_FUNDS"),
        ("PayPal", 8500, 2975, 35.00, "ERR_GATEWAY_TIMEOUT"),
        ("Adyen", 6400, 160, 2.50, "ERR_3DS_AUTH_FAILED"),
        ("Apple Pay", 7100, 142, 2.00, "ERR_EXPIRED_CARD"),
        ("Klarna", 3200, 128, 4.00, "ERR_AVS_MISMATCH"),
    ]

    records = []
    for day_offset in range(14, -1, -1):
        dt_str = (WINDOW_END - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for gw, total_tx, failed_tx, base_dec, err_code in gateways_meta:
            mult = 1.0 + (0.02 * ((day_offset % 4) - 2))
            tot = int(total_tx * mult)
            if gw == "PayPal" and day_offset <= 3:
                fail = int(tot * 0.35)
                dec = 35.00
            elif gw == "PayPal":
                fail = int(tot * 0.035)
                dec = 3.50
            else:
                fail = int(failed_tx * mult)
                dec = round((fail / tot) * 100.0, 2)
            records.append([gw, dt_str, tot, fail, dec, err_code])

    with open(DATA_DIR / "payment_exceptions.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)


def generate_promo_code_validation() -> None:
    headers = [
        "promo_code",
        "date",
        "attempts_count",
        "successful_redemptions",
        "failed_validations",
        "error_type",
    ]
    promos_meta = [
        ("SUMMER20", 3500, 3150, 350, "Minimum Spend Not Met"),
        ("WELCOME10", 2200, 2090, 110, "Usage Limit Exceeded"),
        ("FREESHIP", 1800, 1710, 90, "Excluded Category"),
        ("EXPIRED50", 950, 0, 950, "Code Expired"),
        ("VIPFLASH", 1400, 1330, 70, "Invalid Code"),
    ]

    records = []
    for day_offset in range(14, -1, -1):
        dt_str = (WINDOW_END - timedelta(days=day_offset)).strftime("%Y-%m-%d")
        for code, base_att, base_succ, base_fail, err_type in promos_meta:
            mult = 1.0 + (0.02 * ((day_offset % 3) - 1))
            att = int(base_att * mult)
            succ = int(base_succ * mult) if base_succ > 0 else 0
            fail = att - succ
            records.append([code, dt_str, att, succ, fail, err_type])

    with open(DATA_DIR / "promo_code_validation.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(records)


def main() -> None:
    generate_digital_funnel()
    generate_cart_abandonment()
    generate_payment_exceptions()
    generate_promo_code_validation()
    print("Successfully generated all 4 cart_checkout_analytics CSV files.")


if __name__ == "__main__":
    main()
