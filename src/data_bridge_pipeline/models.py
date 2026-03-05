"""Pydantic models for pipeline configuration and manifests."""

from __future__ import annotations

import hashlib
import json
from typing import Literal

from pydantic import BaseModel, Field


class ManifestEntry(BaseModel):
    path: str
    size: int = Field(ge=0)
    sha256: str = Field(min_length=64, max_length=64)
    mtime: str | None = None


class Manifest(BaseModel):
    version: str
    entries: list[ManifestEntry]

    def digest(self) -> str:
        """Stable digest independent of input entry ordering."""
        payload = [e.model_dump() for e in sorted(self.entries, key=lambda x: x.path)]
        raw = json.dumps({"version": self.version, "entries": payload}, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()


class PipelineProfile(BaseModel):
    source: str
    destination: str
    manifest_path: str
    state_path: str = ".pipeline-state.json"
    queue_path: str = ".pipeline-queue.json"
    rclone_bin: str = "rclone"
    verify_after_copy: bool = True
    delete_after_verify: bool = True
    total_shards: int = 1
    shard_id: int = 0
    dry_run: bool = False


class QueueAction(BaseModel):
    kind: Literal["move", "delete_after_verify"]
    src: str
    dst: str


class ReconcileReport(BaseModel):
    missing: list[str]
    stale: list[str]
    orphaned: list[str]
