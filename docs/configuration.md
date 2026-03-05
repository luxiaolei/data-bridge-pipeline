# Configuration

Profiles are YAML files validated by `PipelineProfile`.

## Fields

- `source`: source path or remote (e.g. `/data/out` or `r2:bucket/path`)
- `destination`: destination path or remote
- `manifest_path`: local path to manifest JSON
- `state_path`: local path for resume checkpoint JSON
- `queue_path`: local path for queued actions JSON
- `rclone_bin`: optional rclone binary path (default `rclone`)
- `verify_after_copy`: bool, default true
- `delete_after_verify`: bool, default true

## Optional execution fields

- `total_shards`: int >= 1
- `shard_id`: int in [0, total_shards)
- `dry_run`: bool

See `profiles/dev.yaml` and `profiles/prod.yaml`.
