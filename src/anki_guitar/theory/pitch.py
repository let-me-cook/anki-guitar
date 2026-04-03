from __future__ import annotations

from dataclasses import dataclass


PITCH_LABELS_DUAL = (
    "C",
    "C#/Db",
    "D",
    "D#/Eb",
    "E",
    "F",
    "F#/Gb",
    "G",
    "G#/Ab",
    "A",
    "A#/Bb",
    "B",
)

PITCH_SLUGS = (
    "C",
    "Cs",
    "D",
    "Ds",
    "E",
    "F",
    "Fs",
    "G",
    "Gs",
    "A",
    "As",
    "B",
)

PITCH_NAME_TO_INDEX = {
    "C": 0,
    "C#": 1,
    "DB": 1,
    "D": 2,
    "D#": 3,
    "EB": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "GB": 6,
    "G": 7,
    "G#": 8,
    "AB": 8,
    "A": 9,
    "A#": 10,
    "BB": 10,
    "B": 11,
}


@dataclass(frozen=True)
class PitchClass:
    index: int

    @property
    def label(self) -> str:
        return PITCH_LABELS_DUAL[self.index]

    @property
    def slug(self) -> str:
        return PITCH_SLUGS[self.index]


def all_pitch_classes() -> tuple[PitchClass, ...]:
    return tuple(PitchClass(i) for i in range(12))


def pitch_index_from_name(name: str) -> int:
    key = name.strip().upper()
    if key not in PITCH_NAME_TO_INDEX:
        raise ValueError(f"Unknown pitch name: {name}")
    return PITCH_NAME_TO_INDEX[key]
