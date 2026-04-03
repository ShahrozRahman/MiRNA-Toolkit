from mirna_toolkit.utils.versioning import DatabaseVersion, DatabaseVersionTracker


def test_version_tracker_adds_entry(tmp_path):
    tracker = DatabaseVersionTracker()
    tracker.add(DatabaseVersion(name="miRBase", version="22.1", retrieved_at="2026-04-03", source_url="https://mirbase.org"))

    out_file = tmp_path / "versions.json"
    tracker.export_json(out_file)

    assert out_file.exists()
    assert "miRBase" in out_file.read_text(encoding="utf-8")
