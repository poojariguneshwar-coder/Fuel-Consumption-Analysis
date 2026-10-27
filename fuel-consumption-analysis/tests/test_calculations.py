import pandas as pd
from analysis.calculations import calculate_metrics

def sample_records():
    return pd.DataFrame([
        {"record_id": 1, "vehicle_id": 1, "vehicle_code": "CAR-1", "fill_date": "2026-01-01",
         "odometer_km": 1000, "litres": 10, "total_cost": 1000, "full_tank_flag": True},
        {"record_id": 2, "vehicle_id": 1, "vehicle_code": "CAR-1", "fill_date": "2026-01-08",
         "odometer_km": 1150, "litres": 10, "total_cost": 1000, "full_tank_flag": True},
        {"record_id": 3, "vehicle_id": 1, "vehicle_code": "CAR-1", "fill_date": "2026-01-15",
         "odometer_km": 1300, "litres": 5, "total_cost": 500, "full_tank_flag": False},
    ])

def test_full_tank_mileage_uses_two_full_tank_records():
    result = calculate_metrics(sample_records())
    assert result.loc[1, "full_tank_mileage_kmpl"] == 15
    assert pd.isna(result.loc[0, "full_tank_mileage_kmpl"])
    assert pd.isna(result.loc[2, "full_tank_mileage_kmpl"])

def test_odometer_rollback_is_flagged():
    records = sample_records()
    records.loc[2, "odometer_km"] = 900
    result = calculate_metrics(records)
    assert bool(result.loc[2, "invalid_reading"]) is True
