from data_bridge_pipeline.sharding import assign_shard, shard_filter


def test_assign_shard_stable() -> None:
    p = "some/path/file.parquet"
    assert assign_shard(p, total_shards=8) == assign_shard(p, total_shards=8)


def test_shard_filter_only_target() -> None:
    paths = [f"p{i}" for i in range(30)]
    selected = shard_filter(paths, shard_id=1, total_shards=3)
    assert all(assign_shard(p, 3) == 1 for p in selected)
