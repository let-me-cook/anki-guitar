from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BuildConfig:
    project_root: Path
    assets_dir: Path
    dist_dir: Path
    deck_name: str = "Anki Guitar - Chromatic Circle"


def default_config(project_root: Path | None = None) -> BuildConfig:
    root = (project_root or Path.cwd()).resolve()
    return BuildConfig(
        project_root=root,
        assets_dir=root / "assets",
        dist_dir=root / "dist",
    )

