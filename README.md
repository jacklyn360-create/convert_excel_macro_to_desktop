# Desktop Response Tracker

A Python desktop application replacing the Excel/VBA response form with a more maintainable and testable architecture.

## Features
- Response form for name, email, and question
- Validation before saving
- SQLite persistence
- List of saved responses
- CSV/Excel export

## Setup
1. Create a virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Run the app:
   python main.py

## Build executable
From the project root, run:

   pyinstaller --name "ResponseTracker" --onefile --windowed main.py

Or use the helper script:

   powershell -ExecutionPolicy Bypass -File scripts\build_app.ps1

## Project Structure
- app/
  - ui/
  - services/
  - domain/
  - repositories/
  - config/
- data/
- tests/
