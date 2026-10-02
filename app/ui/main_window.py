from __future__ import annotations

from datetime import datetime, timezone

from PySide6 import QtWidgets

from app.services.export_service import ExportService
from app.services.response_service import ResponseService
from app.services.validation_service import ValidationError


class ResponseTrackerWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.service = ResponseService()
        self.export_service = ExportService()
        self.start_time = datetime.now(timezone.utc)

        self.setWindowTitle("Response Tracker")
        self.resize(1000, 700)
        self._build_ui()
        self._refresh_response_table()

    def _build_ui(self) -> None:
        central = QtWidgets.QWidget()
        root_layout = QtWidgets.QVBoxLayout(central)

        title = QtWidgets.QLabel("Response Form")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        root_layout.addWidget(title)

        form_layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit()
        self.email_input = QtWidgets.QLineEdit()
        self.question_input = QtWidgets.QPlainTextEdit()
        self.question_input.setMinimumHeight(120)
        self.start_time_label = QtWidgets.QLabel(self.start_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
        self.completion_time_label = QtWidgets.QLabel("Pending")

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Question:", self.question_input)
        form_layout.addRow("Start time:", self.start_time_label)
        form_layout.addRow("Completion time:", self.completion_time_label)
        root_layout.addLayout(form_layout)

        buttons = QtWidgets.QHBoxLayout()
        submit_button = QtWidgets.QPushButton("Submit")
        clear_button = QtWidgets.QPushButton("Clear")
        export_csv_button = QtWidgets.QPushButton("Export CSV")
        export_excel_button = QtWidgets.QPushButton("Export Excel")

        submit_button.clicked.connect(self._handle_submit)
        clear_button.clicked.connect(self._clear_form)
        export_csv_button.clicked.connect(self._handle_export_csv)
        export_excel_button.clicked.connect(self._handle_export_excel)

        buttons.addWidget(submit_button)
        buttons.addWidget(clear_button)
        buttons.addWidget(export_csv_button)
        buttons.addWidget(export_excel_button)
        root_layout.addLayout(buttons)

        response_table_label = QtWidgets.QLabel("Saved responses")
        response_table_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        root_layout.addWidget(response_table_label)

        self.table_widget = QtWidgets.QTableWidget(0, 6)
        self.table_widget.setHorizontalHeaderLabels([
            "ID",
            "Name",
            "Email",
            "Start time",
            "Completion time",
            "Status",
        ])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        root_layout.addWidget(self.table_widget)

        self.setCentralWidget(central)

    def _clear_form(self) -> None:
        self.name_input.clear()
        self.email_input.clear()
        self.question_input.clear()
        self.start_time = datetime.now(timezone.utc)
        self.start_time_label.setText(self.start_time.strftime("%Y-%m-%d %H:%M:%S %Z"))
        self.completion_time_label.setText("Pending")

    def _handle_submit(self) -> None:
        payload = {
            "name": self.name_input.text(),
            "email": self.email_input.text(),
            "question": self.question_input.toPlainText(),
            "start_time": self.start_time.isoformat(),
            "completion_time": datetime.now(timezone.utc).isoformat(),
            "status": "submitted",
        }

        try:
            self.service.create_response(payload)
            self.completion_time_label.setText(datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %Z"))
            self._refresh_response_table()
            QtWidgets.QMessageBox.information(self, "Success", "Response saved successfully.")
            self._clear_form()
        except ValidationError as exc:
            QtWidgets.QMessageBox.warning(self, "Validation error", str(exc))
        except Exception as exc:  # pragma: no cover - UI safety net
            QtWidgets.QMessageBox.critical(self, "Error", f"Unable to save response: {exc}")

    def _handle_export_csv(self) -> None:
        records = self.service.list_responses()
        try:
            path = self.export_service.export_csv(records)
            QtWidgets.QMessageBox.information(self, "Export complete", f"CSV export saved to: {path}")
        except Exception as exc:  # pragma: no cover - UI safety net
            QtWidgets.QMessageBox.critical(self, "Export error", f"Unable to export CSV: {exc}")

    def _handle_export_excel(self) -> None:
        records = self.service.list_responses()
        try:
            path = self.export_service.export_excel(records)
            QtWidgets.QMessageBox.information(self, "Export complete", f"Excel export saved to: {path}")
        except Exception as exc:  # pragma: no cover - UI safety net
            QtWidgets.QMessageBox.critical(self, "Export error", f"Unable to export Excel: {exc}")

    def _refresh_response_table(self) -> None:
        records = self.service.list_responses()
        self.table_widget.setRowCount(len(records))

        for row_index, record in enumerate(records):
            self.table_widget.setItem(row_index, 0, QtWidgets.QTableWidgetItem(record.id[:8]))
            self.table_widget.setItem(row_index, 1, QtWidgets.QTableWidgetItem(record.name))
            self.table_widget.setItem(row_index, 2, QtWidgets.QTableWidgetItem(record.email))
            self.table_widget.setItem(row_index, 3, QtWidgets.QTableWidgetItem(record.start_time.strftime("%Y-%m-%d %H:%M:%S")))
            self.table_widget.setItem(row_index, 4, QtWidgets.QTableWidgetItem(record.completion_time.strftime("%Y-%m-%d %H:%M:%S")))
            self.table_widget.setItem(row_index, 5, QtWidgets.QTableWidgetItem(record.status.value))

        self.table_widget.resizeColumnsToContents()


def main() -> None:
    app = QtWidgets.QApplication([])
    window = ResponseTrackerWindow()
    window.show()
    app.exec()
