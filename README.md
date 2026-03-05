# data-bridge-pipeline

[EN](#english) | [中文](#中文)

---

## English

### 1) What this project solves

`data-bridge-pipeline` is a production-oriented transfer framework for large market datasets when:

- Your **VPS has strong upstream connectivity** (fast provider download) but **limited disk**.
- Your **local archive node** (for example Mac mini + external SSD) has poor direct connectivity to source providers.
- You need a reliable middle layer with explicit lifecycle and auditability.

The pipeline standardizes:

`VPS ingest/stage -> Cloudflare R2 queue -> Mac archive pull`

with verification, resumability, and reconciliation.

### 2) Key capabilities

- **Manifest-driven transfer** (idempotent and deterministic)
- **Resume from checkpoint** (interrupted jobs continue safely)
- **Queue model with verify-before-delete**
- **Three-side reconciliation hooks** (VPS / R2 / Mac)
- **Plugin-style architecture** for data sources and sinks
- **Operational CLI** (`run`, `push`, `pull`, `reconcile`, `gc`, `doctor`)

### 3) Typical use case

- Data source: Massive / Rithmic raw snapshots / any file source
- VPS: fetch/convert and stage temporary files
- R2: act as transfer queue and durability buffer
- Mac: drain queue to local archive path, then queue clears via move semantics

### 4) Repository structure

```text
src/data_bridge_pipeline/    # core package
docs/                        # architecture + operations docs
profiles/                    # profile examples
scripts/                     # operator scripts for VPS/Mac
tests/                       # safety and correctness tests
```

### 5) Quick start

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'

make lint
make test

python -m data_bridge_pipeline.cli doctor --profile profiles/dev.yaml
python -m data_bridge_pipeline.cli run --profile profiles/dev.yaml
```

### 6) Rithmic raw flow (current operational path)

- VPS profile: `profiles/vps_rithmic.yaml`
- VPS runner: `scripts/vps_capture_push.sh`
- Mac archive target: `/Volumes/extdisk/data-bridge-pipeline`
- Dataset description included at dataset root:
  - `rithmic_raw/DATASET_DESCRIPTION.md`

### 7) Security and reliability notes

- Never commit real credentials (R2 keys, provider tokens).
- Use least-privilege storage keys.
- Keep queue prefix isolated per dataset to avoid accidental cross-drain.
- Run periodic reconcile reports and retain operation logs.

### 8) CI and quality gates

- Lint: Ruff
- Tests: Pytest
- Formatting: Black
- CI: GitHub Actions (`.github/workflows/ci.yml`)

### 9) Roadmap

- Full 3-way reconcile command (VPS+R2+Mac in one report)
- Optional parquet conversion worker
- Optional web status panel

---

## 中文

### 1）这个项目解决什么问题

`data-bridge-pipeline` 是一个面向生产的“大数据文件中转”框架，适用于：

- **VPS 上游网络好**（下载源数据快），但 **本地磁盘小**；
- **本地归档机器**（例如 Mac mini + 外置硬盘）直连数据源不稳定；
- 需要可追踪、可恢复、可对账的数据生命周期。

标准链路：

`VPS 下载/暂存 -> Cloudflare R2 队列中转 -> Mac 归档拉取`

并提供校验、断点恢复、对账能力。

### 2）核心能力

- **Manifest 清单驱动**（幂等、可重复）
- **断点续传**（任务中断后安全继续）
- **校验后删除** 的队列模型
- **三端对账能力**（VPS / R2 / Mac）
- 可扩展的数据源/存储插件架构
- 命令行工具：`run/push/pull/reconcile/gc/doctor`

### 3）典型场景

- 数据源：Massive / Rithmic 原始快照 / 任意文件源
- VPS：抓取/转换并临时落盘
- R2：做中转队列与缓冲
- Mac：定时拉取到本地归档目录，使用 move 语义自动清空队列

### 4）目录结构

```text
src/data_bridge_pipeline/    # 核心代码
docs/                        # 架构与运维文档
profiles/                    # 配置样例
scripts/                     # VPS/Mac 运维脚本
tests/                       # 安全与正确性测试
```

### 5）快速开始

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'

make lint
make test

python -m data_bridge_pipeline.cli doctor --profile profiles/dev.yaml
python -m data_bridge_pipeline.cli run --profile profiles/dev.yaml
```

### 6）Rithmic 原始流（当前已跑通）

- VPS 配置：`profiles/vps_rithmic.yaml`
- VPS 采集+上传脚本：`scripts/vps_capture_push.sh`
- Mac 归档路径：`/Volumes/extdisk/data-bridge-pipeline`
- 数据集说明文件（供其他 Agent 理解）：
  - `rithmic_raw/DATASET_DESCRIPTION.md`

### 7）安全与稳健建议

- 禁止提交真实密钥到仓库。
- R2 访问密钥按最小权限原则配置。
- 队列前缀按数据集隔离，避免误拉/误删。
- 保留运行日志与对账报告，便于追溯。

### 8）质量保障

- Lint：Ruff
- 测试：Pytest
- 格式化：Black
- CI：GitHub Actions

### 9）后续计划

- 输出完整三端对账报告（VPS+R2+Mac）
- 可选 Parquet 转换 worker
- 可选状态面板

---

## License

MIT
