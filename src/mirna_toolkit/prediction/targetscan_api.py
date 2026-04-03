from typing import Any

from ..utils.http import safe_get_json

TARGETSCAN_ENDPOINT = "https://www.targetscan.org/cgi-bin/targetscan/vert_80/targetscan.cgi"


def get_targets(
    mirna_id: str,
    species: str = "Human",
    timeout: int = 60,
    strict: bool = False,
) -> list[dict[str, Any]]:
    """Retrieve target predictions from TargetScan-style endpoint.

    This wrapper returns structured records when upstream service responds with JSON.
    """
    params = {"mirg": mirna_id, "species": species, "format": "json"}
    data = safe_get_json(TARGETSCAN_ENDPOINT, params=params, timeout=timeout, strict=strict)
    if data is None:
        return []

    if isinstance(data, dict) and "targets" in data:
        return list(data["targets"])
    if isinstance(data, list):
        return data
    return []
