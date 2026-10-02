from __future__ import annotations

from datetime import datetime
from typing import Sequence

from app.domain.response_record import ResponseRecord, SubmissionStatus
from app.repositories.db_context import DatabaseContext


class ResponseRepository:
    def __init__(self, db_path=None):
        self.db_context = DatabaseContext(db_path)

    def add(self, response: ResponseRecord) -> ResponseRecord:
        with self.db_context.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO responses (
                    id, name, email, question, start_time, completion_time,
                    status, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    response.id,
                    response.name,
                    response.email,
                    response.question,
                    response.start_time.isoformat(),
                    response.completion_time.isoformat(),
                    response.status.value,
                    response.created_at.isoformat(),
                    response.updated_at.isoformat(),
                ),
            )
            connection.commit()
        return response

    def get_by_id(self, response_id: str) -> ResponseRecord | None:
        with self.db_context.get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM responses WHERE id = ?",
                (response_id,),
            ).fetchone()

        if row is None:
            return None

        return self._row_to_record(row)

    def list_all(self) -> list[ResponseRecord]:
        with self.db_context.get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM responses ORDER BY created_at DESC"
            ).fetchall()

        return [self._row_to_record(row) for row in rows]

    def update(self, response: ResponseRecord) -> ResponseRecord:
        with self.db_context.get_connection() as connection:
            connection.execute(
                """
                UPDATE responses
                SET name = ?, email = ?, question = ?, start_time = ?, completion_time = ?,
                    status = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    response.name,
                    response.email,
                    response.question,
                    response.start_time.isoformat(),
                    response.completion_time.isoformat(),
                    response.status.value,
                    response.updated_at.isoformat(),
                    response.id,
                ),
            )
            connection.commit()
        return response

    def delete(self, response_id: str) -> bool:
        with self.db_context.get_connection() as connection:
            cursor = connection.execute(
                "DELETE FROM responses WHERE id = ?",
                (response_id,),
            )
            connection.commit()
        return cursor.rowcount > 0

    @staticmethod
    def _row_to_record(row) -> ResponseRecord:
        return ResponseRecord(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            question=row["question"],
            start_time=datetime.fromisoformat(row["start_time"]),
            completion_time=datetime.fromisoformat(row["completion_time"]),
            status=SubmissionStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
