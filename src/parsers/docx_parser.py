"""DOCX → Markdown parser."""

from pathlib import Path

from .base_parser import BaseParser
from ..utils.markdown_formatter import MarkdownFormatter


class DOCXParser(BaseParser):
    """Convert Microsoft Word .docx files to Markdown.

    Uses *python-docx* to iterate over paragraphs and tables, mapping Word
    styles to Markdown headings, lists, and tables.
    """

    # Mapping from Word built-in style names → Markdown heading levels.
    _HEADING_STYLES: dict[str, int] = {
        "Title": 1,
        "Heading 1": 1,
        "Heading 2": 2,
        "Heading 3": 3,
        "Heading 4": 4,
        "Heading 5": 5,
        "Heading 6": 6,
    }

    def parse(self, file_path: Path) -> str:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph

        doc = Document(str(file_path))
        parts: list[str] = []

        for element in doc.element.body:
            tag = element.tag.split("}")[-1]  # strip namespace

            if tag == "p":
                para = Paragraph(element, doc)
                md = self._convert_paragraph(para)
                if md is not None:
                    parts.append(md)

            elif tag == "tbl":
                table = Table(element, doc)
                md = self._convert_table(table)
                if md:
                    parts.append(md)

        return "\n\n".join(parts) if parts else "*Empty document.*"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _convert_paragraph(self, para) -> str | None:
        text = para.text.strip()
        if not text:
            return None

        style_name = para.style.name if para.style else ""

        # Headings
        level = self._HEADING_STYLES.get(style_name)
        if level is not None:
            return MarkdownFormatter.heading(text, level)

        # List items
        if style_name.startswith("List Bullet"):
            return f"- {text}"
        if style_name.startswith("List Number"):
            return f"1. {text}"

        # Default paragraph
        return text

    @staticmethod
    def _convert_table(table) -> str:
        rows = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            rows.append(cells)

        if not rows:
            return ""

        headers = rows[0]
        body = rows[1:]
        return MarkdownFormatter.make_table(headers, body)

    def _file_type_label(self) -> str:
        return "DOCX"
