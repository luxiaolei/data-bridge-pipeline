#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python -m data_bridge_pipeline.cli doctor --profile profiles/dev.yaml
python -m data_bridge_pipeline.cli pull --profile profiles/dev.yaml
