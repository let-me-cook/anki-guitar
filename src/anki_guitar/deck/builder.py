from __future__ import annotations

import random
from pathlib import Path

import genanki

from anki_guitar.theory.chords import ChordFormulaItem
from anki_guitar.theory.intervals import IntervalItem


class IntervalDeckBuilder:
    def __init__(self, deck_name: str, model_name: str = "Directed Interval (Image Prompt)") -> None:
        self.deck = genanki.Deck(deck_id=_deck_id(deck_name), name=deck_name)
        self.model = genanki.Model(
            model_id=_model_id(deck_name),
            name=model_name,
            fields=[
                {"name": "Question"},
                {"name": "Image"},
                {"name": "Answer"},
            ],
            templates=[
                {
                    "name": "Interval Card",
                    "qfmt": "<h3>{{Question}}</h3>",
                    "afmt": (
                        "<h3>{{Question}}</h3><div>{{Image}}</div>"
                        "<hr id='answer'><p><b>Answer:</b> {{Answer}}</p>"
                    ),
                }
            ],
            css="""
                .card {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    color: #1f2933;
                    background: #f8f9fa;
                }
                img {
                    max-width: 90%;
                    height: auto;
                    border-radius: 8px;
                }
            """,
        )

    def add_interval(
        self, question: str, answer: str, media_file_name: str
    ) -> None:
        note = genanki.Note(
            model=self.model,
            fields=[
                question,
                f"<img src='{media_file_name}'>",
                answer,
            ],
        )
        self.deck.add_note(note)

    def write_package(self, output_path: Path, media_files: list[str]) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        package = genanki.Package(self.deck)
        package.media_files = media_files
        package.write_to_file(str(output_path))


class ChordFormulaDeckBuilder:
    def __init__(self, deck_name: str) -> None:
        self.deck = genanki.Deck(deck_id=_deck_id(deck_name), name=deck_name)
        self.model = genanki.Model(
            model_id=_model_id(deck_name),
            name="Chord Formula (Root-Agnostic)",
            fields=[
                {"name": "Question"},
                {"name": "Image"},
                {"name": "Category"},
                {"name": "Answer"},
            ],
            templates=[
                {
                    "name": "Chord Formula Card",
                    "qfmt": (
                        "<h3>{{Question}}</h3><div>{{Image}}</div>"
                        "<p style='color:#52606d; font-size: 18px;'>Category: {{Category}}</p>"
                    ),
                    "afmt": "{{FrontSide}}<hr id='answer'><p><b>Answer:</b> {{Answer}}</p>",
                }
            ],
            css="""
                .card {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    color: #1f2933;
                    background: #f8f9fa;
                }
            """,
        )

    def add_chord_formula(self, item: ChordFormulaItem, media_file_name: str) -> None:
        note = genanki.Note(
            model=self.model,
            fields=[
                item.prompt,
                f"<img src='{media_file_name}'>",
                item.category.title(),
                item.answer,
            ],
        )
        self.deck.add_note(note)

    def write_package(self, output_path: Path, media_files: list[str]) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        package = genanki.Package(self.deck)
        package.media_files = media_files
        package.write_to_file(str(output_path))


def _deck_id(name: str) -> int:
    rng = random.Random(name + ":deck")
    return rng.randrange(1 << 30, 1 << 31)


def _model_id(name: str) -> int:
    rng = random.Random(name + ":model")
    return rng.randrange(1 << 30, 1 << 31)
