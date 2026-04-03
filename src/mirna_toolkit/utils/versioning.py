import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class DatabaseVersion:
    name: str
    version: str
    retrieved_at: str
    source_url: str


class DatabaseVersionTracker:
    """Track external database versions used by analyses."""

    def __init__(self) -> None:
        self._entries: list[DatabaseVersion] = []

    def add(self, entry: DatabaseVersion) -> None:
        self._entries.append(entry)

    def to_dict(self) -> list[dict[str, str]]:
        return [asdict(e) for e in self._entries]

    def export_json(self, output_path: str | Path) -> Path:
        output = Path(output_path)
        output.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")
        return output
