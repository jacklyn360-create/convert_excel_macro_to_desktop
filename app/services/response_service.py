from __future__ import annotations

from datetime import datetime

from app.domain.response_record import ResponseRecord, SubmissionStatus
from app.repositories.response_repository import ResponseRepository
from app.services.validation_service import ValidationError, ValidationService


class ResponseService:
    def __init__(self, repository: ResponseRepository | None = None):
        self.repository = repository or ResponseRepository()

    def create_response(self, payload: dict) -> ResponseRecord:
        record = ResponseRecord(
            id=payload.get("id") or self._new_id(),
            name=payload.get("name", ""),
            email=payload.get("email", ""),
            question=payload.get("question", ""),
            start_time=ValidationService.validate_datetime(payload.get("start_time"), "Start time"),
            completion_time=ValidationService.validate_datetime(payload.get("completion_time"), "Completion time"),
            status=ValidationService.validate_status(payload.get("status", SubmissionStatus.SUBMITTED)),
        )

        validated = ValidationService.validate_response(record)
        return self.repository.add(validated)

    def list_responses(self) -> list[ResponseRecord]:
        return self.repository.list_all()

    def get_response_by_id(self, response_id: str) -> ResponseRecord | None:
        return self.repository.get_by_id(response_id)

    def update_response(self, response_id: str, payload: dict) -> ResponseRecord:
        existing = self.repository.get_by_id(response_id)
        if existing is None:
            raise ValidationError("Response not found.")

        updated = ResponseRecord(
            id=existing.id,
            name=payload.get("name", existing.name),
            email=payload.get("email", existing.email),
            question=payload.get("question", existing.question),
            start_time=ValidationService.validate_datetime(
                payload.get("start_time", existing.start_time),
                "Start time",
            ),
            completion_time=ValidationService.validate_datetime(
                payload.get("completion_time", existing.completion_time),
                "Completion time",
            ),
            status=ValidationService.validate_status(payload.get("status", existing.status)),
            created_at=existing.created_at,
            updated_at=datetime.utcnow(),
        )

        validated = ValidationService.validate_response(updated)
        return self.repository.update(validated)

    def delete_response(self, response_id: str) -> bool:
        return self.repository.delete(response_id)

    @staticmethod
    def _new_id() -> str:
        import uuid

        return str(uuid.uuid4())
