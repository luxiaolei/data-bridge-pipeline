# Reconcile

Reconcile compares expected manifest entries and actual destination inventory.

## Outputs

- `missing`: expected objects not found at destination
- `stale`: destination object hash differs from manifest
- `orphaned`: destination objects not present in manifest

## Correctness goal

For a healthy sync state:

- `missing == []`
- `stale == []`
- `orphaned` is optional depending on retention policy

## Command

```bash
python -m data_bridge_pipeline.cli reconcile --manifest manifest.json --actual actual.json
```
