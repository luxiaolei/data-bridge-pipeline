"""Pipeline execution and resume semantics."""

from __future__ import annotations

import json
from pathlib import Path

from data_bridge_pipeline.models import Manifest, PipelineProfile


class PipelineRunner:
    """Runs push/pull pipeline with resume checkpointing."""

    def __init__(self, profile: PipelineProfile, rclone) -> None:
        self.profile = profile
        self.rclone = rclone
        self.state_file = Path(profile.state_path)

    def _load_last_index(self) -> int:
        if not self.state_file.exists():
            return -1
        data = json.loads(self.state_file.read_text(encoding="utf-8"))
        return int(data.get("last_index", -1))

    def _save_last_index(self, idx: int) -> None:
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state_file.write_text(json.dumps({"last_index": idx}), encoding="utf-8")

    def push(self, manifest: Manifest) -> None:
        start = self._load_last_index() + 1
        for idx, entry in enumerate(manifest.entries):
            if idx < start:
                continue
            src = f"{self.profile.source}/{entry.path}"
            dst = f"{self.profile.destination}/{entry.path}"
            self.rclone.copyto(src, dst)
            if self.profile.verify_after_copy:
                self.rclone.check(src, dst)
            self._save_last_index(idx)

    def pull(self, manifest: Manifest) -> None:
        start = self._load_last_index() + 1
        for idx, entry in enumerate(manifest.entries):
            if idx < start:
                continue
            src = f"{self.profile.destination}/{entry.path}"
            dst = f"{self.profile.source}/{entry.path}"
            self.rclone.copyto(src, dst)
            if self.profile.verify_after_copy:
                self.rclone.check(src, dst)
            self._save_last_index(idx)
