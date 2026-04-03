from __future__ import annotations

import argparse

from anki_guitar.config import default_config
from anki_guitar.render.svg_renderer import SvgRenderer
from anki_guitar.theory.intervals import IntervalItem
from anki_guitar.theory.pitch import PitchClass, pitch_index_from_name


def _clear_generated_assets(directory: Path) -> None:
    for path in directory.glob("interval_*.svg"):
        path.unlink()


def run() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a single SVG chromatic circle preview for a note pair."
    )
    parser.add_argument("--source", default="C", help="Source note name, e.g. C, F#, Bb")
    parser.add_argument("--target", default="E", help="Target note name, e.g. D#, Gb, A")
    args = parser.parse_args()

    source_idx = pitch_index_from_name(args.source)
    target_idx = pitch_index_from_name(args.target)
    if source_idx == target_idx:
        raise ValueError("Source and target must differ for interval preview.")

    item = IntervalItem(
        source=PitchClass(source_idx),
        target=PitchClass(target_idx),
        semitones=(target_idx - source_idx) % 12,
    )

    cfg = default_config()
    svg_assets_dir = cfg.assets_dir / "svg"
    svg_assets_dir.mkdir(parents=True, exist_ok=True)
    _clear_generated_assets(svg_assets_dir)
    output = svg_assets_dir / f"{item.media_stem}.svg"
    SvgRenderer(size=1000).render_interval(item=item, output_path=output)
    print(f"Wrote SVG preview -> {output}")


if __name__ == "__main__":
    run()
