from data_bridge_pipeline.models import QueueAction
from data_bridge_pipeline.queue import QueueProcessor


class MockRclone:
    def __init__(self) -> None:
        self.moves: list[tuple[str, str]] = []
        self.deletes: list[str] = []
        self.checked: list[tuple[str, str]] = []

    def move(self, src: str, dst: str) -> None:
        self.moves.append((src, dst))

    def delete(self, target: str) -> None:
        self.deletes.append(target)

    def verify_file(self, src: str, dst: str) -> None:
        self.checked.append((src, dst))


def test_queue_move_and_delete_after_verify() -> None:
    r = MockRclone()
    qp = QueueProcessor(rclone=r, delete_after_verify=True)

    actions = [
        QueueAction(kind="move", src="a", dst="b"),
        QueueAction(kind="delete_after_verify", src="b", dst="archive/b"),
    ]
    qp.process(actions)

    assert r.moves == [("a", "b")]
    assert r.checked == [("b", "archive/b")]
    assert r.deletes == ["b"]
