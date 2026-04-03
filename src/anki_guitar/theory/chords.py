from __future__ import annotations

from dataclasses import dataclass

DEGREE_LABELS = (
    "R",
    "b2",
    "2",
    "b3",
    "3",
    "4",
    "b5",
    "5",
    "#5",
    "6",
    "b7",
    "7",
)


@dataclass(frozen=True)
class ChordFormulaItem:
    slug: str
    display_name: str
    intervals: tuple[int, ...]
    bass_interval: int
    inversion_label: str
    shorthand: str
    category: str

    @property
    def prompt(self) -> str:
        return "Identify the chord quality, inversion, and interval formula from this shape."

    @property
    def answer(self) -> str:
        interval_text = ", ".join(str(i) for i in self.intervals)
        bass_label = DEGREE_LABELS[self.bass_interval]
        return (
            f"{self.display_name} ({self.inversion_label}): {interval_text} semitones "
            f"(bass degree: {bass_label}, shorthand: {self.shorthand})"
        )

    @property
    def media_stem(self) -> str:
        return f"chord_{self.slug}_{self.inversion_label.lower().replace(' ', '_')}"


def generate_default_chord_formulas() -> list[ChordFormulaItem]:
    bases = [
        ChordFormulaItem(
            slug="major_triad",
            display_name="Major Triad",
            intervals=(0, 4, 7),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="maj",
            category="triad",
        ),
        ChordFormulaItem(
            slug="minor_triad",
            display_name="Minor Triad",
            intervals=(0, 3, 7),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="min",
            category="triad",
        ),
        ChordFormulaItem(
            slug="diminished_triad",
            display_name="Diminished Triad",
            intervals=(0, 3, 6),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="dim",
            category="triad",
        ),
        ChordFormulaItem(
            slug="augmented_triad",
            display_name="Augmented Triad",
            intervals=(0, 4, 8),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="aug",
            category="triad",
        ),
        ChordFormulaItem(
            slug="major_seventh",
            display_name="Major Seventh",
            intervals=(0, 4, 7, 11),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="maj7",
            category="seventh",
        ),
        ChordFormulaItem(
            slug="dominant_seventh",
            display_name="Dominant Seventh",
            intervals=(0, 4, 7, 10),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="7",
            category="seventh",
        ),
        ChordFormulaItem(
            slug="minor_seventh",
            display_name="Minor Seventh",
            intervals=(0, 3, 7, 10),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="min7",
            category="seventh",
        ),
        ChordFormulaItem(
            slug="half_diminished_seventh",
            display_name="Half-Diminished Seventh",
            intervals=(0, 3, 6, 10),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="m7b5",
            category="seventh",
        ),
        ChordFormulaItem(
            slug="diminished_seventh",
            display_name="Diminished Seventh",
            intervals=(0, 3, 6, 9),
            bass_interval=0,
            inversion_label="Root Position",
            shorthand="dim7",
            category="seventh",
        ),
    ]
    items: list[ChordFormulaItem] = []
    for base in bases:
        items.extend(_inversions_for(base))
    return items


def _inversions_for(base: ChordFormulaItem) -> list[ChordFormulaItem]:
    count = len(base.intervals)
    if count == 3:
        labels = ("Root Position", "1st Inversion", "2nd Inversion")
    elif count == 4:
        labels = ("Root Position", "1st Inversion", "2nd Inversion", "3rd Inversion")
    else:
        raise ValueError(f"Unsupported chord interval length: {count}")

    items: list[ChordFormulaItem] = []
    for inv_idx, label in enumerate(labels):
        ordered = base.intervals[inv_idx:] + base.intervals[:inv_idx]
        items.append(
            ChordFormulaItem(
                slug=base.slug,
                display_name=base.display_name,
                intervals=ordered,
                bass_interval=ordered[0],
                inversion_label=label,
                shorthand=base.shorthand,
                category=base.category,
            )
        )
    return items
