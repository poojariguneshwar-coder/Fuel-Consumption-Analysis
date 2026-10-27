from datetime import date
from decimal import Decimal, InvalidOperation
from database.connection import get_connection
from services.validation import validate_fuel_values

def _ask_decimal(prompt):
    try:
        return Decimal(input(prompt).strip())
    except InvalidOperation as exc:
        raise ValueError("Enter a valid number.") from exc

def add_fuel_record():
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT vehicle_id, vehicle_code FROM vehicles ORDER BY vehicle_code")
        vehicles = cursor.fetchall()
        if not vehicles:
            print("Add a vehicle first.")
            return
        print("Available vehicles:")
        for vehicle in vehicles:
            print(f"{vehicle['vehicle_id']}. {vehicle['vehicle_code']}")
        vehicle_id = int(input("Vehicle ID: ").strip())
        if vehicle_id not in {v['vehicle_id'] for v in vehicles}:
            raise ValueError("Unknown vehicle ID.")
        fill_date = date.fromisoformat(input("Fill date (YYYY-MM-DD): ").strip())
        odometer = _ask_decimal("Odometer reading in km: ")
        litres = _ask_decimal("Litres purchased: ")
        cost = _ask_decimal("Total cost: ")
        full_answer = input("Was this a full-tank fill? (y/n): ").strip().lower()
        if full_answer not in ("y", "n"):
            raise ValueError("Enter y or n for full-tank status.")
        full_tank = full_answer == "y"
        notes = input("Notes (optional): ").strip() or None
        validate_fuel_values(fill_date, odometer, litres, cost)

        cursor.execute("""
            SELECT fill_date, odometer_km FROM fuel_records
            WHERE vehicle_id = %s
            ORDER BY fill_date DESC, record_id DESC LIMIT 1
        """, (vehicle_id,))
        previous = cursor.fetchone()
        if previous and fill_date < previous["fill_date"]:
            raise ValueError("This date is earlier than the latest existing record for this vehicle.")
        if previous and fill_date == previous["fill_date"] and odometer < Decimal(str(previous["odometer_km"])):
            raise ValueError("Odometer reading cannot go backwards on the same date.")
        if previous and odometer < Decimal(str(previous["odometer_km"])):
            raise ValueError("Odometer reading cannot be lower than the previous reading.")

        cursor.execute("""
            INSERT INTO fuel_records
            (vehicle_id, fill_date, odometer_km, litres, total_cost, full_tank_flag, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (vehicle_id, fill_date, str(odometer), str(litres), str(cost), full_tank, notes))
        connection.commit()
        print("Fuel record saved.")
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

def list_fuel_records():
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT fr.record_id, v.vehicle_code, fr.fill_date, fr.odometer_km,
                   fr.litres, fr.total_cost, fr.full_tank_flag
            FROM fuel_records fr JOIN vehicles v ON v.vehicle_id=fr.vehicle_id
            ORDER BY v.vehicle_code, fr.fill_date, fr.record_id
        """)
        rows = cursor.fetchall()
        if not rows:
            print("No fuel records found.")
        for r in rows:
            status = "Full tank" if r["full_tank_flag"] else "Partial/unknown"
            print(f"#{r['record_id']} | {r['vehicle_code']} | {r['fill_date']} | "
                  f"{r['odometer_km']} km | {r['litres']} L | {r['total_cost']} | {status}")
    finally:
        connection.close()
