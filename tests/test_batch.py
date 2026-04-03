import csv
import json

from mirna_toolkit.batch import run_batch_workflow
from mirna_toolkit.pipeline import PipelineResult


def test_batch_workflow_runs_manifest(tmp_path, monkeypatch):
    manifest = tmp_path / "samples.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sample_id", "fastq_path", "reference", "annotation", "run_qc", "trim"],
        )
        writer.writeheader()
        writer.writerow(
            {
                "sample_id": "s1",
                "fastq_path": str(tmp_path / "s1.fastq"),
                "reference": "mirbase.fa",
                "annotation": "mirbase.gtf",
                "run_qc": "true",
                "trim": "false",
            }
        )

    (tmp_path / "s1.fastq").write_text("@r1\nACGT\n+\n!!!!\n", encoding="utf-8")

    def fake_run_end_to_end(config, database_versions=None):
        out_dir = tmp_path / "run_output"
        out_dir.mkdir(parents=True, exist_ok=True)
        bam_path = out_dir / "aligned.bam"
        counts_path = out_dir / "counts.json"
        normalized_path = out_dir / "normalized_tpm.json"
        metadata_path = out_dir / "run_metadata.json"
        bam_path.write_text("bam", encoding="utf-8")
        counts_path.write_text(json.dumps({"hsa-miR-21": 10}), encoding="utf-8")
        normalized_path.write_text(json.dumps({"hsa-miR-21": 1.0}), encoding="utf-8")
        metadata_path.write_text(json.dumps({"aligner": config.aligner}), encoding="utf-8")
        return PipelineResult(
            bam_path=bam_path,
            counts_path=counts_path,
            normalized_path=normalized_path,
            metadata_path=metadata_path,
            counts={"hsa-miR-21": 10},
            normalized={"hsa-miR-21": 1.0},
        )

    monkeypatch.setattr("mirna_toolkit.pipeline.run_end_to_end", fake_run_end_to_end)

    result = run_batch_workflow(manifest, output_dir=tmp_path / "batch_out", database_versions={"miRBase": "22.1"})

    assert result.summary_json_path.exists()
    assert result.summary_csv_path.exists()
    assert len(result.samples) == 1
    assert result.samples[0].sample_id == "s1"

    summary = json.loads(result.summary_json_path.read_text(encoding="utf-8"))
    assert summary[0]["sample_id"] == "s1"
    assert summary[0]["bam_path"].endswith("aligned.bam")
