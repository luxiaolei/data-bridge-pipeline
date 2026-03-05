#!/usr/bin/env bash
set -euo pipefail

ROOT="/home/trader/MyRepos/data-bridge-pipeline"
API_URL="http://127.0.0.1:8090/v1/market/orderflow?symbol=XAUUSD&use_rithmic=true&include_chart=false"

cd "$ROOT"
mkdir -p runtime/vps_out/rithmic_raw runtime/manifests runtime/state runtime/reports

# 1) Capture one snapshot file (JSONL with multiple samples for robustness)
python3 - <<'PY'
import json, time, hashlib
from pathlib import Path
from urllib.request import urlopen

root=Path('/home/trader/MyRepos/data-bridge-pipeline')
api='http://127.0.0.1:8090/v1/market/orderflow?symbol=XAUUSD&use_rithmic=true&include_chart=false'

date=time.strftime('%Y-%m-%d')
hour=time.strftime('%H')
out_dir=root/'runtime'/'vps_out'/'rithmic_raw'/f'date={date}'/f'hour={hour}'
out_dir.mkdir(parents=True, exist_ok=True)
fn=out_dir/f"orderflow_{time.strftime('%Y%m%d_%H%M%S')}.jsonl"
rows=[]
for _ in range(12):
    with urlopen(api, timeout=2) as r:
        d=json.loads(r.read().decode())
    d['_capture_ts']=time.time()
    rows.append(d)
    time.sleep(0.25)
with fn.open('w', encoding='utf-8') as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False)+'\n')

# Ensure dataset description exists
meta = root/'runtime'/'vps_out'/'rithmic_raw'/'DATASET_DESCRIPTION.md'
if not meta.exists():
    meta.write_text('# rithmic_raw\n\nSee repo docs for schema and lifecycle.\n', encoding='utf-8')

# Build manifest for current capture + dataset description
base=root/'runtime'/'vps_out'
entries=[]
for f in [meta, fn]:
    raw=f.read_bytes()
    entries.append({
      'path': str(f.relative_to(base)).replace('\\','/'),
      'size': f.stat().st_size,
      'sha256': hashlib.sha256(raw).hexdigest(),
      'mtime': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(f.stat().st_mtime)),
    })
manifest={'version':'1.0','entries':entries}
(root/'runtime'/'manifests'/'rithmic_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(fn)
PY

# 2) Reset state so push uploads current manifest entries every run
rm -f runtime/state/vps_rithmic_state.json

# 3) Push to R2 queue
.venv/bin/data-bridge-pipeline push --profile profiles/vps_rithmic.yaml
