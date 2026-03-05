# data-bridge-pipeline

A production-ready, open-source data bridge for moving and reconciling file-based datasets across local storage and S3-compatible object stores (for example Cloudflare R2) via `rclone`.

## Highlights

- **Reliable transfer pipeline** with resumable execution state
- **Manifest-first design** for idempotent, deterministic behavior
- **Reconcile engine** to detect missing, stale, and orphaned objects
- **Queue actions** with verify-before-delete safety model
- **Shard assignment** for horizontal scaling
- **Operational CLI**: `run`, `push`, `pull`, `reconcile`, `gc`, `doctor`

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp profiles/dev.yaml .env.profile.yaml

# sanity checks
make lint
make test

# run a single pipeline pass
python -m data_bridge_pipeline.cli run --profile .env.profile.yaml
```

## Project layout

- `src/data_bridge_pipeline/` — implementation
- `tests/` — unit tests for correctness and safety behavior
- `docs/` — architecture, config, reconcile behavior, security, CLI docs
- `profiles/` — example profiles
- `scripts/` — deployment helper scripts

## Safety model

Destructive operations (move/delete) are gated by verification. Queue deletion requires source+destination verification before remove.

## License

MIT (add your preferred LICENSE file if needed).
