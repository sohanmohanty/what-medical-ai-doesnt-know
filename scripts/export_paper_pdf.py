from pathlib import Path
import re
import textwrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "report" / "paper.md"
OUTPUT = ROOT / "report" / "paper.pdf"


def markdown_to_plain_text(text: str) -> list[str]:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    lines = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line:
            lines.append("")
            continue

        if line.startswith("- "):
            wrapped = textwrap.wrap(line[2:], width=90)
            if wrapped:
                lines.append(f"- {wrapped[0]}")
                for extra in wrapped[1:]:
                    lines.append(f"  {extra}")
            else:
                lines.append("-")
            continue

        if re.match(r"^\d+\.\s+", line):
            wrapped = textwrap.wrap(line, width=90)
            lines.extend(wrapped if wrapped else [""])
            continue

        wrapped = textwrap.wrap(line, width=90)
        lines.extend(wrapped if wrapped else [""])

    return lines


def render_pdf(lines: list[str]):
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines_per_page = 46

    with PdfPages(OUTPUT) as pdf:
        for start in range(0, len(lines), lines_per_page):
            chunk = lines[start:start + lines_per_page]
            fig = plt.figure(figsize=(8.27, 11.69))
            fig.patch.set_facecolor("white")
            y = 0.97

            for line in chunk:
                fig.text(
                    0.08,
                    y,
                    line if line else " ",
                    ha="left",
                    va="top",
                    family="DejaVu Sans",
                    fontsize=10,
                )
                y -= 0.02

            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)


def main():
    text = SOURCE.read_text(encoding="utf-8")
    lines = markdown_to_plain_text(text)
    render_pdf(lines)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
