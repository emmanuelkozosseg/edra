# Repository Guidelines

## Project Structure & Module Organization

This repository is the Emmánuel song archive and its export tooling. Song sources live in `songs/`: `_books.yaml` defines book metadata, while each collection is organized by book and chapter (for example, `songs/emm_hu/700/701-alleluja.yaml`). Keep each song's lyrics, attribution, book references, and optional chords in its YAML file.

Conversion code is in `bin/`. `bin/convert.py` is the command-line entry point; format-specific converters are in `bin/converters/`, with shared logic in `bin/converters/helpers/`. Root-level logo files and `opensong-skeleton.zip` are packaging assets. Generated files belong in `dist/` and are ignored by Git.

## Build, Test, and Development Commands

Run commands from the repository root.

- `bin/build.sh` creates `.venv`, installs `requirements.txt`, rebuilds `dist/`, and produces every supported export and OpenSong ZIP package.
- `python3 -m venv .venv && source .venv/bin/activate && python -m pip install -r requirements.txt` prepares a local development environment.
- `python bin/convert.py emmet-json --from-dir songs/ --to /tmp/emmet.json --version 2026.01.01.` validates the YAML sources by producing one targeted export. Other converter names include `opensong`, `diatar`, `pdf`, `openlyrics`, and `emmasongs`.

There is no committed automated test suite. For changes to a song, run an appropriate conversion and inspect the result; for converter or package changes, run the full build. Do not commit `.venv/` or `dist/`.

## Coding Style & Naming Conventions

Follow the existing Python style: four-space indentation, `snake_case` functions and modules, and concise standard-library-oriented code. Preserve the current converter pattern: implement format behavior in `bin/converters/` and register it in `bin/convert.py`.

Use two-space YAML indentation and retain the established field order where practical: `books`, `about`, `lyrics`, then `chords`. Name song files with their catalog identifier followed by a lowercase, hyphenated title, e.g. `701-alleluja.yaml`. Keep accents and copyright information exactly as supplied.

## Commit & Pull Request Guidelines

Recent history uses short Conventional Commit-style messages, commonly `feat(songs): …`, `fix(songs): …`, `chore(infra): …`, and `docs: …`. Use an imperative, scoped summary; describe affected song IDs or export formats in the body when useful.

Pull requests should state the source and scope of song-data changes, identify any converter behavior changed, and note the validation command run. Include sample output or screenshots when an export's rendered appearance changes, and avoid mixing unrelated song corrections with tooling changes.
