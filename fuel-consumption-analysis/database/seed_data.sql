USE fuel_analysis;

INSERT INTO vehicles (vehicle_code, vehicle_type, fuel_type) VALUES
('CAR-001', 'Car', 'Petrol'),
('BIKE-001', 'Motorcycle', 'Petrol'),
('VAN-001', 'Van', 'Diesel')
ON DUPLICATE KEY UPDATE vehicle_type=VALUES(vehicle_type), fuel_type=VALUES(fuel_type);

-- Fictional sample data. Each vehicle has chronological odometer readings.
INSERT INTO fuel_records
(vehicle_id, fill_date, odometer_km, litres, total_cost, full_tank_flag, notes)
SELECT vehicle_id, '2026-01-05', 10000, 35.0, 3675.00, TRUE, 'Sample full tank'
FROM vehicles WHERE vehicle_code='CAR-001'
AND NOT EXISTS (SELECT 1 FROM fuel_records WHERE vehicle_id=vehicles.vehicle_id AND fill_date='2026-01-05');

INSERT INTO fuel_records
(vehicle_id, fill_date, odometer_km, litres, total_cost, full_tank_flag, notes)
SELECT vehicle_id, '2026-01-12', 10420, 32.0, 3360.00, TRUE, 'Sample full tank'
FROM vehicles WHERE vehicle_code='CAR-001'
AND NOT EXISTS (SELECT 1 FROM fuel_records WHERE vehicle_id=vehicles.vehicle_id AND fill_date='2026-01-12');

INSERT INTO fuel_records
(vehicle_id, fill_date, odometer_km, litres, total_cost, full_tank_flag, notes)
SELECT vehicle_id, '2026-02-03', 10820, 31.5, 3307.50, TRUE, 'Sample full tank'
FROM vehicles WHERE vehicle_code='CAR-001'
AND NOT EXISTS (SELECT 1 FROM fuel_records WHERE vehicle_id=vehicles.vehicle_id AND fill_date='2026-02-03');

INSERT INTO fuel_records
(vehicle_id, fill_date, odometer_km, litres, total_cost, full_tank_flag, notes)
SELECT vehicle_id, '2026-01-04', 5000, 8.0, 880.00, TRUE, 'Sample full tank'
FROM vehicles WHERE vehicle_code='BIKE-001'
AND NOT EXISTS (SELECT 1 FROM fuel_records WHERE vehicle_id=vehicles.vehicle_id AND fill_date='2026-01-04');

INSERT INTO fuel_records
(vehicle_id, fill_date, odometer_km, litres, total_cost, full_tank_flag, notes)
SELECT vehicle_id, '2026-01-10', 5240, 7.0, 770.00, TRUE, 'Sample full tank'
FROM vehicles WHERE vehicle_code='BIKE-001'
AND NOT EXISTS (SELECT 1 FROM fuel_records WHERE vehicle_id=vehicles.vehicle_id AND fill_date='2026-01-10');
