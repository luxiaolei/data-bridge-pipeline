"""Queue action processor with verify-before-delete semantics."""

from __future__ import annotations

from data_bridge_pipeline.models import QueueAction


class QueueProcessor:
    """Process queued move/delete-after-verify operations."""

    def __init__(self, rclone, delete_after_verify: bool = True) -> None:
        self.rclone = rclone
        self.delete_after_verify = delete_after_verify

    def process(self, actions: list[QueueAction]) -> None:
        for action in actions:
            if action.kind == "move":
                self.rclone.move(action.src, action.dst)
            elif action.kind == "delete_after_verify":
                self.rclone.verify_file(action.src, action.dst)
                if self.delete_after_verify:
                    self.rclone.delete(action.src)
