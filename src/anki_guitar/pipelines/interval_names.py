from __future__ import annotations

from pathlib import Path

from anki_guitar.config import default_config
from anki_guitar.deck.builder import IntervalDeckBuilder
from anki_guitar.render.typst_renderer import TypstRenderer
from anki_guitar.theory.intervals import generate_directed_intervals_excluding_unison


def _clear_generated_assets(directory: Path) -> None:
    for path in directory.glob("interval_down_*.png"):
        path.unlink()


def run() -> None:
    cfg = default_config()
    cfg.assets_dir.mkdir(parents=True, exist_ok=True)
    cfg.dist_dir.mkdir(parents=True, exist_ok=True)
    interval_assets_dir = cfg.assets_dir / "intervals"
    interval_assets_dir.mkdir(parents=True, exist_ok=True)
    _clear_generated_assets(interval_assets_dir)

    intervals = generate_directed_intervals_excluding_unison(
        directions=("ascending", "descending")
    )
    if len(intervals) != 264:
        raise RuntimeError(f"Expected 264 named interval cards, got {len(intervals)}")

    template_path = (
        Path(__file__).resolve().parent.parent
        / "render"
        / "templates"
        / "interval_circle.typ"
    )
    renderer = TypstRenderer(template_path=template_path)
    deck = IntervalDeckBuilder(
        deck_name="Anki Guitar - Interval Names",
        model_name="Named Interval Recall",
    )

    media_files: list[str] = []
    for item in intervals:
        output_path = interval_assets_dir / f"{item.media_stem}.png"
        renderer.render_interval(item=item, output_path=output_path)
        media_files.append(str(output_path))
        deck.add_interval(
            question=item.named_prompt,
            answer=item.answer,
            media_file_name=output_path.name,
        )

    package_path = cfg.dist_dir / "anki-guitar-interval-names.apkg"
    deck.write_package(output_path=package_path, media_files=media_files)
    print(f"Built named interval deck with {len(intervals)} cards -> {package_path}")


if __name__ == "__main__":
    run()

