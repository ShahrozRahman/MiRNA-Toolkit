from typing import Any

from ..utils.http import safe_get_json

MIRCANCER_ENDPOINT = "https://mircancer.ecu.edu/api/v1/associations"


def get_associations(mirna_id: str, timeout: int = 60, strict: bool = False) -> list[dict[str, Any]]:
    payload = safe_get_json(
        MIRCANCER_ENDPOINT,
        params={"mirna": mirna_id},
        timeout=timeout,
        strict=strict,
    )
    if payload is None:
        return []
    if isinstance(payload, dict) and "data" in payload:
        return list(payload["data"])
    if isinstance(payload, list):
        return payload
    return []
