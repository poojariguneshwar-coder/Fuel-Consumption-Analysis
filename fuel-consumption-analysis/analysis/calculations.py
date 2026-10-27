import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {
    "record_id", "vehicle_id", "vehicle_code", "fill_date", "odometer_km",
    "litres", "total_cost", "full_tank_flag"
}

def calculate_metrics(records: pd.DataFrame) -> pd.DataFrame:
    """Return chronologically ordered records with interval and cost metrics."""
    missing = REQUIRED_COLUMNS - set(records.columns)
    if missing:
        raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")
    if records.empty:
        result = records.copy()
        for col in ["distance_km", "full_tank_mileage_kmpl", "approx_km_per_litre", "cost_per_km", "invalid_reading"]:
            result[col] = pd.Series(dtype="float64" if col != "invalid_reading" else "bool")
        return result

    df = records.copy()
    df["fill_date"] = pd.to_datetime(df["fill_date"])
    for col in ["odometer_km", "litres", "total_cost"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["full_tank_flag"] = df["full_tank_flag"].astype(bool)
    df = df.sort_values(["vehicle_id", "fill_date", "record_id"]).reset_index(drop=True)

    df["previous_odometer"] = df.groupby("vehicle_id")["odometer_km"].shift(1)
    df["previous_full_tank"] = df.groupby("vehicle_id")["full_tank_flag"].shift(1)
    df["distance_km"] = df["odometer_km"] - df["previous_odometer"]
    df["invalid_reading"] = (
        df["odometer_km"].isna() | (df["odometer_km"] < 0) |
        (df["litres"].isna()) | (df["litres"] <= 0) |
        (df["total_cost"].isna()) | (df["total_cost"] < 0) |
        (df["distance_km"] < 0)
    )
    df["full_tank_mileage_kmpl"] = np.where(
        (~df["invalid_reading"]) &
        df["full_tank_flag"] &
        df["previous_full_tank"].fillna(False) &
        (df["distance_km"] > 0),
        df["distance_km"] / df["litres"],
        np.nan
    )
    # This is intentionally labelled approximate, not full-tank mileage.
    df["approx_km_per_litre"] = np.where(
        (~df["invalid_reading"]) & (df["distance_km"] > 0),
        df["distance_km"] / df["litres"],
        np.nan
    )
    df["cost_per_km"] = np.where(
        (~df["invalid_reading"]) & (df["distance_km"] > 0),
        df["total_cost"] / df["distance_km"],
        np.nan
    )
    return df

def vehicle_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame(columns=["vehicle_code", "records", "total_litres", "total_expense",
                                     "average_full_tank_mileage_kmpl", "average_cost_per_km"])
    valid = metrics.loc[~metrics["invalid_reading"]].copy()
    return valid.groupby("vehicle_code", as_index=False).agg(
        records=("record_id", "count"),
        total_litres=("litres", "sum"),
        total_expense=("total_cost", "sum"),
        average_full_tank_mileage_kmpl=("full_tank_mileage_kmpl", "mean"),
        average_cost_per_km=("cost_per_km", "mean")
    )

def monthly_summary(metrics: pd.DataFrame) -> pd.DataFrame:
    if metrics.empty:
        return pd.DataFrame(columns=["month", "total_expense", "total_litres", "average_full_tank_mileage_kmpl"])
    valid = metrics.loc[~metrics["invalid_reading"]].copy()
    valid["month"] = valid["fill_date"].dt.to_period("M").astype(str)
    return valid.groupby("month", as_index=False).agg(
        total_expense=("total_cost", "sum"),
        total_litres=("litres", "sum"),
        average_full_tank_mileage_kmpl=("full_tank_mileage_kmpl", "mean")
    )
