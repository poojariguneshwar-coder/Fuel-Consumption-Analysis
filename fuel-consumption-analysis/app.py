from services.vehicle_service import add_vehicle, list_vehicles
from services.fuel_service import add_fuel_record, list_fuel_records
from analysis.reports import generate_reports
from database.connection import initialize_database

def show_menu():
    print("\n=== FUEL CONSUMPTION ANALYSIS SYSTEM ===")
    print("1. Add vehicle")
    print("2. View vehicles")
    print("3. Add fuel record")
    print("4. View fuel records")
    print("5. Generate reports and charts")
    print("0. Exit")

def main():
    try:
        initialize_database()
    except Exception as exc:
        print(f"\nDatabase connection failed: {exc}")
        print("Check MySQL is running and your .env settings are correct.")
        return

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                add_vehicle()
            elif choice == "2":
                list_vehicles()
            elif choice == "3":
                add_fuel_record()
            elif choice == "4":
                list_fuel_records()
            elif choice == "5":
                generate_reports()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 0–5.")
        except (ValueError, RuntimeError) as exc:
            print(f"Could not complete operation: {exc}")
        except Exception as exc:
            print(f"Unexpected error: {exc}")

if __name__ == "__main__":
    main()
