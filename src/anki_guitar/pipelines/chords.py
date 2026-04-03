from __future__ import annotations

from pathlib import Path

from anki_guitar.config import default_config
from anki_guitar.deck.builder import ChordFormulaDeckBuilder
from anki_guitar.render.typst_renderer import TypstRenderer
from anki_guitar.theory.chords import generate_default_chord_formulas


def _clear_generated_assets(directory: Path) -> None:
    for path in directory.glob("chord_*.png"):
        path.unlink()


def run() -> None:
    cfg = default_config()
    cfg.assets_dir.mkdir(parents=True, exist_ok=True)
    cfg.dist_dir.mkdir(parents=True, exist_ok=True)
    chord_assets_dir = cfg.assets_dir / "chords"
    chord_assets_dir.mkdir(parents=True, exist_ok=True)
    _clear_generated_assets(chord_assets_dir)

    chords = generate_default_chord_formulas()
    if len(chords) != 32:
        raise RuntimeError(f"Expected 32 chord inversion cards, got {len(chords)}")

    template_path = (
        Path(__file__).resolve().parent.parent
        / "render"
        / "templates"
        / "chord_shape.typ"
    )
    renderer = TypstRenderer(template_path=template_path)
    deck = ChordFormulaDeckBuilder(deck_name="Anki Guitar - Chord Inversions")
    media_files: list[str] = []
    for chord in chords:
        output_path = chord_assets_dir / f"{chord.media_stem}.png"
        renderer.render_chord_formula(item=chord, output_path=output_path)
        media_files.append(str(output_path))
        deck.add_chord_formula(chord, media_file_name=output_path.name)

    package_path = cfg.dist_dir / "anki-guitar-chords-inversions.apkg"
    deck.write_package(output_path=package_path, media_files=media_files)
    print(f"Built chord deck with {len(chords)} cards -> {package_path}")


if __name__ == "__main__":
    run()
