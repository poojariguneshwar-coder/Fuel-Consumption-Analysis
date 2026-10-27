from pathlib import Path
import pandas as pd
from database.connection import get_connection
from analysis.calculations import calculate_metrics, vehicle_summary, monthly_summary
from analysis.visualizations import create_charts

REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"

def load_records():
    connection = get_connection()
    try:
        query = """
            SELECT fr.record_id, fr.vehicle_id, v.vehicle_code, v.vehicle_type, v.fuel_type,
                   fr.fill_date, fr.odometer_km, fr.litres, fr.total_cost,
                   fr.full_tank_flag, fr.notes
            FROM fuel_records fr
            JOIN vehicles v ON v.vehicle_id = fr.vehicle_id
            ORDER BY fr.vehicle_id, fr.fill_date, fr.record_id
        """
        return pd.read_sql(query, connection)
    finally:
        connection.close()

def generate_reports():
    REPORT_DIR.mkdir(exist_ok=True)
    records = load_records()
    if records.empty:
        print("No records available. Add records or load database/seed_data.sql first.")
        return
    metrics = calculate_metrics(records)
    vehicles = vehicle_summary(metrics)
    monthly = monthly_summary(metrics)
    invalid = metrics.loc[metrics["invalid_reading"]].copy()

    metrics.to_csv(REPORT_DIR / "fuel_records_analysis.csv", index=False)
    vehicles.to_csv(REPORT_DIR / "vehicle_wise_summary.csv", index=False)
    monthly.to_csv(REPORT_DIR / "monthly_summary.csv", index=False)
    invalid.to_csv(REPORT_DIR / "invalid_readings.csv", index=False)
    create_charts(metrics, monthly)

    print("\\n--- VEHICLE-WISE SUMMARY ---")
    print(vehicles.round(2).to_string(index=False))
    print("\\n--- MONTHLY SUMMARY ---")
    print(monthly.round(2).to_string(index=False))
    print(f"Invalid readings flagged: {len(invalid)}")
    print(f"Reports saved to: {REPORT_DIR}")
    print("Note: partial-fill km/litre values are approximate and are not used as full-tank mileage.")
