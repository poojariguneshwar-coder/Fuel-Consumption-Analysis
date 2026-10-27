from database.connection import get_connection
from services.validation import validate_vehicle

def add_vehicle():
    code = input("Vehicle code (e.g. CAR-002): ").strip().upper()
    vehicle_type = input("Vehicle type (Car/Motorcycle/Van): ").strip()
    fuel_type = input("Fuel type (Petrol/Diesel/CNG/Electric): ").strip()
    validate_vehicle(code, vehicle_type, fuel_type)
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO vehicles (vehicle_code, vehicle_type, fuel_type) VALUES (%s, %s, %s)",
            (code, vehicle_type, fuel_type)
        )
        connection.commit()
        print(f"Vehicle {code} added.")
    except Exception as exc:
        connection.rollback()
        if "Duplicate entry" in str(exc):
            raise ValueError("That vehicle code already exists.") from exc
        raise
    finally:
        connection.close()

def list_vehicles():
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT vehicle_id, vehicle_code, vehicle_type, fuel_type FROM vehicles ORDER BY vehicle_code")
        rows = cursor.fetchall()
        if not rows:
            print("No vehicles found.")
        for row in rows:
            print(f"ID {row['vehicle_id']} | {row['vehicle_code']} | {row['vehicle_type']} | {row['fuel_type']}")
    finally:
        connection.close()
