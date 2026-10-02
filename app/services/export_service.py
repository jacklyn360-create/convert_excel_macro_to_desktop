from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

from openpyxl import Workbook

from app.config.settings import settings
from app.domain.response_record import ResponseRecord


class ExportService:
    def __init__(self, base_dir: str | Path | None = None):
        self.base_dir = Path(base_dir) if base_dir is not None else settings.export_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def export_csv(self, records: list[ResponseRecord], destination: str | Path | None = None) -> Path:
        export_path = Path(destination) if destination is not None else self.base_dir / self._build_filename("csv")
        export_path.parent.mkdir(parents=True, exist_ok=True)

        with export_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                "id",
                "name",
                "email",
                "question",
                "start_time",
                "completion_time",
                "status",
                "created_at",
                "updated_at",
            ])
            for record in records:
                writer.writerow([
                    record.id,
                    record.name,
                    record.email,
                    record.question,
                    record.start_time.isoformat(),
                    record.completion_time.isoformat(),
                    record.status.value,
                    record.created_at.isoformat(),
                    record.updated_at.isoformat(),
                ])

        return export_path

    def export_excel(self, records: list[ResponseRecord], destination: str | Path | None = None) -> Path:
        export_path = Path(destination) if destination is not None else self.base_dir / self._build_filename("xlsx")
        export_path.parent.mkdir(parents=True, exist_ok=True)

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Responses"
        worksheet.append([
            "id",
            "name",
            "email",
            "question",
            "start_time",
            "completion_time",
            "status",
            "created_at",
            "updated_at",
        ])

        for record in records:
            worksheet.append([
                record.id,
                record.name,
                record.email,
                record.question,
                record.start_time.isoformat(),
                record.completion_time.isoformat(),
                record.status.value,
                record.created_at.isoformat(),
                record.updated_at.isoformat(),
            ])

        workbook.save(export_path)
        return export_path

    @staticmethod
    def _build_filename(extension: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"responses_{timestamp}.{extension}"
