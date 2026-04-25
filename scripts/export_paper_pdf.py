from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import textwrap

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "report" / "paper.md"
OUTPUT = ROOT / "report" / "paper.pdf"

PAGE_W = 8.5
PAGE_H = 11.0
LEFT = 0.82
RIGHT = 0.82
TOP = 0.72
BOTTOM = 0.78
CONTENT_W = PAGE_W - LEFT - RIGHT

SERIF = "DejaVu Serif"
SANS = "DejaVu Sans"
MONO = "DejaVu Sans Mono"
INK = "#17272b"
MUTED = "#53666d"
TEAL = "#1f8790"
RULE = "#c8dbe1"
WASH = "#f3f8f9"


@dataclass
class Block:
    kind: str
    text: str
    level: int = 0
    label: str = ""


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


def parse_markdown(text: str) -> list[Block]:
    blocks: list[Block] = []
    paragraph: list[str] = []
    in_code = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(Block("paragraph", clean_inline(" ".join(paragraph))))
            paragraph = []

    for raw_line in text.replace("\r\n", "\n").splitlines():
        line = raw_line.rstrip()

        if line.strip().startswith("```"):
            if in_code:
                blocks.append(Block("code", "\n".join(code_lines)))
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            flush_paragraph()
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush_paragraph()
            blocks.append(
                Block(
                    "heading",
                    clean_inline(heading.group(2)),
                    level=len(heading.group(1)),
                )
            )
            continue

        ordered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if ordered:
            flush_paragraph()
            blocks.append(Block("ordered", clean_inline(ordered.group(2)), label=ordered.group(1)))
            continue

        if line.startswith("- "):
            flush_paragraph()
            blocks.append(Block("bullet", clean_inline(line[2:])))
            continue

        paragraph.append(line.strip())

    flush_paragraph()
    return blocks


def wrap_text(text: str, font_size: float, width: float = CONTENT_W) -> list[str]:
    average_char_width = font_size * 0.47
    max_chars = max(28, int(width * 72 / average_char_width))
    return textwrap.wrap(
        text,
        width=max_chars,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [""]


class PaperRenderer:
    def __init__(self, pdf: PdfPages):
        self.pdf = pdf
        self.page_number = 0
        self.fig = None
        self.y = PAGE_H - TOP
        self.title = ""

    def new_page(self) -> None:
        if self.fig is not None:
            self.finish_page()

        self.page_number += 1
        self.fig = plt.figure(figsize=(PAGE_W, PAGE_H))
        self.fig.patch.set_facecolor("white")
        self.y = PAGE_H - TOP

        # Subtle top rule gives every page a finished journal-style frame.
        self.line(LEFT, PAGE_H - 0.38, PAGE_W - RIGHT, PAGE_H - 0.38, RULE, 0.7)

    def finish_page(self) -> None:
        if self.fig is None:
            return
        footer_y = 0.38
        self.line(LEFT, footer_y + 0.16, PAGE_W - RIGHT, footer_y + 0.16, "#e2edf0", 0.55)
        self.text(
            LEFT,
            footer_y,
            self.title[:72],
            size=7.7,
            family=SANS,
            color=MUTED,
            va="bottom",
        )
        self.text(
            PAGE_W - RIGHT,
            footer_y,
            str(self.page_number),
            size=8,
            family=SANS,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        self.pdf.savefig(self.fig)
        plt.close(self.fig)
        self.fig = None

    def text(
        self,
        x: float,
        y: float,
        value: str,
        *,
        size: float,
        family: str = SERIF,
        weight: str = "normal",
        style: str = "normal",
        color: str = INK,
        ha: str = "left",
        va: str = "top",
    ) -> None:
        assert self.fig is not None
        self.fig.text(
            x / PAGE_W,
            y / PAGE_H,
            value,
            ha=ha,
            va=va,
            fontsize=size,
            family=family,
            fontweight=weight,
            fontstyle=style,
            color=color,
        )

    def line(self, x0: float, y0: float, x1: float, y1: float, color: str, width: float) -> None:
        assert self.fig is not None
        self.fig.lines.append(
            plt.Line2D(
                [x0 / PAGE_W, x1 / PAGE_W],
                [y0 / PAGE_H, y1 / PAGE_H],
                transform=self.fig.transFigure,
                color=color,
                linewidth=width,
            )
        )

    def rounded_box(self, x: float, y_top: float, w: float, h: float, *, fill: str, edge: str) -> None:
        assert self.fig is not None
        patch = FancyBboxPatch(
            (x / PAGE_W, (y_top - h) / PAGE_H),
            w / PAGE_W,
            h / PAGE_H,
            boxstyle="round,pad=0.012,rounding_size=0.02",
            transform=self.fig.transFigure,
            linewidth=0.8,
            edgecolor=edge,
            facecolor=fill,
        )
        self.fig.patches.append(patch)

    def ensure_space(self, needed: float) -> None:
        if self.y - needed < BOTTOM:
            self.new_page()

    def render_title(self, title: str) -> None:
        self.title = title
        lines = wrap_text(title, 20, width=CONTENT_W - 0.35)
        self.y -= 0.08
        for line in lines:
            self.text(
                PAGE_W / 2,
                self.y,
                line,
                size=20,
                family=SERIF,
                weight="bold",
                ha="center",
            )
            self.y -= 0.34
        self.y -= 0.06
        self.text(
            PAGE_W / 2,
            self.y,
            "Research report | Clinical missing-data robustness benchmark",
            size=8.8,
            family=SANS,
            color=MUTED,
            ha="center",
        )
        self.y -= 0.22
        self.line(LEFT + 1.15, self.y, PAGE_W - RIGHT - 1.15, self.y, TEAL, 1.1)
        self.y -= 0.36

    def render_abstract(self, text: str) -> None:
        lines = wrap_text(text, 9.5, width=CONTENT_W - 0.48)
        line_h = 9.5 / 72 * 1.5
        box_h = 0.58 + len(lines) * line_h + 0.22
        self.ensure_space(box_h + 0.12)
        self.rounded_box(LEFT, self.y, CONTENT_W, box_h, fill=WASH, edge=RULE)
        box_y = self.y - 0.22
        self.text(
            LEFT + 0.24,
            box_y,
            "ABSTRACT",
            size=8.3,
            family=SANS,
            weight="bold",
            color=TEAL,
        )
        box_y -= 0.30
        for line in lines:
            self.text(LEFT + 0.24, box_y, line, size=9.5, family=SERIF, color=INK)
            box_y -= line_h
        self.y -= box_h + 0.38

    def render_heading(self, block: Block) -> None:
        if block.level == 2:
            self.ensure_space(0.72)
            if self.y < PAGE_H - TOP - 0.2:
                self.y -= 0.18
            self.text(LEFT, self.y, block.text, size=15, family=SERIF, weight="bold")
            self.y -= 0.27
            self.line(LEFT, self.y, LEFT + 1.15, self.y, TEAL, 1.0)
            self.y -= 0.26
            return

        if block.level == 3:
            self.ensure_space(0.48)
            self.y -= 0.08
            self.text(LEFT, self.y, block.text, size=11.8, family=SERIF, weight="bold")
            self.y -= 0.34
            return

        self.ensure_space(0.34)
        self.text(LEFT, self.y, block.text, size=10.5, family=SERIF, weight="bold")
        self.y -= 0.30

    def render_paragraph(self, text: str) -> None:
        lines = wrap_text(text, 10.2)
        line_h = 10.2 / 72 * 1.48
        self.ensure_space(len(lines) * line_h + 0.20)
        for line in lines:
            self.text(LEFT, self.y, line, size=10.2, family=SERIF)
            self.y -= line_h
        self.y -= 0.16

    def render_list_item(self, block: Block) -> None:
        label = f"{block.label}." if block.kind == "ordered" else chr(8226)
        indent = 0.32
        label_w = 0.25
        lines = wrap_text(block.text, 10.1, width=CONTENT_W - indent - label_w)
        line_h = 10.1 / 72 * 1.42
        self.ensure_space(len(lines) * line_h + 0.08)
        self.text(LEFT + indent, self.y, label, size=10.1, family=SERIF)
        for i, line in enumerate(lines):
            self.text(
                LEFT + indent + label_w,
                self.y - i * line_h,
                line,
                size=10.1,
                family=SERIF,
            )
        self.y -= len(lines) * line_h + 0.07

    def render_code(self, code: str) -> None:
        lines = code.splitlines() or [""]
        line_h = 8.7 / 72 * 1.35
        box_h = len(lines) * line_h + 0.26
        self.ensure_space(box_h + 0.12)
        self.rounded_box(LEFT, self.y, CONTENT_W, box_h, fill="#f7fafb", edge="#d7e5e9")
        code_y = self.y - 0.16
        for line in lines:
            self.text(LEFT + 0.20, code_y, line, size=8.7, family=MONO, color="#26383d")
            code_y -= line_h
        self.y -= box_h + 0.18


def render_pdf(blocks: list[Block]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUTPUT) as pdf:
        renderer = PaperRenderer(pdf)
        renderer.new_page()

        index = 0
        if blocks and blocks[0].kind == "heading" and blocks[0].level == 1:
            renderer.render_title(blocks[0].text)
            index = 1

        if (
            index + 1 < len(blocks)
            and blocks[index].kind == "heading"
            and blocks[index].text.lower() == "abstract"
            and blocks[index + 1].kind == "paragraph"
        ):
            renderer.render_abstract(blocks[index + 1].text)
            index += 2

        for block in blocks[index:]:
            if block.kind == "heading":
                renderer.render_heading(block)
            elif block.kind == "paragraph":
                renderer.render_paragraph(block.text)
            elif block.kind in {"bullet", "ordered"}:
                renderer.render_list_item(block)
            elif block.kind == "code":
                renderer.render_code(block.text)

        renderer.finish_page()


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    blocks = parse_markdown(text)
    render_pdf(blocks)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
