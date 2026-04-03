from typing import Any

from ..utils.http import safe_get_json

MIRECORDS_ENDPOINT = "https://c1.accurascience.com/miRecords/api/targets"


def get_targets(mirna_id: str, timeout: int = 60, strict: bool = False) -> list[dict[str, Any]]:
    payload = safe_get_json(
        MIRECORDS_ENDPOINT,
        params={"mirna": mirna_id},
        timeout=timeout,
        strict=strict,
    )
    if payload is None:
        return []
    if isinstance(payload, dict) and "results" in payload:
        return list(payload["results"])
    if isinstance(payload, list):
        return payload
    return []
