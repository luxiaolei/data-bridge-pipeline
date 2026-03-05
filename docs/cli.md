# CLI

## Commands

- `run --profile PATH`: execute full pipeline pass with resume
- `push --profile PATH`: copy source -> destination by manifest
- `pull --profile PATH`: copy destination -> source by manifest
- `reconcile --manifest PATH --actual PATH`: compute drift report
- `gc --profile PATH`: process queue actions (move/delete-after-verify)
- `doctor --profile PATH`: validate profile, paths, and tooling

## Exit codes

- `0`: success
- non-zero: validation or execution failure
