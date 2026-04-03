from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(frozen=True)
class IntervalItem:
    source: PitchClass
    target: PitchClass
    semitones: int

    @property
    def media_stem(self) -> str:
        return f"interval_{self.source.slug}_to_{self.target.slug}"

    @property
    def prompt(self) -> str:
        return (
            f"Starting on {self.source.label}, which note is "
            f"{self.semitones} semitone{'s' if self.semitones != 1 else ''} above?"
        )

    @property
    def interval_name(self) -> str:
        return INTERVAL_NAMES[self.semitones]

    @property
    def answer(self) -> str:
        suffix = "semitone" if self.semitones == 1 else "semitones"
        return f"{self.target.label} ({self.interval_name}, {self.semitones} {suffix})"


def generate_directed_intervals_excluding_unison() -> list[IntervalItem]:
    notes = all_pitch_classes()
    items: list[IntervalItem] = []
    for source in notes:
        for target in notes:
            if source.index == target.index:
                continue
            semitones = (target.index - source.index) % 12
            if semitones == 0:
                continue
            items.append(
                IntervalItem(source=source, target=target, semitones=semitones)
            )
    return items
