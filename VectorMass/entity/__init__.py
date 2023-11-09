from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DatabaseConfig:
    db_name: str