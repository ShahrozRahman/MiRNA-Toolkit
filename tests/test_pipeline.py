import json

from mirna_toolkit.pipeline import PipelineConfig, run_end_to_end


def test_pipeline_exports_artifacts(monkeypatch, tmp_path):
    fastq = tmp_path / "sample.fastq"
    fastq.write_text("@r1\nACGT\n+\n!!!!\n", encoding="utf-8")

    def fake_align(*args, **kwargs):
        bam = tmp_path / "aligned.bam"
        bam.write_text("bam", encoding="utf-8")
        return bam

    def fake_from_bam(*args, **kwargs):
        return {"hsa-miR-21": 100, "hsa-miR-16": 50}

    monkeypatch.setattr("mirna_toolkit.alignment.bowtie.align", fake_align)
    monkeypatch.setattr("mirna_toolkit.quantification.counts.from_bam", fake_from_bam)

    config = PipelineConfig(
        fastq_path=fastq,
        reference="dummy_ref",
        annotation="dummy_annot",
        output_dir=tmp_path,
        aligner="bowtie",
        normalization_method="rpm",
    )

    result = run_end_to_end(config, database_versions={"miRBase": "22.1"})

    assert result.bam_path.exists()
    assert result.counts_path.exists()
    assert result.normalized_path.exists()
    assert result.metadata_path.exists()

    metadata = json.loads(result.metadata_path.read_text(encoding="utf-8"))
    assert metadata["aligner"] == "bowtie"
    assert metadata["database_versions"]["miRBase"] == "22.1"
