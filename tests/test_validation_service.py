from datetime import datetime, timedelta, timezone

import pytest

from app.domain.response_record import ResponseRecord, SubmissionStatus
from app.services.validation_service import ValidationError, ValidationService


def test_valid_response_passes_validation():
    start = datetime.now(timezone.utc)
    completion = start + timedelta(minutes=5)
    record = ResponseRecord(
        id="1",
        name="Jane Doe",
        email="jane@example.com",
        question="What is the issue?",
        start_time=start,
        completion_time=completion,
        status=SubmissionStatus.SUBMITTED,
    )

    validated = ValidationService.validate_response(record)

    assert validated.name == "Jane Doe"
    assert validated.email == "jane@example.com"
    assert validated.question == "What is the issue?"


def test_empty_name_raises_error():
    record = ResponseRecord(
        id="2",
        name="   ",
        email="jane@example.com",
        question="Question",
        start_time=datetime.now(timezone.utc),
        completion_time=datetime.now(timezone.utc) + timedelta(minutes=1),
    )

    with pytest.raises(ValidationError, match="Name is required"):
        ValidationService.validate_response(record)


def test_invalid_email_raises_error():
    record = ResponseRecord(
        id="3",
        name="Jane Doe",
        email="not-an-email",
        question="Question",
        start_time=datetime.now(timezone.utc),
        completion_time=datetime.now(timezone.utc) + timedelta(minutes=1),
    )

    with pytest.raises(ValidationError, match="Email format is invalid"):
        ValidationService.validate_response(record)


def test_completion_before_start_raises_error():
    start = datetime.now(timezone.utc)
    record = ResponseRecord(
        id="4",
        name="Jane Doe",
        email="jane@example.com",
        question="Question",
        start_time=start,
        completion_time=start - timedelta(minutes=1),
    )

    with pytest.raises(ValidationError, match="Completion time cannot be earlier"):
        ValidationService.validate_response(record)
