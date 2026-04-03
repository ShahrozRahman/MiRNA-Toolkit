from pathlib import Path


def discover_novel_mirnas(collapsed_reads_fasta: str | Path, min_count: int = 10) -> list[dict[str, str | int]]:
    """Heuristic novel miRNA candidate discovery from collapsed FASTA reads.

    Input format expects headers like: >read_id_x25
    """
    candidates: list[dict[str, str | int]] = []
    path = Path(collapsed_reads_fasta)

    current_header = ""
    current_seq = ""

    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(">"):
            if current_header and current_seq:
                count = _extract_count(current_header)
                if count >= min_count and 18 <= len(current_seq) <= 26:
                    candidates.append({"id": current_header[1:], "sequence": current_seq, "read_count": count})
            current_header = line
            current_seq = ""
        else:
            current_seq += line.strip().upper()

    if current_header and current_seq:
        count = _extract_count(current_header)
        if count >= min_count and 18 <= len(current_seq) <= 26:
            candidates.append({"id": current_header[1:], "sequence": current_seq, "read_count": count})

    return candidates


def _extract_count(header: str) -> int:
    if "_x" in header:
        try:
            return int(header.rsplit("_x", 1)[1])
        except ValueError:
            return 1
    return 1
