"""PDF → Markdown parser."""

from pathlib import Path

from .base_parser import BaseParser
from ..utils.markdown_formatter import MarkdownFormatter


class PDFParser(BaseParser):
    """Extract text from PDF files and format as Markdown.

    Uses *pypdf* for text extraction. Falls back to page-by-page plain text
    when structural extraction is not possible.
    """

    def parse(self, file_path: Path) -> str:
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        sections: list[str] = []

        for page_num, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            text = text.strip()
            if not text:
                continue

            heading = MarkdownFormatter.heading(f"Page {page_num}", level=2)
            sections.append(f"{heading}\n\n{text}")

        return "\n\n".join(sections) if sections else "*No extractable text found.*"

    def add_metadata(self, content: str, file_path: Path, **extra) -> str:
        from pypdf import PdfReader

        reader = PdfReader(str(file_path))
        extra.setdefault("Pages", str(len(reader.pages)))
        return super().add_metadata(content, file_path, **extra)

    def _file_type_label(self) -> str:
        return "PDF"
