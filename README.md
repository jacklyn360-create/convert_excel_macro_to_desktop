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

## Project Structure
- app/
  - ui/
  - services/
  - domain/
  - repositories/
  - config/
- data/
- tests/
