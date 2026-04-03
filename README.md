# anki-guitar

Generate Anki decks for guitar/music-theory training using Typst-rendered visuals.

## Intervals deck (semitone recall)

Builds a single deck with ordered chromatic interval pairs excluding same-note pairs:
- `12 x 11 = 132` cards
- Front: root + semitone-distance question
- Back: revealed image + note + interval name answer

## Interval names deck

Builds a second interval deck focused on named recall:
- `264` cards (`132` ascending + `132` descending)
- Front: root + named interval question
- Back: revealed image + note answer

## Chords deck (inversions)

Builds a root-agnostic chord inversion deck:
- `32` cards (`4 triads x 3 inversions` + `5 sevenths x 4 inversions`)
- Front: chord-shape image with connected active notes
- Back: chord quality, inversion, and interval-formula answer

## Commands

```bash
uv sync
uv run python -m anki_guitar.pipelines.intervals
uv run python -m anki_guitar.pipelines.interval_names
uv run python -m anki_guitar.pipelines.chords
uv run python -m anki_guitar.pipelines.svg_preview --source C --target E
```

## Outputs

- `assets/intervals/interval_*.png`
- `assets/chords/chord_*.png`
- `assets/svg/interval_*.svg` (when running SVG preview)
- `dist/anki-guitar-intervals.apkg`
- `dist/anki-guitar-interval-names.apkg`
- `dist/anki-guitar-chords-inversions.apkg`
