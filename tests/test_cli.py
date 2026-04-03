import json

from mirna_toolkit.batch import BatchRunResult, BatchSampleResult
from mirna_toolkit.cli import main


def test_cli_help_subcommand_shows_examples(capsys):
    exit_code = main(["help"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "mirna-toolkit help run" in captured.out
    assert "batch" in captured.out


def test_cli_batch_subcommand_uses_manifest(tmp_path, monkeypatch, capsys):
    manifest = tmp_path / "samples.json"
    manifest.write_text(
        json.dumps(
            [
                {
                    "sample_id": "s1",
                    "fastq_path": "sample.fastq",
                    "reference": "mirbase.fa",
                    "annotation": "mirbase.gtf",
                }
            ]
        ),
        encoding="utf-8",
    )

    sample_result = BatchSampleResult(
        sample_id="s1",
        bam_path=tmp_path / "aligned.bam",
        counts_path=tmp_path / "counts.json",
        normalized_path=tmp_path / "normalized.json",
        metadata_path=tmp_path / "metadata.json",
        counts={"hsa-miR-21": 10},
        normalized={"hsa-miR-21": 1.0},
    )
    result = BatchRunResult(
        manifest_path=manifest,
        summary_json_path=tmp_path / "batch_summary.json",
        summary_csv_path=tmp_path / "batch_summary.csv",
        samples=[sample_result],
    )

    monkeypatch.setattr("mirna_toolkit.batch.run_batch_workflow", lambda *args, **kwargs: result)

    exit_code = main(["batch", "--manifest", str(manifest), "--output-dir", str(tmp_path / "batch_out")])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert str(result.summary_json_path) in captured.out
