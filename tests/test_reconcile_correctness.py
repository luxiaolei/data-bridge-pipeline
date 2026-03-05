from data_bridge_pipeline.models import Manifest, ManifestEntry
from data_bridge_pipeline.reconcile import reconcile_manifest


def test_reconcile_detects_missing_stale_orphaned() -> None:
    manifest = Manifest(
        version="1",
        entries=[
            ManifestEntry(path="a", size=1, sha256="a" * 64),
            ManifestEntry(path="b", size=2, sha256="b" * 64),
        ],
    )
    actual = {
        "a": "a" * 64,
        "b": "c" * 64,
        "x": "x" * 64,
    }
    report = reconcile_manifest(manifest, actual)

    assert report.missing == []
    assert report.stale == ["b"]
    assert report.orphaned == ["x"]
