from __future__ import annotations

import re
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
PAPER_MD = ROOT / "report" / "paper.md"
FIGURES_DIR = ROOT / "figures"
PAPER_DIR = FIGURES_DIR / "paper"


def referenced_paper_targets() -> list[Path]:
    text = PAPER_MD.read_text(encoding="utf-8")
    matches = re.findall(r"figures/(paper/)?([^\s`]+?\.(?:png|jpg|jpeg))", text)
    targets = []
    for paper_prefix, filename in matches:
        if paper_prefix:
            targets.append(PAPER_DIR / filename)
        else:
            targets.append(FIGURES_DIR / filename)
    return sorted(set(targets))


def main() -> None:
    PAPER_DIR.mkdir(parents=True, exist_ok=True)

    moved = []
    already_present = []
    missing = []

    for target in referenced_paper_targets():
        final_target = PAPER_DIR / target.name if target.parent == FIGURES_DIR else target
        source_in_root = FIGURES_DIR / target.name

        if source_in_root.exists():
            final_target.parent.mkdir(parents=True, exist_ok=True)
            if final_target.exists():
                final_target.unlink()
            shutil.move(str(source_in_root), str(final_target))
            moved.append(final_target)
            continue

        if final_target.exists():
            already_present.append(final_target)
            continue

        missing.append(final_target)

    print(f"Paper figures ready in: {PAPER_DIR}")
    print(f"Moved: {len(moved)}")
    print(f"Already present: {len(already_present)}")
    print(f"Missing: {len(missing)}")

    if missing:
        print("Missing paper figure targets:")
        for path in missing:
            print(path.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
