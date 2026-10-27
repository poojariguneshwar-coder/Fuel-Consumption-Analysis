from datetime import date
import pytest
from services.validation import validate_vehicle, validate_fuel_values

def test_vehicle_validation_accepts_normal_values():
    validate_vehicle("CAR-1", "Car", "Petrol")

@pytest.mark.parametrize("values", [
    ("", "Car", "Petrol"),
    ("CAR-1", "", "Petrol"),
    ("CAR-1", "Car", ""),
])
def test_vehicle_validation_rejects_blank_fields(values):
    with pytest.raises(ValueError):
        validate_vehicle(*values)

def test_fuel_validation_rejects_zero_litres():
    with pytest.raises(ValueError):
        validate_fuel_values(date(2026, 1, 1), 100, 0, 100)

def test_fuel_validation_rejects_negative_cost():
    with pytest.raises(ValueError):
        validate_fuel_values(date(2026, 1, 1), 100, 1, -1)
