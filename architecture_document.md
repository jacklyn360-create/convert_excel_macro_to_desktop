# Desktop Application Architecture Document

## 1. Purpose
This document defines the target architecture for replacing the current VBA-based Excel application with a Python desktop application. The current workbook-based solution is a lightweight respondent data capture tool; the new architecture will preserve the same business intent while improving maintainability, validation, scalability, and user experience.

## 2. Background
The existing solution consists of:
- an Excel macro-enabled workbook
- a simple VBA UserForm
- a table-based data structure for captured responses
- placeholder behavior such as a message box on button click

The workbook currently supports record tracking for:
- response ID
- start time
- completion time
- email
- name
- question/response text

The replacement architecture should convert this into a proper desktop application with structured business logic, validation, and data persistence.

## 3. Business Goals
The desktop application should:
- replace the Excel/VBA form with a modern desktop interface
- simplify data entry and validation
- store records in a reliable database rather than a spreadsheet table
- support future expansion without exposing business logic in the UI layer
- enable cleaner reporting, import/export, and maintenance

## 4. Scope
### In Scope
- Desktop user interface for form entry
- Submission tracking and validation
- Persistence of response records
- Export to spreadsheet-compatible formats when needed
- Basic reporting and listing of saved responses
- Audit-friendly timestamps and record metadata

### Out of Scope for v1
- Multi-user concurrent editing in a spreadsheet-like model
- Complex workflow approval chains
- External integration APIs
- Advanced role-based authorization
- Large-scale analytics or BI dashboards

## 5. Architectural Principles
- Keep business logic separate from the UI
- Favor explicit data models over hidden spreadsheet assumptions
- Use a persistent database instead of workbook cells for record storage
- Design for testability and maintainability
- Support future migration to a web or cloud solution without rewriting the core domain layer
- Minimize dependence on Excel-specific behavior

## 6. Target Architecture Overview
The proposed system will be a layered desktop application built with Python.

### 6.1 Layers
1. Presentation Layer
   - Desktop UI built using PySide6 or tkinter
   - Main form for entering responses
   - Data grid or list view for viewing saved records
   - Validation messages and confirmation dialogs

2. Application Layer
   - Business services for submission processing
   - Validation and workflow rules
   - Form orchestration logic
   - Export/reporting services

3. Domain Layer
   - Data entities such as ResponseRecord
   - Value objects and validation rules
   - Core business rules for record creation, update, and status handling

4. Data Access Layer
   - SQLite for local desktop deployment
   - Optional PostgreSQL for future multi-user deployment
   - Repository classes for CRUD operations

5. Integration Layer
   - Excel import/export support
   - Optional CSV export
   - Future connectors to APIs or external systems

## 7. Proposed Technology Stack
### Python Runtime
- Python 3.11+

### Desktop UI
- PySide6 for a modern, professional desktop interface
- Alternative: tkinter for a lighter-weight app

### Data Access
- SQLite for local single-user deployment
- SQLAlchemy for ORM or data abstraction
- Optional PostgreSQL for enterprise deployment later

### Business Logic and Validation
- Python dataclasses or pydantic models
- service-layer classes

### File/Spreadsheet Support
- openpyxl for Excel workbook interaction
- pandas for data export or reporting if needed

### Quality and Testability
- pytest for automated testing
- logging for runtime diagnostics
- configuration management via environment variables or config files

## 8. Component Breakdown
### 8.1 UI Components
- Main application window
- Response form screen
- Submission confirmation dialog
- Response list/report screen
- Settings screen (optional)

### 8.2 Service Components
- ResponseService
  - create response
  - validate fields
  - save response
  - get all responses
  - export responses

- ValidationService
  - required field checks
  - email validation
  - timestamp checks
  - duplicate or invalid data prevention

- ExportService
  - export to CSV or Excel
  - generate summary reports

### 8.3 Data Components
- ResponseRepository
  - insert response
  - update response
  - fetch by ID
  - fetch all records

- DataContext
  - manages SQLite/PostgreSQL connection lifecycle

## 9. Data Model
### Core Entity: ResponseRecord
- id: string or integer
- start_time: datetime
- completion_time: datetime
- email: string
- name: string
- question: text
- created_at: datetime
- updated_at: datetime
- status: enum (draft, submitted, cancelled)

### Optional Fields for future versions
- user_id
- department
- source_channel
- archived
- notes

## 10. Process Flow
1. User opens the application.
2. App loads form screen.
3. User enters required information.
4. App validates input in real time or on submit.
5. App stores response in database.
6. App records timestamps for start and completion.
7. App confirms submission to user.
8. User can view saved responses and export them.

## 11. Non-Functional Requirements
### Performance
- Form load time under 2 seconds on standard desktop hardware
- Submission processing under 1 second for normal record volumes

### Reliability
- No data loss during normal submission flows
- Graceful handling of database or disk errors

### Usability
- Intuitive form layout
- Clear validation feedback
- Minimal training required for end users

### Maintainability
- Separation of UI, services, and data access
- Unit tests for validation and persistence logic
- Clear folder structure with modular design

### Security
- Local data protection on user machine
- Avoid plaintext secrets in source code
- Support file permissions and encrypted storage where required

## 12. Deployment Model
### v1 Deployment
- Single-user desktop application
- SQLite database stored in the application data directory
- Installer created with PyInstaller or a similar packaging tool

### Future Deployment
- Move to PostgreSQL for multi-user scenarios
- Shift to central server with remote clients
- Add authentication and audit logging

## 13. Migration Strategy from VBA
1. Inventory current Excel/VBA logic and workbook structure
2. Map spreadsheet columns to domain entities
3. Replace spreadsheet-based storage with database tables
4. Recreate the form as a desktop UI
5. Rebuild validation logic in Python
6. Add import/export compatibility with Excel files
7. Test against existing sample data
8. Cut over to the new application with a fallback export path

## 14. Risks and Mitigations
### Risk: Spreadsheet assumptions embedded in business logic
Mitigation: move logic into explicit Python service classes and tests.

### Risk: Data inconsistency during migration
Mitigation: validate migrated data against the original workbook records.

### Risk: Inadequate user experience
Mitigation: iterative UI prototyping and usability testing.

### Risk: Hidden business rules not documented
Mitigation: conduct review sessions with workbook owner and end users.

## 15. Recommended Initial Folder Structure
project/
- app/
  - ui/
  - services/
  - domain/
  - repositories/
  - config/
- data/
  - db/
  - exports/
- tests/
- scripts/
- requirements.txt
- README.md

## 16. Recommended MVP Scope
The first production-ready desktop version should include:
- main response form
- field validation
- data persistence to SQLite
- list/report view of saved records
- CSV or Excel export
- basic error handling and logs

## 17. Decision Summary
The best architecture for replacing the VBA application is a Python desktop app with a layered design:
- PySide6 for UI
- SQLite for data persistence
- Python service layer for business logic
- repository pattern for database access
- optional Excel compatibility via openpyxl

This approach preserves the original functionality while making the solution cleaner, more maintainable, and easier to evolve.

## 18. Next Step
The next phase should be to create a technical design document and then implement the MVP structure, beginning with the form, data model, and persistence layer.
