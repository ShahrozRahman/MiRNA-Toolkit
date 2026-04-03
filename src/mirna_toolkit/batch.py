from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import pipeline
from .pipeline import PipelineConfig, PipelineResult


@dataclass
class BatchSampleConfig:
    sample_id: str
    fastq_path: str | Path
    reference: str | Path
    annotation: str | Path
    output_dir: str | Path | None = None
    aligner: str = "bowtie"
    normalization_method: str = "tpm"
    threads: int = 4
    run_qc: bool = False
    trim: bool = False


@dataclass
class BatchSampleResult:
    sample_id: str
    bam_path: Path
    counts_path: Path
    normalized_path: Path
    metadata_path: Path
    counts: dict[str, int]
    normalized: dict[str, float]


@dataclass
class BatchRunResult:
    manifest_path: Path
    summary_json_path: Path
    summary_csv_path: Path
    samples: list[BatchSampleResult]


def load_manifest(manifest_path: str | Path) -> list[BatchSampleConfig]:
    path = Path(manifest_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return _load_csv_manifest(path)
    if suffix == ".json":
        return _load_json_manifest(path)
    raise ValueError("manifest_path must end with .csv or .json")


def run_batch_workflow(
    manifest_path: str | Path,
    output_dir: str | Path | None = None,
    database_versions: dict[str, str] | None = None,
) -> BatchRunResult:
    manifest_file = Path(manifest_path)
    base_output_dir = Path(output_dir) if output_dir is not None else manifest_file.parent / "batch_outputs"
    base_output_dir.mkdir(parents=True, exist_ok=True)

    sample_configs = load_manifest(manifest_file)
    sample_results: list[BatchSampleResult] = []

    for sample in sample_configs:
        sample_output_dir = Path(sample.output_dir) if sample.output_dir is not None else base_output_dir / sample.sample_id
        config = PipelineConfig(
            fastq_path=sample.fastq_path,
            reference=sample.reference,
            annotation=sample.annotation,
            output_dir=sample_output_dir,
            aligner=sample.aligner,
            normalization_method=sample.normalization_method,
            threads=sample.threads,
            run_qc=sample.run_qc,
            trim=sample.trim,
        )

        result = pipeline.run_end_to_end(config, database_versions=database_versions)
        sample_results.append(_to_sample_result(sample.sample_id, result))

    summary_json_path = base_output_dir / "batch_summary.json"
    summary_csv_path = base_output_dir / "batch_summary.csv"
    _write_summary(sample_results, summary_json_path, summary_csv_path)

    return BatchRunResult(
        manifest_path=manifest_file,
        summary_json_path=summary_json_path,
        summary_csv_path=summary_csv_path,
        samples=sample_results,
    )


def _load_csv_manifest(path: Path) -> list[BatchSampleConfig]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
    return [_row_to_sample(row, index=index) for index, row in enumerate(rows, start=1)]


def _load_json_manifest(path: Path) -> list[BatchSampleConfig]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        rows = payload.get("samples", [])
    elif isinstance(payload, list):
        rows = payload
    else:
        raise ValueError("JSON manifest must be a list or a dict with a samples key")
    return [_row_to_sample(row, index=index) for index, row in enumerate(rows, start=1)]


def _row_to_sample(row: dict[str, Any], index: int) -> BatchSampleConfig:
    sample_id = str(row.get("sample_id") or row.get("sample") or row.get("id") or f"sample_{index}")
    fastq_path = row.get("fastq_path") or row.get("fastq")
    reference = row.get("reference")
    annotation = row.get("annotation")

    if not fastq_path or not reference or not annotation:
        raise ValueError("Each manifest row must include fastq_path, reference, and annotation")

    return BatchSampleConfig(
        sample_id=sample_id,
        fastq_path=fastq_path,
        reference=reference,
        annotation=annotation,
        output_dir=row.get("output_dir") or None,
        aligner=str(row.get("aligner") or "bowtie"),
        normalization_method=str(row.get("normalization_method") or row.get("normalize") or "tpm"),
        threads=int(row.get("threads") or 4),
        run_qc=_parse_bool(row.get("run_qc") or row.get("qc") or False),
        trim=_parse_bool(row.get("trim") or False),
    )


def _to_sample_result(sample_id: str, result: PipelineResult) -> BatchSampleResult:
    return BatchSampleResult(
        sample_id=sample_id,
        bam_path=result.bam_path,
        counts_path=result.counts_path,
        normalized_path=result.normalized_path,
        metadata_path=result.metadata_path,
        counts=result.counts,
        normalized=result.normalized,
    )


def _write_summary(samples: list[BatchSampleResult], json_path: Path, csv_path: Path) -> None:
    summary_rows = [
        {
            "sample_id": sample.sample_id,
            "bam_path": str(sample.bam_path),
            "counts_path": str(sample.counts_path),
            "normalized_path": str(sample.normalized_path),
            "metadata_path": str(sample.metadata_path),
        }
        for sample in samples
    ]

    json_path.write_text(json.dumps(summary_rows, indent=2), encoding="utf-8")

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["sample_id", "bam_path", "counts_path", "normalized_path", "metadata_path"])
        writer.writeheader()
        writer.writerows(summary_rows)


def _parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return value != 0

    normalized = str(value).strip().lower()
    return normalized in {"1", "true", "yes", "y", "on"}