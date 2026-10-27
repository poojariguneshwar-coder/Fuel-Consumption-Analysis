from dataclasses import dataclass
from datetime import date
from decimal import Decimal

@dataclass
class FuelRecord:
    vehicle_id: int
    fill_date: date
    odometer_km: Decimal
    litres: Decimal
    total_cost: Decimal
    full_tank_flag: bool
    notes: str = ""
