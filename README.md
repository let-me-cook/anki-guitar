# anki-guitar

Generate Anki decks for guitar/music-theory training using Typst-rendered visuals.

## Intervals deck (current)

Builds a single deck with ordered chromatic interval pairs excluding same-note pairs:
- `12 x 11 = 132` cards
- Front: pair prompt + Typst image
- Back: same image + ascending semitone answer

## Chords deck (inversions)

Builds a root-agnostic chord inversion deck:
- `32` cards (`4 triads x 3 inversions` + `5 sevenths x 4 inversions`)
- Front: chord-shape image with connected active notes
- Back: chord quality, inversion, and interval-formula answer

## Commands

```bash
uv sync
uv run python -m anki_guitar.pipelines.intervals
uv run python -m anki_guitar.pipelines.chords
uv run python -m anki_guitar.pipelines.svg_preview --source C --target E
```

## Outputs

- `assets/intervals/interval_*.png`
- `assets/chords/chord_*.png`
- `assets/svg/interval_*.svg` (when running SVG preview)
- `dist/anki-guitar-intervals.apkg`
- `dist/anki-guitar-chords-inversions.apkg`
