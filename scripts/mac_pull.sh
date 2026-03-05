#!/usr/bin/env bash
set -euo pipefail

# Pull queue objects from R2 to local ext disk archive on Mac mini.
# This wrapper keeps parity with /Volumes/extdisk/massive/auto_pull.sh defaults.
rclone move \
  r2_down:ny-data-transfer/data-bridge-pipeline/queue \
  /Volumes/extdisk/data-bridge-pipeline \
  --transfers=8 \
  --min-age=10s
