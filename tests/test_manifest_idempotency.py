from data_bridge_pipeline.models import Manifest, ManifestEntry


def test_manifest_digest_idempotent() -> None:
    entries = [
        ManifestEntry(path="b/file2", size=2, sha256="b" * 64),
        ManifestEntry(path="a/file1", size=1, sha256="a" * 64),
    ]
    m1 = Manifest(version="1", entries=entries)
    m2 = Manifest(version="1", entries=list(reversed(entries)))

    assert m1.digest() == m2.digest()
