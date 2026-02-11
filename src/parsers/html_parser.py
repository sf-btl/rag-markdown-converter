"""HTML → Markdown parser."""

from pathlib import Path

from .base_parser import BaseParser


class HTMLParser(BaseParser):
    """Convert HTML files to Markdown using *html2text*."""

    def parse(self, file_path: Path) -> str:
        import html2text

        raw_html = file_path.read_text(encoding="utf-8", errors="replace")

        converter = html2text.HTML2Text()
        converter.body_width = 0  # no line wrapping
        converter.protect_links = True
        converter.unicode_snob = True
        converter.wrap_links = False
        converter.skip_internal_links = False

        md = converter.handle(raw_html)
        return md.strip() if md.strip() else "*No content extracted from HTML.*"

    def _file_type_label(self) -> str:
        return "HTML"
