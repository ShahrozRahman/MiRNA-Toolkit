from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from ..utils.http import safe_get_json

HMDD_ENDPOINT = "https://www.cuilab.cn/hmdd/api/v1/associations"


def get_associations(mirna_id: str, timeout: int = 60, strict: bool = False) -> list[dict[str, Any]]:
    payload = safe_get_json(HMDD_ENDPOINT, params={"mirna": mirna_id}, timeout=timeout, strict=strict)
    if payload is None:
        return []
    if isinstance(payload, dict) and "data" in payload:
        return list(payload["data"])
    if isinstance(payload, list):
        return payload
    return []


def build_network_edges(associations: list[dict[str, Any]]) -> list[tuple[str, str]]:
    edges: list[tuple[str, str]] = []
    for row in associations:
        mirna = str(row.get("mirna") or row.get("miRNA") or "")
        disease = str(row.get("disease") or row.get("disease_name") or "")
        if mirna and disease:
            edges.append((mirna, disease))
    return edges


def export_associations(associations: list[dict[str, Any]], output_path: str | Path) -> Path:
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if output.suffix.lower() == ".json":
        output.write_text(json.dumps(associations, indent=2), encoding="utf-8")
        return output

    if output.suffix.lower() == ".csv":
        if associations:
            fields = sorted({k for row in associations for k in row.keys()})
            with output.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(associations)
        else:
            output.write_text("", encoding="utf-8")
        return output

    raise ValueError("output_path must end with .json or .csv")
