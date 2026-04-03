from mirna_toolkit.alignment.bowtie import align
from mirna_toolkit.disease.hmdd import get_associations
from mirna_toolkit.io.downloaders import download_mirbase_release
from mirna_toolkit.prediction.targetscan_api import get_targets
from mirna_toolkit.utils import http as http_utils


def test_bowtie_align_builds_commands(tmp_path, monkeypatch):
    fastq = tmp_path / "sample.fastq"
    fastq.write_text("@r1\nACGT\n+\n!!!!\n", encoding="utf-8")

    calls = []

    def fake_run(cmd, check):
        calls.append(cmd)
        return None

    monkeypatch.setattr("subprocess.run", fake_run)

    output = align(fastq, reference="mirbase_index", output_bam=tmp_path / "aligned.bam", threads=2)

    assert output == tmp_path / "aligned.bam"
    assert calls[0][0] == "bowtie"
    assert calls[1][0] == "samtools"


def test_download_file_uses_injected_session(tmp_path, monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            return None

        content = b"downloaded-bytes"

    class FakeSession:
        def __init__(self):
            self.closed = False

        def get(self, *args, **kwargs):
            return FakeResponse()

        def close(self):
            self.closed = True

    fake_session = FakeSession()
    monkeypatch.setattr(http_utils, "build_session", lambda: fake_session)

    output = download_mirbase_release("test.fa", output_dir=tmp_path)

    assert output == tmp_path / "test.fa"
    assert output.read_bytes() == b"downloaded-bytes"


def test_http_connectors_parse_mocked_payloads(monkeypatch):
    monkeypatch.setattr(
        "mirna_toolkit.prediction.targetscan_api.safe_get_json",
        lambda *args, **kwargs: {"targets": [{"gene": "GENE1"}]},
    )
    monkeypatch.setattr(
        "mirna_toolkit.disease.hmdd.safe_get_json",
        lambda *args, **kwargs: [{"mirna": "hsa-miR-21", "disease": "Cancer"}],
    )

    targets = get_targets("hsa-miR-21")
    associations = get_associations("hsa-miR-21")

    assert targets == [{"gene": "GENE1"}]
    assert associations == [{"mirna": "hsa-miR-21", "disease": "Cancer"}]
