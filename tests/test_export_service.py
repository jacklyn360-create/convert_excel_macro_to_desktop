from datetime import datetime, timedelta, timezone

from app.domain.response_record import ResponseRecord, SubmissionStatus
from app.services.export_service import ExportService


def test_export_csv_creates_file(tmp_path):
    export_service = ExportService(base_dir=tmp_path)
    record = ResponseRecord(
        id="exp-1",
        name="Bob Example",
        email="bob@example.com",
        question="What should we build?",
        start_time=datetime.now(timezone.utc),
        completion_time=datetime.now(timezone.utc) + timedelta(minutes=2),
        status=SubmissionStatus.SUBMITTED,
    )

    export_path = export_service.export_csv([record])

    assert export_path.exists()
    assert export_path.suffix == ".csv"


def test_export_excel_creates_file(tmp_path):
    export_service = ExportService(base_dir=tmp_path)
    record = ResponseRecord(
        id="exp-2",
        name="Carol Example",
        email="carol@example.com",
        question="What else should be included?",
        start_time=datetime.now(timezone.utc),
        completion_time=datetime.now(timezone.utc) + timedelta(minutes=4),
        status=SubmissionStatus.SUBMITTED,
    )

    export_path = export_service.export_excel([record])

    assert export_path.exists()
    assert export_path.suffix == ".xlsx"
