from __future__ import annotations

import subprocess
from pathlib import Path

from anki_guitar.theory.chords import ChordFormulaItem
from anki_guitar.theory.intervals import IntervalItem


class TypstRenderer:
    def __init__(self, template_path: Path) -> None:
        self.template_path = template_path

    def render_interval(self, item: IntervalItem, output_path: Path) -> None:
        self._render_interval_variant(item=item, output_path=output_path, show_target=True)

    def _render_interval_variant(
        self, item: IntervalItem, output_path: Path, show_target: bool
    ) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        template = self.template_path.read_text(encoding="utf-8")
        subtitle = f"{item.source.label} -> {item.target.label}" if show_target else ""
        rendered = (
            template.replace("{{SOURCE_INDEX}}", str(item.source.index))
            .replace("{{TARGET_INDEX}}", str(item.target.index))
            .replace("{{SHOW_TARGET}}", "1" if show_target else "0")
            .replace("{{SUBTITLE}}", _escape_typst_string(subtitle))
        )

        src_path = output_path.with_suffix(".typ")
        src_path.write_text(rendered, encoding="utf-8")
        try:
            result = subprocess.run(
                [
                    "typst",
                    "compile",
                    str(src_path),
                    str(output_path),
                    "--format",
                    "png",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Typst compile failed for {output_path.name}: {result.stderr.strip()}"
                )
        finally:
            if src_path.exists():
                src_path.unlink()

    def render_chord_formula(self, item: ChordFormulaItem, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        template = self.template_path.read_text(encoding="utf-8")

        active_indices = ", ".join(str(i) for i in sorted(set(item.intervals)))
        ring = list(item.intervals)
        edge_pairs = [(ring[i], ring[(i + 1) % len(ring)]) for i in range(len(ring))]
        edge_pairs_text = ", ".join(f"({a}, {b})" for a, b in edge_pairs)
        subtitle = (
            f"{item.inversion_label} | Intervals: {', '.join(str(i) for i in item.intervals)}"
            f" | {item.shorthand}"
        )

        rendered = (
            template.replace("{{ACTIVE_INDICES}}", active_indices)
            .replace("{{EDGE_PAIRS}}", edge_pairs_text)
            .replace("{{BASS_INDEX}}", str(item.bass_interval))
            .replace(
                "{{TITLE}}",
                _escape_typst_string(f"{item.display_name} ({item.inversion_label})"),
            )
            .replace("{{SUBTITLE}}", _escape_typst_string(subtitle))
        )

        src_path = output_path.with_suffix(".typ")
        src_path.write_text(rendered, encoding="utf-8")
        try:
            result = subprocess.run(
                [
                    "typst",
                    "compile",
                    str(src_path),
                    str(output_path),
                    "--format",
                    "png",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise RuntimeError(
                    f"Typst compile failed for {output_path.name}: {result.stderr.strip()}"
                )
        finally:
            if src_path.exists():
                src_path.unlink()


def _escape_typst_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')
