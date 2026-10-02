from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class SubmissionStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    CANCELLED = "cancelled"


@dataclass
class ResponseRecord:
    id: str
    name: str
    email: str
    question: str
    start_time: datetime
    completion_time: datetime
    status: SubmissionStatus = SubmissionStatus.SUBMITTED
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        *,
        id: str,
        name: str,
        email: str,
        question: str,
        start_time: datetime,
        completion_time: datetime,
        status: SubmissionStatus = SubmissionStatus.SUBMITTED,
    ) -> "ResponseRecord":
        now = datetime.now(timezone.utc)
        return cls(
            id=id,
            name=name.strip(),
            email=email.strip(),
            question=question.strip(),
            start_time=start_time,
            completion_time=completion_time,
            status=status,
            created_at=now,
            updated_at=now,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "question": self.question,
            "start_time": self.start_time.isoformat(),
            "completion_time": self.completion_time.isoformat(),
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
