"""Reconciliation logic for manifest vs actual inventory."""

from __future__ import annotations

from data_bridge_pipeline.models import Manifest, ReconcileReport


def reconcile_manifest(manifest: Manifest, actual_hashes: dict[str, str]) -> ReconcileReport:
    """Compare manifest expectations with actual path->hash mapping."""
    missing: list[str] = []
    stale: list[str] = []

    expected = {e.path: e.sha256 for e in manifest.entries}
    for path, expected_hash in expected.items():
        if path not in actual_hashes:
            missing.append(path)
        elif actual_hashes[path] != expected_hash:
            stale.append(path)

    orphaned = sorted(set(actual_hashes) - set(expected))
    return ReconcileReport(missing=sorted(missing), stale=sorted(stale), orphaned=orphaned)
