#!/usr/bin/env bash
set -euo pipefail
ROOT="/home/trader/MyRepos/data-bridge-pipeline"
cd "$ROOT"
mkdir -p runtime/reports

TS="$(date +%Y%m%d_%H%M%S)"
OUT="runtime/reports/reconcile_vps_r2_${TS}.md"

LOCAL_COUNT=$(find runtime/vps_out/rithmic_raw -type f 2>/dev/null | wc -l | tr -d ' ')
R2_COUNT=$(rclone lsf r2_down:ny-data-transfer/data-bridge-pipeline/queue/rithmic_raw --recursive 2>/dev/null | wc -l | tr -d ' ')

cat > "$OUT" <<EOF
# Reconcile report (VPS vs R2 queue)

- time: $(date -Iseconds)
- local_files: ${LOCAL_COUNT}
- r2_queue_files: ${R2_COUNT}
- note: full 3-way reconcile requires Mac local file count (generated on Mac side).
EOF

echo "$OUT"
