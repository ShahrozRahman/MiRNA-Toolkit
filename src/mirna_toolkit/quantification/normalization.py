from __future__ import annotations

import numpy as np


def rpm(counts: dict[str, int]) -> dict[str, float]:
    total = float(sum(counts.values()))
    if total == 0:
        return {k: 0.0 for k in counts}
    return {k: (v * 1_000_000.0) / total for k, v in counts.items()}


def tpm(counts: dict[str, int], lengths: dict[str, int] | None = None) -> dict[str, float]:
    if lengths is None:
        lengths = {k: 22 for k in counts}  # Typical mature miRNA length fallback.
    rpk = {k: counts[k] / max(lengths.get(k, 22), 1) for k in counts}
    scale = sum(rpk.values()) / 1_000_000.0
    if scale == 0:
        return {k: 0.0 for k in counts}
    return {k: v / scale for k, v in rpk.items()}


def deseq2_style_normalization(sample_counts: list[dict[str, int]]) -> list[dict[str, float]]:
    """Approximate DESeq2 median-of-ratios normalization."""
    if not sample_counts:
        return []

    features = sorted({f for sample in sample_counts for f in sample.keys()})
    matrix = np.array([[sample.get(f, 0) for f in features] for sample in sample_counts], dtype=float)
    matrix[matrix == 0] = np.nan

    geometric_means = np.exp(np.nanmean(np.log(matrix), axis=0))
    geometric_means[np.isnan(geometric_means)] = 1.0

    size_factors = []
    for row in matrix:
        ratios = row / geometric_means
        ratios = ratios[~np.isnan(ratios)]
        size_factors.append(float(np.median(ratios)) if ratios.size else 1.0)

    normalized = []
    for row, sf in zip(matrix, size_factors):
        normalized.append({f: float(v / max(sf, 1e-9)) for f, v in zip(features, row)})
    return normalized
