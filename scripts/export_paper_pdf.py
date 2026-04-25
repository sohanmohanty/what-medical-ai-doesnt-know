from __future__ import annotations

from dataclasses import dataclass, field
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
LEFT = 0.95
RIGHT = 0.95
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
    cells: list[list[str]] = field(default_factory=list)


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text.strip()


def parse_markdown(text: str) -> list[Block]:
    blocks: list[Block] = []
    paragraph: list[str] = []
    table_lines: list[str] = []
    in_code = False
    in_references = False
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            blocks.append(Block("paragraph", clean_inline(" ".join(paragraph))))
            paragraph = []

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        rows = []
        for row in table_lines:
            cells = [clean_inline(cell.strip()) for cell in row.strip().strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            rows.append(cells)
        if rows:
            blocks.append(Block("table", "", cells=rows))
        table_lines = []

    for raw_line in text.replace("\r\n", "\n").splitlines():
        line = raw_line.rstrip()

        if line.strip().startswith("```"):
            if in_code:
                blocks.append(Block("code", "\n".join(code_lines)))
                code_lines = []
                in_code = False
            else:
                flush_paragraph()
                flush_table()
                in_code = True
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            flush_paragraph()
            flush_table()
            continue

        image = re.match(r"^!\[(.*?)\]\((.*?)\)$", line.strip())
        if image:
            flush_paragraph()
            flush_table()
            blocks.append(Block("figure", clean_inline(image.group(1)), label=image.group(2).strip()))
            continue

        if line.strip().startswith("|") and line.strip().endswith("|"):
            flush_paragraph()
            table_lines.append(line.strip())
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", line)
        if heading:
            flush_paragraph()
            flush_table()
            heading_text = clean_inline(heading.group(2))
            in_references = "references" in heading_text.lower()
            blocks.append(
                Block(
                    "heading",
                    heading_text,
                    level=len(heading.group(1)),
                )
            )
            continue

        if in_references:
            flush_paragraph()
            flush_table()
            blocks.append(Block("reference", clean_inline(line.removeprefix("- ").strip())))
            continue

        ordered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if ordered:
            flush_paragraph()
            flush_table()
            blocks.append(Block("ordered", clean_inline(ordered.group(2)), label=ordered.group(1)))
            continue

        if line.startswith("- "):
            flush_paragraph()
            flush_table()
            blocks.append(Block("bullet", clean_inline(line[2:])))
            continue

        paragraph.append(line.strip())

    flush_paragraph()
    flush_table()
    return blocks


def wrap_text(
    text: str,
    font_size: float,
    width: float = CONTENT_W,
    *,
    break_long_words: bool = False,
) -> list[str]:
    # Use a conservative character-width estimate because PDF text is not clipped
    # to the logical column. This protects the right margin on long scientific lines.
    average_char_width = font_size * 0.56
    max_chars = max(28, int(width * 72 / average_char_width))
    should_break = break_long_words or any(len(token) > max_chars for token in text.split())
    return textwrap.wrap(
        text,
        width=max_chars,
        break_long_words=should_break,
        break_on_hyphens=should_break,
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

    def render_author(self, author: str) -> None:
        self.text(
            PAGE_W / 2,
            self.y + 0.18,
            author,
            size=10.2,
            family=SERIF,
            color=INK,
            ha="center",
        )
        self.y -= 0.06

    def render_abstract(self, text: str) -> None:
        lines = wrap_text(text, 9.7, width=CONTENT_W)
        line_h = 9.7 / 72 * 1.45
        self.ensure_space(0.38 + len(lines) * line_h + 0.30)
        self.text(LEFT, self.y, "Abstract", size=11, family=SERIF, weight="bold")
        self.y -= 0.30
        for line in lines:
            self.text(LEFT, self.y, line, size=9.7, family=SERIF, color=INK)
            self.y -= line_h
        self.y -= 0.20

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

    def render_reference(self, text: str) -> None:
        indent = 0.26
        lines = wrap_text(text, 9.3, width=CONTENT_W - indent, break_long_words=True)
        line_h = 9.3 / 72 * 1.38
        self.ensure_space(len(lines) * line_h + 0.18)
        for i, line in enumerate(lines):
            x = LEFT if i == 0 else LEFT + indent
            self.text(x, self.y - i * line_h, line, size=9.3, family=SERIF, color=INK)
        self.y -= len(lines) * line_h + 0.16

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

    def render_figure(self, block: Block) -> None:
        path = ROOT / block.label
        caption_lines = wrap_text(block.text, 8.3, width=CONTENT_W)
        caption_h = len(caption_lines) * (8.3 / 72 * 1.35) + 0.18
        if not path.exists():
            self.render_paragraph(f"[Missing figure: {block.label}] {block.text}")
            return

        image = plt.imread(path)
        image_h, image_w = image.shape[:2]
        aspect = image_h / image_w
        max_w = CONTENT_W
        max_h = 4.25
        draw_w = min(max_w, max_h / aspect)
        draw_h = draw_w * aspect
        self.ensure_space(draw_h + caption_h + 0.42)
        x = LEFT + (CONTENT_W - draw_w) / 2
        y_bottom = self.y - draw_h
        ax = self.fig.add_axes([x / PAGE_W, y_bottom / PAGE_H, draw_w / PAGE_W, draw_h / PAGE_H])
        ax.imshow(image)
        ax.set_axis_off()
        self.y = y_bottom - 0.12
        for line in caption_lines:
            self.text(LEFT, self.y, line, size=8.3, family=SERIF, style="italic", color=MUTED)
            self.y -= 8.3 / 72 * 1.35
        self.y -= 0.22

    def render_table(self, block: Block) -> None:
        if not block.cells:
            return
        headers = block.cells[0]
        rows = block.cells[1:]
        n_cols = len(headers)
        col_w = CONTENT_W / max(1, n_cols)
        font_size = 7.0 if n_cols >= 6 else 7.8
        line_h = font_size / 72 * 1.30
        row_heights = []
        wrapped_rows = []
        for row in [headers] + rows:
            wrapped = [wrap_text(cell, font_size, width=col_w - 0.08) for cell in row]
            wrapped_rows.append(wrapped)
            row_heights.append(max(len(cell_lines) for cell_lines in wrapped) * line_h + 0.12)
        table_h = sum(row_heights) + 0.16
        self.ensure_space(table_h + 0.20)
        y_top = self.y
        self.line(LEFT, y_top, PAGE_W - RIGHT, y_top, INK, 0.55)
        y = y_top - 0.10
        for r_i, wrapped in enumerate(wrapped_rows):
            if r_i == 1:
                self.line(LEFT, y + 0.04, PAGE_W - RIGHT, y + 0.04, RULE, 0.55)
            for c_i, cell_lines in enumerate(wrapped):
                x = LEFT + c_i * col_w
                for l_i, line in enumerate(cell_lines):
                    self.text(
                        x,
                        y - l_i * line_h,
                        line,
                        size=font_size,
                        family=SANS,
                        weight="bold" if r_i == 0 else "normal",
                        color=INK if r_i == 0 else MUTED,
                    )
            y -= row_heights[r_i]
        self.line(LEFT, y + 0.02, PAGE_W - RIGHT, y + 0.02, INK, 0.55)
        self.y = y - 0.18


def render_pdf(blocks: list[Block]) -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(OUTPUT) as pdf:
        renderer = PaperRenderer(pdf)
        renderer.new_page()

        index = 0
        if blocks and blocks[0].kind == "heading" and blocks[0].level == 1:
            renderer.render_title(blocks[0].text)
            index = 1

        if index < len(blocks) and blocks[index].kind == "paragraph":
            next_block = blocks[index + 1] if index + 1 < len(blocks) else None
            if next_block and next_block.kind == "heading" and next_block.text.lower() == "abstract":
                renderer.render_author(blocks[index].text)
                index += 1

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
            elif block.kind == "reference":
                renderer.render_reference(block.text)
            elif block.kind == "code":
                renderer.render_code(block.text)
            elif block.kind == "figure":
                renderer.render_figure(block)
            elif block.kind == "table":
                renderer.render_table(block)

        renderer.finish_page()


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    blocks = parse_markdown(text)
    render_pdf(blocks)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()
