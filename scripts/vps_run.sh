#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python -m data_bridge_pipeline.cli doctor --profile profiles/prod.yaml
python -m data_bridge_pipeline.cli run --profile profiles/prod.yaml
