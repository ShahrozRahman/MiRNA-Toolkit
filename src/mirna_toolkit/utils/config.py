from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ToolkitConfig:
    threads: int = 4
    working_dir: Path = Path(".")
    mirbase_version: Optional[str] = None
    targetscan_release: Optional[str] = None


def load_config(config_path: str | Path) -> ToolkitConfig:
    """Load a simple key=value config file."""
    cfg = ToolkitConfig()
    path = Path(config_path)
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = [x.strip() for x in line.split("=", 1)]
        if key == "threads":
            cfg.threads = int(value)
        elif key == "working_dir":
            cfg.working_dir = Path(value)
        elif key == "mirbase_version":
            cfg.mirbase_version = value
        elif key == "targetscan_release":
            cfg.targetscan_release = value
    return cfg
