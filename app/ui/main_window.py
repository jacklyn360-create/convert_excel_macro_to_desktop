from __future__ import annotations

from PySide6 import QtWidgets


def main() -> None:
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    window.setWindowTitle("Response Tracker")
    window.resize(900, 600)

    central = QtWidgets.QWidget()
    layout = QtWidgets.QVBoxLayout(central)

    label = QtWidgets.QLabel("Welcome to the response tracker")
    label.setStyleSheet("font-size: 20px; font-weight: bold;")
    layout.addWidget(label)

    info = QtWidgets.QLabel("The application shell is initialized and ready for the form workflow.")
    layout.addWidget(info)

    window.setCentralWidget(central)
    window.show()
    app.exec()
