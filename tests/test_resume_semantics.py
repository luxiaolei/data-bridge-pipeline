from pathlib import Path

from data_bridge_pipeline.models import Manifest, ManifestEntry, PipelineProfile
from data_bridge_pipeline.pipeline import PipelineRunner


class DummyRclone:
    def __init__(self) -> None:
        self.copied: list[tuple[str, str]] = []

    def copyto(self, src: str, dst: str) -> None:
        self.copied.append((src, dst))

    def check(self, src: str, dst: str) -> None:
        return None


def test_resume_skips_processed_entries(tmp_path: Path) -> None:
    state = tmp_path / "state.json"
    profile = PipelineProfile(
        source="src",
        destination="dst",
        manifest_path="manifest.json",
        state_path=str(state),
    )
    manifest = Manifest(
        version="1",
        entries=[
            ManifestEntry(path="a", size=1, sha256="a" * 64),
            ManifestEntry(path="b", size=1, sha256="b" * 64),
        ],
    )
    state.write_text('{"last_index": 0}', encoding="utf-8")
    rclone = DummyRclone()
    runner = PipelineRunner(profile, rclone)

    runner.push(manifest)

    assert rclone.copied == [("src/b", "dst/b")]
