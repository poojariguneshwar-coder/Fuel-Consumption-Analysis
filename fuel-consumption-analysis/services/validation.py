from datetime import date

def validate_vehicle(vehicle_code, vehicle_type, fuel_type):
    if not vehicle_code.strip():
        raise ValueError("Vehicle code cannot be empty.")
    if not vehicle_type.strip():
        raise ValueError("Vehicle type cannot be empty.")
    if not fuel_type.strip():
        raise ValueError("Fuel type cannot be empty.")

def validate_fuel_values(fill_date, odometer_km, litres, total_cost):
    if not isinstance(fill_date, date):
        raise ValueError("Fill date must be a valid date.")
    if odometer_km < 0:
        raise ValueError("Odometer reading cannot be negative.")
    if litres <= 0:
        raise ValueError("Litres must be greater than zero.")
    if total_cost < 0:
        raise ValueError("Total cost cannot be negative.")
