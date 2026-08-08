#!/usr/bin/env python3
"""
Sets 'weight' front matter on Hugo content files to match outline order.
Run from your Hugo project root: python3 set_weights.py
"""

import re
from pathlib import Path

# Maps file path (relative to content/) -> weight
# Order within each folder reflects the outline order.
WEIGHTS = {
    # Introduction
    "introduction/_index.md": 1,
    "introduction/who-we-are.md": 1,
    "introduction/what-is-christian-middle-earth.md": 2,
    "introduction/methodology/_index.md": 3,
    "introduction/methodology/hermeneutical-approach.md": 1,
    "introduction/methodology/creation-evolution-debate.md": 2,

    # Chapters (top-level order)
    "chapters/chapter-01-creation-cosmic-temple/_index.md": 1,
    "chapters/chapter-02-calling-and-vocation/_index.md": 2,
    "chapters/chapter-03-fall-the-first/_index.md": 3,
    "chapters/chapter-04-in-sorrow-thou-shalt-bring-forth-children/_index.md": 4,
    "chapters/chapter-05-these-are-the-generations/_index.md": 5,
    "chapters/chapter-06-fall-the-second/_index.md": 6,
    "chapters/chapter-07/_index.md": 7,
    "chapters/chapter-08/_index.md": 8,
    "chapters/chapter-09/_index.md": 9,
    "chapters/chapter-10/_index.md": 10,
    "chapters/chapter-11-fall-the-third/_index.md": 11,

    # Chapter 1
    "chapters/chapter-01-creation-cosmic-temple/heptalogue.md": 1,
    "chapters/chapter-01-creation-cosmic-temple/waters-of-chaos.md": 2,
    "chapters/chapter-01-creation-cosmic-temple/the-spirit.md": 3,
    "chapters/chapter-01-creation-cosmic-temple/three-tier-dwelling-spaces.md": 4,
    "chapters/chapter-01-creation-cosmic-temple/filling-the-spaces/_index.md": 5,
    "chapters/chapter-01-creation-cosmic-temple/filling-the-spaces/man-in-gods-image.md": 1,
    "chapters/chapter-01-creation-cosmic-temple/filling-the-spaces/generous-host.md": 2,
    "chapters/chapter-01-creation-cosmic-temple/temple-dedication.md": 6,
    "chapters/chapter-01-creation-cosmic-temple/creation-as-exodus.md": 7,

    # Chapter 2
    "chapters/chapter-02-calling-and-vocation/every-temple-needs-a-priest.md": 1,
    "chapters/chapter-02-calling-and-vocation/trees-and-rivers.md": 2,
    "chapters/chapter-02-calling-and-vocation/every-priest-needs-an-ezer.md": 3,

    # Chapter 3
    "chapters/chapter-03-fall-the-first/serpent-snake-or-dragon.md": 1,
    "chapters/chapter-03-fall-the-first/knowledge-of-good-and-evil.md": 2,
    "chapters/chapter-03-fall-the-first/god-as-righteous-judge/_index.md": 3,
    "chapters/chapter-03-fall-the-first/god-as-righteous-judge/protoevangelium.md": 1,
    "chapters/chapter-03-fall-the-first/god-as-righteous-judge/clothed-in-skins.md": 2,

    # Chapter 4
    "chapters/chapter-04-in-sorrow-thou-shalt-bring-forth-children/cain-and-abel-offerings.md": 1,
    "chapters/chapter-04-in-sorrow-thou-shalt-bring-forth-children/the-way-of-cain-death.md": 2,
    "chapters/chapter-04-in-sorrow-thou-shalt-bring-forth-children/the-family-of-cain.md": 3,

    # Chapter 5
    "chapters/chapter-05-these-are-the-generations/the-giving-of-a-name.md": 1,
    "chapters/chapter-05-these-are-the-generations/the-path-of-life-through-death.md": 2,

    # Chapter 6
    "chapters/chapter-06-fall-the-second/nephilim-intro-to-deluge.md": 1,
    "chapters/chapter-06-fall-the-second/who-are-the-sons-of-god.md": 2,
    "chapters/chapter-06-fall-the-second/nephilim-giborim-giants.md": 3,
    "chapters/chapter-06-fall-the-second/divine-destruction-and-salvation.md": 4,
    "chapters/chapter-06-fall-the-second/righteousness-and-corruption.md": 5,
    "chapters/chapter-06-fall-the-second/the-ark/_index.md": 6,
    "chapters/chapter-06-fall-the-second/the-ark/gopher-and-kopher.md": 1,
    "chapters/chapter-06-fall-the-second/the-ark/the-ark-as-temple.md": 2,
    "chapters/chapter-06-fall-the-second/the-first-divine-speech.md": 7,

    # Chapter 7
    "chapters/chapter-07/the-second-divine-speech.md": 1,

    # Chapter 8
    "chapters/chapter-08/the-seventeenth-of-abib.md": 1,
    "chapters/chapter-08/god-remembers.md": 2,
    "chapters/chapter-08/parallels-to-genesis-1.md": 3,
    "chapters/chapter-08/noah-patterns-submission-suffering-life.md": 4,

    # Chapter 9
    "chapters/chapter-09/covenant-conclusion.md": 1,
    "chapters/chapter-09/the-sin-of-ham.md": 2,

    # Chapter 10
    "chapters/chapter-10/deuteronomy-32-worldview.md": 1,
    "chapters/chapter-10/the-table-of-nations/_index.md": 2,
    "chapters/chapter-10/the-table-of-nations/sons-of-japheth.md": 1,
    "chapters/chapter-10/the-table-of-nations/sons-of-ham.md": 2,
    "chapters/chapter-10/the-table-of-nations/sons-of-shem.md": 3,

    # Chapter 11
    "chapters/chapter-11-fall-the-third/the-babel-narrative.md": 1,
    "chapters/chapter-11-fall-the-third/tracing-the-name-motif.md": 2,
    "chapters/chapter-11-fall-the-third/tracing-the-city-motif.md": 3,
}


def set_weight(filepath: Path, weight: int):
    text = filepath.read_text(encoding="utf-8")

    if not text.startswith("---"):
        print(f"  SKIP (no front matter found): {filepath}")
        return

    # Split off the front matter block
    parts = text.split("---", 2)
    if len(parts) < 3:
        print(f"  SKIP (malformed front matter): {filepath}")
        return

    front_matter = parts[1]
    rest = parts[2]

    if re.search(r"^weight:.*$", front_matter, flags=re.MULTILINE):
        # Replace existing weight line
        front_matter = re.sub(
            r"^weight:.*$", f"weight: {weight}", front_matter, flags=re.MULTILINE
        )
    else:
        # Insert weight after the 'draft:' line if present, else at the end
        if re.search(r"^draft:.*$", front_matter, flags=re.MULTILINE):
            front_matter = re.sub(
                r"^(draft:.*)$",
                rf"\1\nweight: {weight}",
                front_matter,
                flags=re.MULTILINE,
            )
        else:
            front_matter = front_matter.rstrip("\n") + f"\nweight: {weight}\n"

    new_text = "---" + front_matter + "---" + rest
    filepath.write_text(new_text, encoding="utf-8")
    print(f"  OK weight={weight}: {filepath}")


def main():
    content_dir = Path("content")
    if not content_dir.exists():
        print("ERROR: run this script from your Hugo project root (where 'content/' lives).")
        return

    print(f"Setting weights on {len(WEIGHTS)} files...\n")
    missing = []
    for rel_path, weight in WEIGHTS.items():
        filepath = content_dir / rel_path
        if not filepath.exists():
            missing.append(rel_path)
            continue
        set_weight(filepath, weight)

    if missing:
        print("\nWARNING: these files were not found (check paths/filenames):")
        for m in missing:
            print(f"  - {m}")

    print("\nDone.")


if __name__ == "__main__":
    main()