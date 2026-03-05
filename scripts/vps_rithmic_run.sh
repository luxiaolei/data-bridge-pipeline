#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
python -m data_bridge_pipeline.cli doctor --profile profiles/vps_rithmic.yaml
python -m data_bridge_pipeline.cli push --profile profiles/vps_rithmic.yaml
