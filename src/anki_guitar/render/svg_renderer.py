from __future__ import annotations

import math
from pathlib import Path

from anki_guitar.theory.intervals import IntervalItem
from anki_guitar.theory.pitch import PITCH_LABELS_DUAL


class SvgRenderer:
    def __init__(self, size: int = 1000) -> None:
        self.size = size
        self.center = size / 2
        self.radius = size * 0.33

    def render_interval(self, item: IntervalItem, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(self._build_svg(item), encoding="utf-8")

    def _build_svg(self, item: IntervalItem) -> str:
        rel_target = (item.target.index - item.source.index) % 12
        nodes: list[str] = []
        labels: list[str] = []

        for i in range(12):
            angle = math.radians(-90 + (i * 30))
            x = self.center + self.radius * math.cos(angle)
            y = self.center + self.radius * math.sin(angle)
            note_index = (item.source.index + i) % 12

            if i == 0:
                fill = "#D9480F"
            elif i == rel_target:
                fill = "#0B7285"
            else:
                fill = "#F1F3F5"

            nodes.append(
                f"<circle cx='{x:.2f}' cy='{y:.2f}' r='30' fill='{fill}' stroke='#6C757D' stroke-width='2' />"
            )
            labels.append(
                (
                    f"<text x='{x:.2f}' y='{(y + 80):.2f}' text-anchor='middle' "
                    f"font-family='system-ui, -apple-system, Segoe UI, Arial' font-size='24' fill='#212529'>"
                    f"{PITCH_LABELS_DUAL[note_index]}</text>"
                )
            )

        ring = (
            f"<circle cx='{self.center:.2f}' cy='{self.center:.2f}' r='{self.radius:.2f}' "
            "fill='none' stroke='#ADB5BD' stroke-width='3' />"
        )
        title = (
            f"<text x='{self.center:.2f}' y='{(self.center + 8):.2f}' text-anchor='middle' "
            "font-family='system-ui, -apple-system, Segoe UI, Arial' font-size='28' fill='#343A40'>"
            "Chromatic Circle</text>"
        )

        return (
            f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.size}' height='{self.size}' viewBox='0 0 {self.size} {self.size}'>"
            "<rect width='100%' height='100%' fill='#F8F9FA' />"
            f"{ring}{''.join(nodes)}{''.join(labels)}{title}</svg>"
        )

