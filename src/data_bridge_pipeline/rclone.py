"""Thin wrapper around rclone CLI for object operations."""

from __future__ import annotations

import json
import subprocess
import time


class RcloneClient:
    """Executes rclone commands with retries and file-level verification."""

    def __init__(
        self,
        binary: str = "rclone",
        dry_run: bool = False,
        retries: int = 3,
        retry_sleep_seconds: float = 1.0,
    ) -> None:
        self.binary = binary
        self.dry_run = dry_run
        self.retries = retries
        self.retry_sleep_seconds = retry_sleep_seconds

    def _run(self, args: list[str]) -> None:
        if self.dry_run:
            return

        last_err: subprocess.CalledProcessError | None = None
        for attempt in range(1, self.retries + 1):
            try:
                subprocess.run([self.binary, *args], check=True)
                return
            except subprocess.CalledProcessError as err:
                last_err = err
                if attempt < self.retries:
                    time.sleep(self.retry_sleep_seconds * attempt)
        if last_err is not None:
            raise last_err

    def _run_json(self, args: list[str]) -> list[dict]:
        if self.dry_run:
            return []
        out = subprocess.check_output([self.binary, *args], text=True)
        return json.loads(out)

    def copyto(self, src: str, dst: str) -> None:
        self._run(["copyto", src, dst])

    def move(self, src: str, dst: str) -> None:
        self._run(["moveto", src, dst])

    def delete(self, target: str) -> None:
        self._run(["delete", target])

    def check(self, src: str, dst: str) -> None:
        self._run(["check", src, dst])

    def verify_file(self, src: str, dst: str) -> None:
        """Verify file-level copy by comparing size from lsjson metadata."""
        if self.dry_run:
            return
        src_meta = self._run_json(["lsjson", src])
        dst_meta = self._run_json(["lsjson", dst])
        if len(src_meta) != 1 or len(dst_meta) != 1:
            raise RuntimeError(f"verify_file expected exactly one object for src={src} dst={dst}")
        if int(src_meta[0].get("Size", -1)) != int(dst_meta[0].get("Size", -2)):
            raise RuntimeError(f"size mismatch for src={src} dst={dst}")
