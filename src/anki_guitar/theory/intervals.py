from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from anki_guitar.theory.pitch import PitchClass, all_pitch_classes

INTERVAL_NAMES = {
    1: "Minor 2nd",
    2: "Major 2nd",
    3: "Minor 3rd",
    4: "Major 3rd",
    5: "Perfect 4th",
    6: "Tritone",
    7: "Perfect 5th",
    8: "Minor 6th",
    9: "Major 6th",
    10: "Minor 7th",
    11: "Major 7th",
}


IntervalDirection = Literal["ascending", "descending"]


@dataclass(frozen=True)
class IntervalItem:
    source: PitchClass
    target: PitchClass
    semitones: int
    direction: IntervalDirection = "ascending"

    @property
    def media_stem(self) -> str:
        direction_slug = "up" if self.direction == "ascending" else "down"
        return f"interval_{direction_slug}_{self.source.slug}_to_{self.target.slug}"

    @property
    def prompt(self) -> str:
        direction_text = "above" if self.direction == "ascending" else "below"
        return (
            f"Starting on {self.source.label}, which note is "
            f"{self.semitones} semitone{'s' if self.semitones != 1 else ''} {direction_text}?"
        )

    @property
    def interval_name(self) -> str:
        return INTERVAL_NAMES[self.semitones]

    @property
    def named_prompt(self) -> str:
        direction_text = "above" if self.direction == "ascending" else "below"
        return (
            f"Starting on {self.source.label}, which note is "
            f"a {self.interval_name} {direction_text}?"
        )

    @property
    def answer(self) -> str:
        suffix = "semitone" if self.semitones == 1 else "semitones"
        direction_text = "up" if self.direction == "ascending" else "down"
        return (
            f"{self.target.label} "
            f"({self.interval_name} {direction_text}, {self.semitones} {suffix})"
        )


def generate_directed_intervals_excluding_unison(
    directions: tuple[IntervalDirection, ...] = ("ascending",),
) -> list[IntervalItem]:
    notes = all_pitch_classes()
    items: list[IntervalItem] = []
    for direction in directions:
        for source in notes:
            for semitones in range(1, 12):
                if direction == "ascending":
                    target_index = (source.index + semitones) % 12
                else:
                    target_index = (source.index - semitones) % 12
                target = notes[target_index]
                items.append(
                    IntervalItem(
                        source=source,
                        target=target,
                        semitones=semitones,
                        direction=direction,
                    )
                )
    return items
