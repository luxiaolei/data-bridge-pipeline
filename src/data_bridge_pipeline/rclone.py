"""Thin wrapper around rclone CLI for object operations."""

from __future__ import annotations

import subprocess


class RcloneClient:
    """Executes rclone commands with strict failure behavior."""

    def __init__(self, binary: str = "rclone", dry_run: bool = False) -> None:
        self.binary = binary
        self.dry_run = dry_run

    def _run(self, args: list[str]) -> None:
        if self.dry_run:
            return
        subprocess.run([self.binary, *args], check=True)

    def copyto(self, src: str, dst: str) -> None:
        self._run(["copyto", src, dst])

    def move(self, src: str, dst: str) -> None:
        self._run(["moveto", src, dst])

    def delete(self, target: str) -> None:
        self._run(["delete", target])

    def check(self, src: str, dst: str) -> None:
        self._run(["check", src, dst])
