from app.ingestion.loader import discover_documents


def test_root_level_files_are_not_ingested(tmp_path):
    (tmp_path / "manifest.txt").write_text("not a department document")
    hr = tmp_path / "HR"
    hr.mkdir()
    (hr / "policy.txt").write_text("policy")

    names = [p.name for p in discover_documents(tmp_path)]

    assert names == ["policy.txt"]
