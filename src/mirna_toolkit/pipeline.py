from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import alignment
from .io.fastq import run_fastqc, trim_adapters
from .quantification import counts, normalization


@dataclass
class PipelineConfig:
    fastq_path: str | Path
    reference: str | Path
    annotation: str | Path
    output_dir: str | Path = "outputs"
    aligner: str = "bowtie"
    normalization_method: str = "tpm"
    threads: int = 4
    run_qc: bool = False
    trim: bool = False


@dataclass
class PipelineResult:
    bam_path: Path
    counts_path: Path
    normalized_path: Path
    metadata_path: Path
    counts: dict[str, int]
    normalized: dict[str, float]


def run_end_to_end(
    config: PipelineConfig,
    database_versions: dict[str, str] | None = None,
) -> PipelineResult:
    """Run preprocess -> align -> quantify -> normalize and export run artifacts."""
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    input_fastq = Path(config.fastq_path)

    qc_dir: Path | None = None
    if config.run_qc:
        qc_dir = run_fastqc(input_fastq, output_dir / "qc")

    if config.trim:
        trimmed_fastq = output_dir / f"{input_fastq.stem}.trimmed.fastq"
        input_fastq = trim_adapters(input_fastq, trimmed_fastq, threads=config.threads)

    bam_path = _run_alignment(
        aligner_name=config.aligner,
        fastq_path=input_fastq,
        reference=config.reference,
        output_dir=output_dir,
        threads=config.threads,
    )

    raw_counts = counts.from_bam(bam_path, annotation=config.annotation)
    normalized_counts = _normalize(raw_counts, method=config.normalization_method)

    counts_path = output_dir / "counts.json"
    counts_path.write_text(json.dumps(raw_counts, indent=2), encoding="utf-8")

    normalized_path = output_dir / f"normalized_{config.normalization_method}.json"
    normalized_path.write_text(json.dumps(normalized_counts, indent=2), encoding="utf-8")

    metadata: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "input_fastq": str(config.fastq_path),
        "reference": str(config.reference),
        "annotation": str(config.annotation),
        "aligner": config.aligner,
        "threads": config.threads,
        "normalization": config.normalization_method,
        "run_qc": config.run_qc,
        "trim": config.trim,
        "qc_dir": str(qc_dir) if qc_dir else None,
        "output_dir": str(output_dir),
        "database_versions": database_versions or {},
    }

    metadata_path = output_dir / "run_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    return PipelineResult(
        bam_path=bam_path,
        counts_path=counts_path,
        normalized_path=normalized_path,
        metadata_path=metadata_path,
        counts=raw_counts,
        normalized=normalized_counts,
    )


def _run_alignment(
    aligner_name: str,
    fastq_path: str | Path,
    reference: str | Path,
    output_dir: Path,
    threads: int,
) -> Path:
    output_bam = output_dir / f"aligned.{aligner_name}.bam"
    if aligner_name == "bowtie":
        return alignment.bowtie.align(fastq_path, reference=reference, output_bam=output_bam, threads=threads)
    if aligner_name == "hisat2":
        return alignment.hisat2.align(fastq_path, reference=reference, output_bam=output_bam, threads=threads)
    if aligner_name == "star":
        return alignment.star.align(fastq_path, reference=reference, output_bam=output_bam, threads=threads)
    raise ValueError("aligner must be one of: bowtie, hisat2, star")


def _normalize(raw_counts: dict[str, int], method: str) -> dict[str, float]:
    if method == "tpm":
        return normalization.tpm(raw_counts)
    if method == "rpm":
        return normalization.rpm(raw_counts)
    raise ValueError("normalization_method must be one of: tpm, rpm")
