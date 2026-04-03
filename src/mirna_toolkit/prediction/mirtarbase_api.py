from typing import Any

from ..utils.http import safe_get_json

MIRTARBASE_ENDPOINT = "https://mirtarbase.cuhk.edu.cn/~miRTarBase/api/interactions"


def get_validated_targets(mirna_id: str, timeout: int = 60, strict: bool = False) -> list[dict[str, Any]]:
    payload = safe_get_json(
        MIRTARBASE_ENDPOINT,
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
