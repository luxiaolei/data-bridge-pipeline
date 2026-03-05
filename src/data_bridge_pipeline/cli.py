"""Typer CLI for data_bridge_pipeline."""

from __future__ import annotations

import json
from pathlib import Path

import typer
import yaml

from data_bridge_pipeline.models import Manifest, PipelineProfile, QueueAction
from data_bridge_pipeline.pipeline import PipelineRunner
from data_bridge_pipeline.queue import QueueProcessor
from data_bridge_pipeline.rclone import RcloneClient
from data_bridge_pipeline.reconcile import reconcile_manifest

app = typer.Typer(help="Manifest-driven data bridge pipeline")


def load_profile(path: str) -> PipelineProfile:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return PipelineProfile(**data)


def load_manifest(path: str) -> Manifest:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Manifest(**data)


@app.command()
def run(profile: str = typer.Option(..., "--profile")) -> None:
    """Run full push + queue gc pass."""
    p = load_profile(profile)
    m = load_manifest(p.manifest_path)
    r = RcloneClient(binary=p.rclone_bin, dry_run=p.dry_run)
    runner = PipelineRunner(p, r)
    runner.push(m)
    gc(profile)


@app.command()
def push(profile: str = typer.Option(..., "--profile")) -> None:
    """Push files from source to destination."""
    p = load_profile(profile)
    m = load_manifest(p.manifest_path)
    PipelineRunner(p, RcloneClient(binary=p.rclone_bin, dry_run=p.dry_run)).push(m)


@app.command()
def pull(profile: str = typer.Option(..., "--profile")) -> None:
    """Pull files from destination to source."""
    p = load_profile(profile)
    m = load_manifest(p.manifest_path)
    PipelineRunner(p, RcloneClient(binary=p.rclone_bin, dry_run=p.dry_run)).pull(m)


@app.command()
def reconcile(
    manifest: str = typer.Option(..., "--manifest"),
    actual: str = typer.Option(..., "--actual"),
) -> None:
    """Reconcile expected manifest with actual path->sha256 map."""
    m = load_manifest(manifest)
    actual_map = json.loads(Path(actual).read_text(encoding="utf-8"))
    report = reconcile_manifest(m, actual_map)
    typer.echo(report.model_dump_json(indent=2))


@app.command()
def gc(profile: str = typer.Option(..., "--profile")) -> None:
    """Process queue operations."""
    p = load_profile(profile)
    queue_file = Path(p.queue_path)
    if not queue_file.exists():
        typer.echo("No queue file found")
        return
    actions_data = json.loads(queue_file.read_text(encoding="utf-8"))
    actions = [QueueAction(**a) for a in actions_data]
    qp = QueueProcessor(
        rclone=RcloneClient(binary=p.rclone_bin, dry_run=p.dry_run),
        delete_after_verify=p.delete_after_verify,
    )
    qp.process(actions)
    typer.echo(f"Processed {len(actions)} queue actions")


@app.command()
def doctor(profile: str = typer.Option(..., "--profile")) -> None:
    """Validate profile and required files."""
    p = load_profile(profile)
    issues: list[str] = []
    if not Path(p.manifest_path).exists():
        issues.append(f"manifest not found: {p.manifest_path}")
    if p.total_shards < 1:
        issues.append("total_shards must be >= 1")
    if not (0 <= p.shard_id < p.total_shards):
        issues.append("shard_id must be in [0, total_shards)")

    if issues:
        for issue in issues:
            typer.echo(f"[FAIL] {issue}")
        raise typer.Exit(code=1)

    typer.echo("[OK] profile validation passed")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
