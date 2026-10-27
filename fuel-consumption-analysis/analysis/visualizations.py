from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"

def create_charts(metrics: pd.DataFrame, monthly: pd.DataFrame):
    REPORT_DIR.mkdir(exist_ok=True)
    valid = metrics.loc[~metrics["invalid_reading"]] if not metrics.empty else metrics
    mileage = valid.dropna(subset=["full_tank_mileage_kmpl"]) if not valid.empty else valid

    if not mileage.empty:
        plt.figure(figsize=(9, 5))
        for code, group in mileage.groupby("vehicle_code"):
            plt.plot(group["fill_date"], group["full_tank_mileage_kmpl"], marker="o", label=code)
        plt.title("Full-Tank Mileage by Date")
        plt.xlabel("Fill date")
        plt.ylabel("Mileage (km/litre)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(REPORT_DIR / "mileage_trend.png", dpi=150)
        plt.close()

    if not monthly.empty:
        plt.figure(figsize=(9, 5))
        plt.bar(monthly["month"], monthly["total_expense"])
        plt.title("Monthly Fuel Expense")
        plt.xlabel("Month")
        plt.ylabel("Fuel expense")  
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(REPORT_DIR / "monthly_fuel_expense.png", dpi=150)
        plt.close()
