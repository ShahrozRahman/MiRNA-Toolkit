from __future__ import annotations

from collections import Counter
from pathlib import Path


def from_bam(bam_path: str | Path, annotation: str | Path | None = None) -> dict[str, int]:
    """Count read alignments by reference name from a BAM file."""
    try:
        import pysam  # type: ignore
    except ImportError as exc:
        raise ImportError("pysam is required for BAM quantification. Install with: pip install mirna-toolkit[full]") from exc

    counts: Counter[str] = Counter()
    with pysam.AlignmentFile(str(bam_path), "rb") as bam:
        for read in bam.fetch(until_eof=True):
            if read.is_unmapped:
                continue
            ref_name = bam.get_reference_name(read.reference_id)
            counts[ref_name] += 1
    return dict(counts)
