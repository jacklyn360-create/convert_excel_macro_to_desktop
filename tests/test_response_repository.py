from datetime import datetime, timedelta, timezone

from app.domain.response_record import ResponseRecord, SubmissionStatus
from app.repositories.response_repository import ResponseRepository


def test_repository_can_add_and_fetch_response(tmp_path):
    repo = ResponseRepository(db_path=tmp_path / "test_app.db")

    start = datetime.now(timezone.utc)
    completion = start + timedelta(minutes=3)
    record = ResponseRecord(
        id="repo-1",
        name="Alice Example",
        email="alice@example.com",
        question="How can we help?",
        start_time=start,
        completion_time=completion,
        status=SubmissionStatus.SUBMITTED,
    )

    repo.add(record)
    saved = repo.get_by_id("repo-1")

    assert saved is not None
    assert saved.name == "Alice Example"
    assert saved.email == "alice@example.com"
    assert saved.question == "How can we help?"
