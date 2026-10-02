from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppSettings:
    app_name: str = "Response Tracker"
    app_version: str = "0.1.0"
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"
    db_name: str = "app.db"
    export_dir: Path = Path(__file__).resolve().parents[2] / "data" / "exports"
    log_level: str = "INFO"

    @property
    def db_path(self) -> Path:
        return self.data_dir / self.db_name


settings = AppSettings()
