import mysql.connector
from config.settings import DB_CONFIG

def get_connection(with_database=True):
    config = DB_CONFIG.copy()
    if not with_database:
        config.pop("database", None)
    return mysql.connector.connect(**config)

def initialize_database():
    """Create tables if missing. The configured database must already exist."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_code VARCHAR(30) NOT NULL UNIQUE,
                vehicle_type VARCHAR(50) NOT NULL,
                fuel_type VARCHAR(30) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS fuel_records (
                record_id INT AUTO_INCREMENT PRIMARY KEY,
                vehicle_id INT NOT NULL,
                fill_date DATE NOT NULL,
                odometer_km DECIMAL(12,2) NOT NULL,
                litres DECIMAL(10,3) NOT NULL,
                total_cost DECIMAL(12,2) NOT NULL,
                full_tank_flag BOOLEAN NOT NULL DEFAULT FALSE,
                notes VARCHAR(255) NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_fuel_vehicle FOREIGN KEY (vehicle_id)
                    REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
                CONSTRAINT chk_litres_positive CHECK (litres > 0),
                CONSTRAINT chk_cost_nonnegative CHECK (total_cost >= 0),
                CONSTRAINT chk_odometer_nonnegative CHECK (odometer_km >= 0),
                INDEX idx_fuel_vehicle_date (vehicle_id, fill_date, record_id)
            )
        """)
        connection.commit()
    finally:
        connection.close()
