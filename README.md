# data-bridge-pipeline

EN | 中文

A production-ready, manifest-driven data bridge for large datasets:
**VPS ingest/stage → Cloudflare R2 queue → Mac archive pull**.

一个面向大数据集的、可生产使用的数据桥接管道：
**VPS 下载/暂存 → Cloudflare R2 中转队列 → Mac 本地归档拉取**。

---

## Why this project / 解决了什么痛点

### EN
- VPS disk is small: store temporarily, upload quickly, delete locally.
- Source network is better on VPS than on local machine.
- Local machine (Mac) can pull reliably from R2, then archive on external disk.
- Need replayable, auditable data lifecycle across three locations.

### 中文
- VPS 磁盘小：只能临时落盘，上传后要及时清理。
- 数据源在 VPS 网络更好，本地（如北京）直连下载不稳定。
- 本地 Mac 可稳定从 R2 拉取并落地到外置硬盘。
- 需要三端（VPS / R2 / Mac）可审计、可回放的数据生命周期。

---

## Core features / 核心能力

- Manifest-first, idempotent transfers / 清单驱动、幂等传输
- Resume from checkpoint / 断点续传
- Reconcile across VPS, R2, Mac / 三端对账
- Queue drain with verify-before-delete / 校验后删除（防误删）
- Sharding support / 分片并行
- CLI: `run`, `push`, `pull`, `reconcile`, `gc`, `doctor`

---

## Quick start / 快速开始

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .[dev]

make lint
make test

# one run with a profile
python -m data_bridge_pipeline.cli run --profile profiles/dev.yaml
```

---

## Typical architecture / 典型架构

1. VPS creates raw files + manifest.
2. VPS pushes files to `r2://.../queue/...`.
3. Mac runs pull script (`rclone move`) to archive path.
4. Queue objects are removed only after transfer verification.

1. VPS 生成原始文件与 manifest。
2. VPS 推送到 `r2://.../queue/...`。
3. Mac 执行拉取脚本（`rclone move`）归档到本地。
4. 校验通过后再删除队列对象。

---

## Rithmic raw example / Rithmic 原始流示例

- VPS profile: `profiles/vps_rithmic.yaml`
- VPS script: `scripts/vps_rithmic_run.sh`
- Mac destination (example): `/Volumes/extdisk/data-bridge-pipeline`

---

## Security notes / 安全说明

- Never commit real credentials.
- Put secrets in local env files (`~/.r2_env`) or secret manager.
- Use least-privilege API keys for R2.

- 不要把真实密钥提交到仓库。
- 使用本地环境文件（如 `~/.r2_env`）或密钥管理系统。
- R2 使用最小权限密钥。

---

## Docs / 文档

- `docs/architecture.md`
- `docs/configuration.md`
- `docs/reconcile.md`
- `docs/security.md`
- `docs/cli.md`
- `docs/manifest.schema.json`

---

## License

MIT
