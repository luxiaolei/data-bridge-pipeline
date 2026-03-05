"""Shard assignment helpers."""

from __future__ import annotations

import hashlib
from typing import Iterable


def assign_shard(path: str, total_shards: int) -> int:
    """Assign a path to shard index deterministically."""
    h = hashlib.sha256(path.encode("utf-8")).hexdigest()
    return int(h[:16], 16) % total_shards


def shard_filter(paths: Iterable[str], shard_id: int, total_shards: int) -> list[str]:
    """Filter path collection to entries belonging to a shard."""
    return [p for p in paths if assign_shard(p, total_shards) == shard_id]
