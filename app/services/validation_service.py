from __future__ import annotations

import re
from datetime import datetime

from app.domain.response_record import ResponseRecord, SubmissionStatus


class ValidationError(ValueError):
    pass


class ValidationService:
    EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @staticmethod
    def validate_name(name: str) -> str:
        cleaned = (name or "").strip()
        if not cleaned:
            raise ValidationError("Name is required.")
        return cleaned

    @staticmethod
    def validate_email(email: str) -> str:
        cleaned = (email or "").strip()
        if not cleaned:
            raise ValidationError("Email is required.")
        if not ValidationService.EMAIL_PATTERN.match(cleaned):
            raise ValidationError("Email format is invalid.")
        return cleaned

    @staticmethod
    def validate_question(question: str) -> str:
        cleaned = (question or "").strip()
        if not cleaned:
            raise ValidationError("Question is required.")
        return cleaned

    @staticmethod
    def validate_status(status: str | SubmissionStatus) -> SubmissionStatus:
        if isinstance(status, SubmissionStatus):
            return status
        try:
            return SubmissionStatus(status)
        except ValueError as exc:
            raise ValidationError("Status is invalid.") from exc

    @staticmethod
    def validate_response(record: ResponseRecord) -> ResponseRecord:
        record.name = ValidationService.validate_name(record.name)
        record.email = ValidationService.validate_email(record.email)
        record.question = ValidationService.validate_question(record.question)
        record.status = ValidationService.validate_status(record.status)

        if record.completion_time < record.start_time:
            raise ValidationError("Completion time cannot be earlier than start time.")

        return record

    @staticmethod
    def validate_datetime(value: datetime | str | None, field_name: str) -> datetime:
        if value is None:
            raise ValidationError(f"{field_name} is required.")

        if isinstance(value, datetime):
            return value

        try:
            return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValidationError(f"{field_name} has an invalid date format.") from exc
