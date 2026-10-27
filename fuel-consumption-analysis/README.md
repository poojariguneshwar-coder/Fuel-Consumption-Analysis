# Fuel Consumption Analysis System

A beginner-friendly command-line application using Python, MySQL, Pandas, NumPy and Matplotlib.

## Features
- Manage vehicles and fuel purchases
- Store odometer reading, date, litres, total cost and full-tank status
- Validate positive litres/cost and non-decreasing odometer readings
- Calculate full-tank mileage only when consecutive records are both marked full tank
- Flag partial-fill and invalid-reading limitations
- Export vehicle and monthly CSV summaries
- Create mileage and monthly fuel-expense charts
- Include automated tests for calculations and validation

## Requirements
- Python 3.10+
- MySQL Server 8+
- A MySQL account that can create/use the configured database

## Setup (Windows PowerShell)
1. Install Python and MySQL Server.
2. Open a terminal in this project folder.
3. Create a virtual environment:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. Install packages:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and update the database settings.
6. In MySQL, create the database and application user (adjust the password):
   ```sql
   CREATE DATABASE fuel_analysis;
   CREATE USER 'fuel_app'@'localhost' IDENTIFIED BY 'change_me';
   GRANT ALL PRIVILEGES ON fuel_analysis.* TO 'fuel_app'@'localhost';
   FLUSH PRIVILEGES;
   ```
   Use the same credentials in `.env`. If you use an existing MySQL account, adjust `.env` instead.
7. Run the application:
   ```powershell
   python app.py
   ```
   The app creates the tables automatically. To load the sample records, run `database/seed_data.sql` in MySQL Workbench after the tables exist.

## Run tests
```powershell
python -m pytest -v
```

## Mileage rules and limitations
- **Full-tank method:** mileage is calculated only when the current and previous records for a vehicle are both marked as full-tank fills. Distance is the difference between their odometer readings, divided by litres added at the current fill.
- **Partial fills:** distance divided by litres bought is only a rough indicator because the fuel consumed may not equal the amount purchased during that interval. These records are not presented as reliable full-tank mileage.
- Odometer readings must not go backwards for a vehicle. Equal readings are permitted but produce zero distance and no mileage.
- Records are sorted by date and record ID before calculations. An earlier-dated record added later can make the sequence invalid; the invalid-reading report flags it.
- Sample records are fictional demonstration data, not real vehicle advice.

## Generated output
After selecting menu option 5, CSV summaries and PNG charts are written into `reports/`.

## Git and GitHub
See `docs/git_commands.md`.
