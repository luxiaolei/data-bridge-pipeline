# Architecture

## Overview

`data-bridge-pipeline` uses a manifest-driven, resumable pipeline with clear control points:

1. Build/load manifest
2. Select shard slice (optional)
3. Execute transfer stage (`push`/`pull`)
4. Execute queue actions (move/delete-after-verify)
5. Persist checkpoint for resume

## Components

- **CLI (`cli.py`)**: Typer entrypoint and command orchestration
- **Models (`models.py`)**: Pydantic schemas for config, manifests, reconcile reports, queue actions
- **Rclone wrapper (`rclone.py`)**: shell-safe subprocess wrapper for copy/move/delete/check
- **Pipeline (`pipeline.py`)**: resumable execution and transfer orchestration
- **Reconcile (`reconcile.py`)**: compares expected state (manifest) against actual state
- **Sharding (`sharding.py`)**: deterministic shard assignment via hash(path)

## Data flow

```text
Manifest -> Filter by shard -> Transfer -> Verify -> Queue move/delete -> State checkpoint
```

## Reliability patterns

- idempotent manifest digest
- checkpoint file written each successful item
- verify-before-delete queue semantics
- rclone command execution with strict error propagation

## Scale model

Shard workers can run in parallel by assigning `--shard-id` and `--total-shards`.
